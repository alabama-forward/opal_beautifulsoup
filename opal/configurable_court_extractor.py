#!/usr/bin/env python3
"""
Configurable Court Case Extractor for Alabama Appeals Court
Allows users to set custom search parameters OR use pre-built URLs
"""
import json
import argparse
from datetime import datetime, timedelta
from urllib.parse import quote
from opal.court_case_parser import ParserAppealsAL
from opal.court_url_paginator import parse_court_url


class CourtSearchBuilder:
    """Builder class for constructing Alabama Court search URLs with court-specific parameters"""
    
    def __init__(self):
        self.base_url = "https://publicportal.alappeals.gov/portal/search/case/results"
        
        # Court definitions with their specific IDs and configurations
        # NOTE: Court IDs may be dynamically assigned by the website
        # These IDs should be discovered through session initialization
        self.courts = {
            'civil': {
                'name': 'Alabama Civil Court of Appeals',
                'id': None,  # Will be discovered dynamically
                'case_prefix': 'CL',
                'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition']
            },
            'criminal': {
                'name': 'Alabama Court of Criminal Appeals', 
                'id': None,  # Will be discovered dynamically
                'case_prefix': 'CR',
                'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition']
            },
            'supreme': {
                'name': 'Alabama Supreme Court',
                'id': None,  # Will be discovered dynamically
                'case_prefix': 'SC',
                'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition', 'Certified Question']
            }
        }
        
        # Date period mappings
        self.date_periods = {
            '7d': '-7d',
            '1m': '-1m', 
            '3m': '-3m',
            '6m': '-6m',
            '1y': '-1y',
            'custom': 'custom'
        }
        
        self.current_court = 'civil'  # Default court
        self.session_initialized = False
        self.reset_params()
    
    def reset_params(self):
        """Reset all parameters to defaults"""
        court_info = self.courts[self.current_court]
        self.params = {
            'advanced': 'false',
            'courtID': court_info['id'],  # May be None until discovered
            'page': {
                'size': 25,
                'number': 0,
                'totalElements': 0,
                'totalPages': 0
            },
            'sort': {
                'sortBy': 'caseHeader.filedDate',
                'sortDesc': 'true'
            },
            'case': {
                'caseCategoryID': 1000000,  # All categories
                'caseNumberQueryTypeID': 10463,  # Contains
                'caseTitleQueryTypeID': 300054,  # Contains
                'filedDateChoice': '-1y',  # Last year
                'filedDateStart': '',
                'filedDateEnd': '',
                'excludeClosed': 'false'
            }
        }
    
    def discover_court_ids(self, parser_instance):
        """
        Discover court IDs by navigating to the website and inspecting the court selection interface
        
        Args:
            parser_instance: Instance of ParserAppealsAL with active WebDriver
        """
        try:
            # Navigate to the main search page
            search_page_url = "https://publicportal.alappeals.gov/portal/search/case"
            parser_instance.driver.get(search_page_url)
            
            # Wait for the page to load
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            import time
            
            wait = WebDriverWait(parser_instance.driver, 10)
            
            # Wait for page to fully load
            time.sleep(3)
            
            # Try to find court selection elements
            # This is a placeholder implementation - actual selectors would need to be discovered
            try:
                # Look for any dropdown or selection elements that might contain court options
                court_elements = parser_instance.driver.find_elements(By.XPATH, "//select[@id='court'] | //select[contains(@name, 'court')] | //div[contains(@class, 'court')]")
                
                if court_elements:
                    # Try to extract court IDs from dropdown options
                    for element in court_elements:
                        options = element.find_elements(By.TAG_NAME, "option")
                        for option in options:
                            court_name = option.text.lower()
                            court_id = option.get_attribute("value")
                            
                            # Map court names to our court keys
                            if "civil" in court_name and "appeals" in court_name:
                                self.courts['civil']['id'] = court_id
                            elif "criminal" in court_name and "appeals" in court_name:
                                self.courts['criminal']['id'] = court_id
                            elif "supreme" in court_name:
                                self.courts['supreme']['id'] = court_id
                else:
                    # If no court selector found, use fallback approach
                    print("Court selector not found, using fallback discovery method...")
                    # Use known working ID for civil court as baseline
                    self.courts['civil']['id'] = '68f021c4-6a44-4735-9a76-5360b2e8af13'
                    
            except Exception as inner_e:
                print(f"Court element discovery failed: {inner_e}")
                # Use fallback IDs
                self.courts['civil']['id'] = '68f021c4-6a44-4735-9a76-5360b2e8af13'
            
            self.session_initialized = True
            print("Court ID discovery completed:")
            for court_key, court_info in self.courts.items():
                status = "✓" if court_info['id'] else "⚠"
                print(f"  {status} {court_info['name']}: {court_info['id'] or 'Not found'}")
                
        except Exception as e:
            print(f"Warning: Could not discover court IDs automatically: {e}")
            print("Try running your search on the website and searching by URL populated by the search")
            # Use fallback ID for civil court
            self.courts['civil']['id'] = '68f021c4-6a44-4735-9a76-5360b2e8af13'
    
    def set_court_id_manually(self, court_key, court_id):
        """
        Manually set a court ID if automatic discovery fails
        
        Args:
            court_key: 'civil', 'criminal', or 'supreme'
            court_id: The discovered court ID string
        """
        if court_key in self.courts:
            self.courts[court_key]['id'] = court_id
            print(f"Manually set {court_key} court ID to: {court_id}")
        else:
            raise ValueError(f"Invalid court key: {court_key}")
    
    def set_court(self, court_key):
        """
        Set the court to search
        
        Args:
            court_key: 'civil', 'criminal', or 'supreme'
        """
        if court_key not in self.courts:
            raise ValueError(f"Invalid court: {court_key}. Must be one of {list(self.courts.keys())}")
        
        self.current_court = court_key
        self.reset_params()  # Reset params with new court ID
    
    def get_court_info(self):
        """Get information about the current court"""
        return self.courts[self.current_court]
    
    def validate_case_category(self, category):
        """Validate that the category is available for the current court"""
        court_info = self.courts[self.current_court]
        if category not in court_info['categories']:
            raise ValueError(f"Category '{category}' not available for {court_info['name']}. "
                           f"Available: {court_info['categories']}")
        return True
    
    def format_case_number_suggestion(self, year=None):
        """Suggest proper case number format for current court"""
        court_info = self.courts[self.current_court]
        current_year = year or datetime.now().year
        return f"{court_info['case_prefix']}-{current_year}-####"
    
    def set_date_range(self, start_date=None, end_date=None, period='1y'):
        """
        Set the date range for case searches
        
        Args:
            start_date: Start date (YYYY-MM-DD) or None
            end_date: End date (YYYY-MM-DD) or None  
            period: Predefined period ('7d', '1m', '3m', '6m', '1y', 'custom')
        """
        if period == 'custom' and start_date and end_date:
            # Convert dates to the format expected by the portal
            self.params['case']['filedDateChoice'] = 'custom'
            self.params['case']['filedDateStart'] = start_date.replace('-', '*2f')
            self.params['case']['filedDateEnd'] = end_date.replace('-', '*2f')
        else:
            # Use predefined period - validate it exists
            if period not in self.date_periods:
                raise ValueError(f"Invalid date period: {period}. Must be one of {list(self.date_periods.keys())}")
            
            self.params['case']['filedDateChoice'] = self.date_periods[period]
            
            # Calculate dates for display purposes
            today = datetime.now()
            if period == '7d':
                start = today - timedelta(days=7)
            elif period == '1m':
                start = today - timedelta(days=30)
            elif period == '3m':
                start = today - timedelta(days=90)
            elif period == '6m':
                start = today - timedelta(days=180)
            elif period == '1y':
                start = today - timedelta(days=365)
            else:
                start = today - timedelta(days=365)
            
            self.params['case']['filedDateStart'] = start.strftime('%m*2f%d*2f%Y')
            self.params['case']['filedDateEnd'] = today.strftime('%m*2f%d*2f%Y')
    
    def set_case_category(self, category_name=None):
        """
        Set case category filter
        
        Args:
            category_name: Category name ('Appeal', 'Certiorari', 'Original Proceeding', 
                          'Petition', 'Certified Question') or None for all
        """
        if category_name is None:
            self.params['case']['caseCategoryID'] = 1000000  # All categories
            return
        
        # Validate category is available for current court
        self.validate_case_category(category_name)
        
        # Map category names to IDs (these would need to be discovered from the portal)
        category_map = {
            'Appeal': 1000001,
            'Certiorari': 1000002, 
            'Original Proceeding': 1000003,
            'Petition': 1000004,
            'Certified Question': 1000005  # Supreme Court only
        }
        
        if category_name in category_map:
            self.params['case']['caseCategoryID'] = category_map[category_name]
        else:
            raise ValueError(f"Unknown category: {category_name}")
    
    def set_case_number_filter(self, case_number=None, query_type=10463):
        """
        Set case number filter
        
        Args:
            case_number: Case number to search for
            query_type: Query type (10463=contains, check portal for others)
        """
        self.params['case']['caseNumberQueryTypeID'] = query_type
        if case_number:
            self.params['case']['caseNumber'] = case_number
    
    def set_case_title_filter(self, title=None, query_type=300054):
        """
        Set case title filter
        
        Args:
            title: Title text to search for
            query_type: Query type (300054=contains, check portal for others)
        """
        self.params['case']['caseTitleQueryTypeID'] = query_type
        if title:
            self.params['case']['caseTitle'] = title
    
    def set_exclude_closed(self, exclude=False):
        """
        Set whether to exclude closed cases
        
        Args:
            exclude: True to exclude closed cases, False to include all
        """
        self.params['case']['excludeClosed'] = 'true' if exclude else 'false'
    
    def set_sort_order(self, sort_by='caseHeader.filedDate', descending=True):
        """
        Set sort order for results
        
        Args:
            sort_by: Field to sort by
            descending: True for descending, False for ascending
        """
        self.params['sort']['sortBy'] = sort_by
        self.params['sort']['sortDesc'] = 'true' if descending else 'false'
    
    def set_page_info(self, page_number=0, page_size=25, total_elements=0, total_pages=0):
        """Set pagination information"""
        self.params['page'].update({
            'number': page_number,
            'size': page_size,
            'totalElements': total_elements,
            'totalPages': total_pages
        })
    
    def build_criteria_string(self):
        """Build the criteria string for the URL"""
        criteria_parts = []
        
        # Basic parameters
        criteria_parts.append(f"advanced~{self.params['advanced']}")
        criteria_parts.append(f"courtID~%27{self.params['courtID']}")
        
        # Page parameters
        page = self.params['page']
        page_str = f"page~%28size~{page['size']}~number~{page['number']}~totalElements~{page['totalElements']}~totalPages~{page['totalPages']}%29"
        criteria_parts.append(page_str)
        
        # Sort parameters
        sort = self.params['sort']
        sort_str = f"sort~%28sortBy~%27{sort['sortBy']}~sortDesc~{sort['sortDesc']}%29"
        criteria_parts.append(sort_str)
        
        # Case parameters
        case = self.params['case']
        case_parts = []
        case_parts.append(f"caseCategoryID~{case['caseCategoryID']}")
        case_parts.append(f"caseNumberQueryTypeID~{case['caseNumberQueryTypeID']}")
        case_parts.append(f"caseTitleQueryTypeID~{case['caseTitleQueryTypeID']}")
        case_parts.append(f"filedDateChoice~%27{case['filedDateChoice']}")
        case_parts.append(f"filedDateStart~%27{case['filedDateStart']}")
        case_parts.append(f"filedDateEnd~%27{case['filedDateEnd']}")
        case_parts.append(f"excludeClosed~{case['excludeClosed']}")
        
        # Add optional case filters
        if 'caseNumber' in case:
            case_parts.append(f"caseNumber~{quote(case['caseNumber'])}")
        if 'caseTitle' in case:
            case_parts.append(f"caseTitle~{quote(case['caseTitle'])}")
        
        case_str = f"case~%28{'~'.join(case_parts)}%29"
        criteria_parts.append(case_str)
        
        return f"~%28{'~'.join(criteria_parts)}%29"
    
    def build_url(self, page_number=0):
        """Build complete search URL"""
        # Update page number
        self.set_page_info(page_number=page_number, 
                          page_size=self.params['page']['size'],
                          total_elements=self.params['page']['totalElements'],
                          total_pages=self.params['page']['totalPages'])
        
        criteria = self.build_criteria_string()
        return f"{self.base_url}?criteria={criteria}"


