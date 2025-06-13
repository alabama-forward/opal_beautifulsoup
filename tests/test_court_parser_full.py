#!/usr/bin/env python3
"""
Full test script for the court parser with multiple pages
"""
import json
from datetime import datetime
from opal.court_case_parser import CourtCaseParser
from opal.court_url_paginator import build_court_url

def test_court_parser_full():
    """Test the court parser with multiple pages"""
    
    # Base URL for Alabama Appeals Court
    base_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29"
    
    print("Alabama Appeals Court Data Extraction")
    print("=====================================")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create parser instance
    parser = CourtCaseParser(headless=True, rate_limit_seconds=3)
    
    try:
        # First, load the initial page to see how many total pages there are
        print("\nLoading first page to determine total pages...")
        first_result = parser.parse_article(base_url)
        
        if "cases" in first_result and first_result['cases']:
            print(f"Found {len(first_result['cases'])} cases on the first page")
            
            # For this test, let's process first 3 pages (or less if fewer exist)
            # In production, you would determine the actual total pages from the response
            max_pages_to_process = 3
            all_cases = []
            
            # Process multiple pages
            for page_num in range(max_pages_to_process):
                print(f"\nProcessing page {page_num + 1} of {max_pages_to_process}...")
                
                if page_num == 0:
                    # We already have the first page data
                    all_cases.extend(first_result['cases'])
                else:
                    # Build URL for subsequent pages
                    page_url = build_court_url(base_url, page_num)
                    result = parser.parse_article(page_url)
                    
                    if "cases" in result and result['cases']:
                        all_cases.extend(result['cases'])
                        print(f"Found {len(result['cases'])} cases on page {page_num + 1}")
                    else:
                        print(f"No cases found on page {page_num + 1}, stopping...")
                        break
            
            # Create the final output
            output_data = {
                "status": "success",
                "total_cases": len(all_cases),
                "extraction_date": datetime.now().strftime("%Y-%m-%d"),
                "extraction_time": datetime.now().strftime("%H:%M:%S"),
                "pages_processed": min(page_num + 1, max_pages_to_process),
                "cases": all_cases
            }
            
            # Save to JSON file with timestamp
            filename = f"alabama_appeals_court_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            
            print(f"\n✓ Successfully extracted {len(all_cases)} court cases")
            print(f"✓ Results saved to {filename}")
            
            # Create a CSV version for easier viewing in spreadsheet applications
            csv_filename = f"alabama_appeals_court_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(csv_filename, "w", encoding="utf-8") as f:
                # Write CSV header
                f.write("Court,Case Number,Case Title,Classification,Filed Date,Status,Case Link\n")
                
                # Write each case as a CSV row
                for case in all_cases:
                    court = case.get('court', '').replace(',', ';')
                    case_num = case.get('case_number', {}).get('text', '').replace(',', ';')
                    title = case.get('case_title', '').replace(',', ';')
                    classification = case.get('classification', '').replace(',', ';')
                    filed = case.get('filed_date', '')
                    status = case.get('status', '')
                    link = f"https://publicportal.alappeals.gov{case.get('case_number', {}).get('link', '')}"
                    
                    f.write(f"{court},{case_num},{title},{classification},{filed},{status},{link}\n")
            
            print(f"✓ CSV table saved to {csv_filename}")
            
            # Display summary statistics
            print("\nSummary Statistics:")
            print(f"- Total cases extracted: {len(all_cases)}")
            print(f"- Pages processed: {min(page_num + 1, max_pages_to_process)}")
            
            # Count by court
            courts = {}
            for case in all_cases:
                court = case.get('court', 'Unknown')
                courts[court] = courts.get(court, 0) + 1
            
            print("\nCases by Court:")
            for court, count in courts.items():
                print(f"- {court}: {count}")
                
            # Count by status
            statuses = {}
            for case in all_cases:
                status = case.get('status', 'Unknown')
                statuses[status] = statuses.get(status, 0) + 1
                
            print("\nCases by Status:")
            for status, count in statuses.items():
                print(f"- {status}: {count}")
                
        else:
            print("Error: No cases found on the first page")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure driver is closed
        parser._close_driver()
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_court_parser_full()