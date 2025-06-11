"""
main.py - Simple script to run the integrated parser
"""
import json
import argparse
from datetime import datetime
from opal.integrated_parser import IntegratedNewsParser
from opal.parser_module import Parser1819, ParserDailyNews
from opal.court_case_parser import CourtCaseParser

def main():
    """
    Runs news parsers using command line arguments for
    URL, suffix, and max pages
    """

    #Get today's date. You'll use this when saving the file
    today = datetime.today().strftime('%Y-%m-%d')

    # Command-line arguments
    console_arguments = argparse.ArgumentParser(description='Run news parser on specified website')
    console_arguments.add_argument('--url', type=str, required=True,
                                   help='Base URL of the news site (ex. https://1819news.com/)')
    console_arguments.add_argument('--suffix', type=str, required=False,
                                   help='URL suffix to identify article pages (e.g., /news/item)')
    console_arguments.add_argument('--max_pages', type=int, required=False, default=None,
                                   help='Max number of pages to process. Optional but recommended')
    console_arguments.add_argument('--parser', type=str, required=True, default=None,
                                choices=['Parser1819', 'ParserDailyNews', 'court'],
                                help='Pick an available parser')

    # Pass command-line arguments
    args = console_arguments.parse_args()

    parsers = {
        'Parser1819': Parser1819,
        'ParserDailyNews': ParserDailyNews,
        'court': CourtCaseParser
    }

    #Print progress
    print(f"Starting parser with: ${args.parser}")
    print(f"Base URL: {args.url}")
    print(f"Suffix: {args.suffix}")
    print(f"Max Pages: {args.max_pages if args.max_pages else 'No limit'}")

    #Print the news parser class being used
    news_parser_class = parsers[args.parser]
    print(f"Using parser: {args.parser}")


    # Create parser instance
    news_parser = IntegratedNewsParser(news_parser_class)

    #Save the arguments to the news_items variable
    news_urls = news_parser.process_site(
        base_url = args.url,
        suffix=args.suffix,
        max_pages=args.max_pages
    )


   # Print results
    parsed_data = json.loads(news_urls)
    
    # Check if this is court data or news data
    if args.parser == 'court':
        # Handle court case results
        if parsed_data.get('status') == 'success':
            print(f"\nSuccessfully processed {parsed_data['total_cases']} court cases")
            
            # Save to file
            parser_name = args.parser
            with open(f"{today}_{parser_name}.json", 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=4, ensure_ascii=False)
                print(f"\nResults saved to '{today}_{parser_name}.json'")
            
            # Print first case as example
            if parsed_data['cases']:
                print("\nFirst case preview:")
                case = parsed_data['cases'][0]
                print(f"Court: {case['court']}")
                print(f"Case Number: {case['case_number']['text']}")
                print(f"Case Title: {case['case_title']}")
                print(f"Filed Date: {case['filed_date']}")
                print(f"Status: {case['status']}")
        else:
            print(f"\nError occurred: {parsed_data.get('error', 'Unknown error')}")
    else:
        # Handle news article results
        if parsed_data['success']:
            print(f"\nSuccessfully processed {parsed_data['total_articles']} articles")

            # Save to file
            parser_name = args.parser
            with open(f"{today}_{parser_name}.json", 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=4, ensure_ascii=False)
                print(f"\nResults saved to '{today}_{parser_name}.json'")

            # Print first article as example
            if parsed_data['articles']:
                print("\nFirst article preview:")
                article = parsed_data['articles'][0]
                print(f"Title: {article['title']}")
                print(f"Author: {article['author']}")
                print(f"Date: {article['date']}")
                print(f"Number of paragraphs: {article['line_count']}")
        else:
            print(f"\nError occurred: {parsed_data['error']}")

if __name__ == "__main__":
    main()