def extract_court_cases_with_params(
    court='civil',
    date_period='1y',
    start_date=None,
    end_date=None,
    case_number=None,
    case_title=None,
    case_category=None,
    exclude_closed=False,
    max_pages=None,
    output_prefix="court_cases",
    custom_url=None
):
    """
    Extract court cases with configurable search parameters OR a pre-built URL
    
    Args:
        court: Court to search ('civil', 'criminal', 'supreme') - ignored if custom_url provided
        date_period: Date period ('7d', '1m', '3m', '6m', '1y', 'custom') - ignored if custom_url provided
        start_date: Start date for custom range (YYYY-MM-DD) - ignored if custom_url provided
        end_date: End date for custom range (YYYY-MM-DD) - ignored if custom_url provided
        case_number: Filter by case number (partial match) - ignored if custom_url provided
        case_title: Filter by case title (partial match) - ignored if custom_url provided
        case_category: Filter by category ('Appeal', 'Certiorari', etc.) - ignored if custom_url provided
        exclude_closed: Whether to exclude closed cases - ignored if custom_url provided
        max_pages: Maximum pages to process (None for all)
        output_prefix: Prefix for output files
        custom_url: Pre-built search URL with embedded parameters (overrides all other search params)
    """
    
    if custom_url:
        # Use the provided URL directly
        print("Using custom URL with embedded search parameters")
        print("⚠️  WARNING: Custom URLs contain session-specific parameters that expire.")
        print("   This URL will only work temporarily and may become invalid after your browser session ends.")
        print("   For reliable, repeatable searches, use the CLI search parameters instead of --url option.")
        print()
        base_url = custom_url
        court_name = "Custom Search"  # Generic name since we don't know the court
    else:
        # Build search URL from parameters
        search_builder = CourtSearchBuilder()
        
        # Create parser instance early for court ID discovery
        parser = ParserAppealsAL(headless=True, rate_limit_seconds=2)
        
        # Discover court IDs if not already done
        if not search_builder.session_initialized:
            print("Discovering court IDs from website...")
            search_builder.discover_court_ids(parser)
        
        # Set court
        search_builder.set_court(court)
        court_info = search_builder.get_court_info()
        court_name = court_info['name']
        
        # Verify court ID was discovered
        if court_info['id'] is None:
            raise ValueError(f"Could not discover court ID for {court_name}. "
                           "Try using the --url option with a pre-built search URL instead.")
        
        # Set date range
        if date_period == 'custom':
            if not start_date or not end_date:
                raise ValueError("Custom date range requires both start_date and end_date")
            search_builder.set_date_range(start_date, end_date, 'custom')
        else:
            search_builder.set_date_range(period=date_period)
        
        # Set filters
        if case_number:
            search_builder.set_case_number_filter(case_number)
        if case_title:
            search_builder.set_case_title_filter(case_title)
        if case_category:
            search_builder.set_case_category(case_category)
        
        search_builder.set_exclude_closed(exclude_closed)
        
        # Build initial URL
        base_url = search_builder.build_url(0)
    
    print("Alabama Appeals Court - Configurable Data Extraction")
    print("=" * 55)
    print(f"Court: {court_name}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if not custom_url:
        print(f"Date period: {date_period}")
        if date_period == 'custom':
            print(f"Date range: {start_date} to {end_date}")
        if case_number:
            print(f"Case number filter: {case_number}")
        if case_title:
            print(f"Case title filter: {case_title}")
        if case_category:
            print(f"Case category: {case_category}")
        print(f"Exclude closed: {exclude_closed}")
    print(f"Max pages: {max_pages or 'All available'}")
    print()
    
    # Create parser instance (may have been created earlier for court ID discovery)
    if 'parser' not in locals():
        parser = ParserAppealsAL(headless=True, rate_limit_seconds=2)
    
    try:
        # First, get the first page to determine total pages
        print("Loading first page to determine total results...")
        result = parser.parse_article(base_url)
        
        if "cases" not in result or not result['cases']:
            print("No cases found with the specified criteria.")
            return
        
        # Try to get total pages from the URL after JavaScript execution
        total_pages = None
        if hasattr(parser, 'driver') and parser.driver:
            current_url = parser.driver.current_url
            _, total_pages = parse_court_url(current_url)
            
        if not total_pages:
            # Estimate based on first page results
            total_pages = 1
            print(f"Could not determine total pages, will process incrementally")
        else:
            print(f"Found {total_pages} total pages")
        
        # Apply max_pages limit
        if max_pages and max_pages < total_pages:
            total_pages = max_pages
            print(f"Limited to {max_pages} pages")
        
        all_cases = []
        
        # Process all pages
        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1}...", end='', flush=True)
            
            if page_num == 0:
                # Use result from first page
                page_result = result
            else:
                # Build URL for subsequent pages only if not using custom URL
                if custom_url:
                    # For custom URLs, we need to modify pagination manually
                    # This is a simplified approach - in practice, you'd need to parse and modify the URL
                    page_url = custom_url.replace('number~0', f'number~{page_num}')
                else:
                    page_url = search_builder.build_url(page_num)
                page_result = parser.parse_article(page_url)
            
            if "cases" in page_result and page_result['cases']:
                all_cases.extend(page_result['cases'])
                print(f" Found {len(page_result['cases'])} cases")
            else:
                print(" No cases found")
                # If no cases on this page, we might have reached the end
                break
        
        # Create output data
        output_data = {
            "status": "success",
            "search_parameters": {
                "court": court if not custom_url else "Custom URL",
                "date_period": date_period if not custom_url else "Custom URL",
                "start_date": start_date,
                "end_date": end_date,
                "case_number_filter": case_number,
                "case_title_filter": case_title,
                "case_category": case_category,
                "exclude_closed": exclude_closed,
                "custom_url": custom_url
            },
            "total_cases": len(all_cases),
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "extraction_time": datetime.now().strftime("%H:%M:%S"),
            "pages_processed": page_num + 1,
            "cases": all_cases
        }
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f"{output_prefix}_{timestamp}.json"
        
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        print(f"\n✓ Successfully extracted {len(all_cases)} court cases")
        print(f"✓ Results saved to {json_filename}")
        
        # Create CSV if there are results
        if all_cases:
            csv_filename = f"{output_prefix}_{timestamp}.csv"
            with open(csv_filename, "w", encoding="utf-8") as f:
                f.write("Court,Case Number,Case Title,Classification,Filed Date,Status,Case Link\n")
                
                for case in all_cases:
                    court = case.get('court', '').replace(',', ';')
                    case_num = case.get('case_number', {}).get('text', '').replace(',', ';')
                    title = case.get('case_title', '').replace(',', ';').replace('"', "'")
                    classification = case.get('classification', '').replace(',', ';')
                    filed = case.get('filed_date', '')
                    status = case.get('status', '')
                    link = f"https://publicportal.alappeals.gov{case.get('case_number', {}).get('link', '')}"
                    
                    f.write(f'"{court}","{case_num}","{title}","{classification}","{filed}","{status}","{link}"\n')
            
            print(f"✓ CSV table saved to {csv_filename}")
        
        return output_data
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        parser._close_driver()
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Command line interface for the configurable court extractor"""
    parser = argparse.ArgumentParser(description='Extract Alabama Court cases with configurable search parameters OR custom URL')
    
    # URL option that overrides all search parameters
    parser.add_argument('--url', help='Pre-built search URL with embedded parameters (overrides all search options)')
    
    # Search parameter arguments (ignored if --url is provided)
    parser.add_argument('--court', choices=['civil', 'criminal', 'supreme'], 
                       default='civil', help='Court to search (default: civil)')
    parser.add_argument('--date-period', choices=['7d', '1m', '3m', '6m', '1y', 'custom'], 
                       default='1y', help='Date period for case search (default: 1y)')
    parser.add_argument('--start-date', help='Start date for custom range (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date for custom range (YYYY-MM-DD)')
    parser.add_argument('--case-number', help='Filter by case number (e.g., CL-2024-, CR-2024-, SC-2024-)')
    parser.add_argument('--case-title', help='Filter by case title (partial match)')
    parser.add_argument('--case-category', 
                       choices=['Appeal', 'Certiorari', 'Original Proceeding', 'Petition', 'Certified Question'],
                       help='Filter by case category')
    parser.add_argument('--exclude-closed', action='store_true', 
                       help='Exclude closed cases from results')
    
    # Output options (always available)
    parser.add_argument('--max-pages', type=int, 
                       help='Maximum number of pages to process (default: all)')
    parser.add_argument('--output-prefix', default='court_cases',
                       help='Prefix for output files (default: court_cases)')
    
    args = parser.parse_args()
    
    # If URL is provided, skip all parameter validation
    if args.url:
        print("Using custom URL - all search parameter options will be ignored")
        print("⚠️  IMPORTANT: Custom URLs are session-based and temporary!")
        print("   Your URL may stop working when the court website session expires.")
        print("   Consider using CLI search parameters for reliable, repeatable searches.")
        print()
        extract_court_cases_with_params(
            custom_url=args.url,
            max_pages=args.max_pages,
            output_prefix=args.output_prefix
        )
        return
    
    # Validate custom date range
    if args.date_period == 'custom':
        if not args.start_date or not args.end_date:
            parser.error("Custom date period requires both --start-date and --end-date")
    
    # Validate case category for court
    if args.case_category:
        builder = CourtSearchBuilder()
        builder.set_court(args.court)
        try:
            builder.validate_case_category(args.case_category)
        except ValueError as e:
            parser.error(str(e))
    
    # Show case number format suggestion
    if args.case_number:
        builder = CourtSearchBuilder()
        builder.set_court(args.court)
        suggested_format = builder.format_case_number_suggestion()
        print(f"Case number format for {builder.get_court_info()['name']}: {suggested_format}")
    
    # Extract cases using search parameters
    extract_court_cases_with_params(
        court=args.court,
        date_period=args.date_period,
        start_date=args.start_date,
        end_date=args.end_date,
        case_number=args.case_number,
        case_title=args.case_title,
        case_category=args.case_category,
        exclude_closed=args.exclude_closed,
        max_pages=args.max_pages,
        output_prefix=args.output_prefix
    )


if __name__ == "__main__":
    main()