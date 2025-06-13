#!/usr/bin/env python3
"""
Test script for the court parser
"""
import json
from opal.court_case_parser import ParserAppealsAL

def test_court_parser():
    """Test the court parser with a single page"""
    
    # URL for Alabama Appeals Court - first page
    test_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29"
    
    print("Testing Court Case Parser...")
    print(f"URL: {test_url[:100]}...")
    
    # Create parser instance
    parser = ParserAppealsAL(headless=True, rate_limit_seconds=2)
    
    try:
        # Parse just the first page
        print("\nLoading page and extracting court cases...")
        result = parser.parse_article(test_url)
        
        if "cases" in result:
            print(f"\nFound {len(result['cases'])} cases on the first page")
            
            # Save to JSON file
            output_data = {
                "status": "success",
                "total_cases": len(result['cases']),
                "extraction_date": "2025-06-11",
                "cases": result['cases']
            }
            
            with open("test_court_cases.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            
            print("\nResults saved to test_court_cases.json")
            
            # Print first few cases as examples
            if result['cases']:
                print("\nFirst 3 cases:")
                for i, case in enumerate(result['cases'][:3]):
                    print(f"\n{i+1}. {case.get('case_title', 'No title')}")
                    print(f"   Court: {case.get('court', 'N/A')}")
                    print(f"   Case Number: {case.get('case_number', {}).get('text', 'N/A')}")
                    print(f"   Filed: {case.get('filed_date', 'N/A')}")
                    print(f"   Status: {case.get('status', 'N/A')}")
        else:
            print(f"\nError: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
    finally:
        # Ensure driver is closed
        parser._close_driver()

if __name__ == "__main__":
    test_court_parser()