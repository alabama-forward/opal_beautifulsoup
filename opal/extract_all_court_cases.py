#!/usr/bin/env python3
"""
Extract ALL court cases from Alabama Appeals Court
This script will process all available pages
"""
import json
from datetime import datetime
from opal.court_case_parser import CourtCaseParser
from opal.court_url_paginator import parse_court_url

def extract_all_court_cases():
    """Extract all court cases from all available pages"""
    
    # Base URL for Alabama Appeals Court
    base_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29"
    
    # URL from the last page that shows the real total
    last_page_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~12~totalElements~318~totalPages~13%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29"
    
    # Extract the total pages from the last page URL
    _, total_pages = parse_court_url(last_page_url)
    total_pages = total_pages or 13  # Fallback to 13 if parsing fails
    
    print("Alabama Appeals Court - Complete Data Extraction")
    print("==============================================")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total pages to process: {total_pages}")
    print()
    
    # Create parser instance
    parser = CourtCaseParser(headless=True, rate_limit_seconds=2)
    
    try:
        all_cases = []
        
        # Process ALL pages (0-indexed, so 0 to 12 for 13 pages)
        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1} of {total_pages}...", end='', flush=True)
            
            # Build URL for current page
            if page_num == 0:
                page_url = base_url
            else:
                # Update the page number in the URL
                page_url = base_url.replace('number~0', f'number~{page_num}')
                page_url = page_url.replace('totalElements~0~totalPages~0', 'totalElements~318~totalPages~13')
            
            # Parse the page
            result = parser.parse_article(page_url)
            
            if "cases" in result and result['cases']:
                all_cases.extend(result['cases'])
                print(f" Found {len(result['cases'])} cases")
            else:
                print(f" No cases found")
                
        # Create the final output
        output_data = {
            "status": "success",
            "total_cases": len(all_cases),
            "expected_total": 318,  # From the URL
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "extraction_time": datetime.now().strftime("%H:%M:%S"),
            "pages_processed": total_pages,
            "cases": all_cases
        }
        
        # Save to JSON file
        filename = f"alabama_appeals_court_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        print(f"\n✓ Successfully extracted {len(all_cases)} court cases")
        print(f"✓ Expected total: 318 cases")
        print(f"✓ Results saved to {filename}")
        
        # Create CSV table
        csv_filename = f"alabama_appeals_court_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(csv_filename, "w", encoding="utf-8") as f:
            # Write CSV header
            f.write("Court,Case Number,Case Title,Classification,Filed Date,Status,Case Link\n")
            
            # Write each case as a CSV row
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
        
        # Display summary
        print("\nSummary:")
        print(f"- Total cases extracted: {len(all_cases)}")
        print(f"- Pages processed: {total_pages}")
        
        # Verify we got all cases
        if len(all_cases) < 318:
            print(f"\n⚠️  Warning: Expected 318 cases but only found {len(all_cases)}")
            print("   Some pages may have had fewer than 25 cases")
        elif len(all_cases) > 318:
            print(f"\n⚠️  Warning: Found more cases ({len(all_cases)}) than expected (318)")
            print("   There may be duplicates or the total has changed")
        else:
            print("\n✓ Successfully extracted all expected cases!")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure driver is closed
        parser._close_driver()
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    extract_all_court_cases()