"""
main.py - Simple script to run the integrated parser
"""
import json
import argparse
from datetime import datetime
from opal.integrated_parser import IntegratedNewsParser
from opal.parser_module import Parser1819, ParserDailyNews

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
                                choices=['Parser1819', 'ParserDailyNews'],
                                help='Pick an available parser')

    # Pass command-line arguments
    args = console_arguments.parse_args()

    parsers = {
        'Parser1819': Parser1819,
        'ParserDailyNews': ParserDailyNews
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
    if parsed_data['success']:
        print(f"\nSuccessfully processed {parsed_data['total_articles']} articles")

        # Save to file
        with open(f"{today}_{news_parser_class}.json", 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=4, ensure_ascii=False)
            print(f"\nResults saved to '{today}_{news_parser_class}.json'")

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
