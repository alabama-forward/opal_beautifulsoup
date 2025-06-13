"""
integrated_parser.py - Combines URL collection and article parsing functionality
"""

from typing import Type
import json
from opal.parser_module import NewsParser
from opal.url_catcher_module import get_all_news_urls
from opal.court_url_paginator import paginate_court_urls, is_court_url
from opal.court_case_parser import ParserAppealsAL

class IntegratedNewsParser:
    """Class to handle both URL collection and article parsing"""

    def __init__(self, parser_class: Type[NewsParser]):
        """
        Initialize with specific parser class
        
        Args:
            parser_class: Class reference to specific NewsParser implementation
        """
        self.parser = parser_class()

    def process_site(self, base_url: str, suffix: str ="", max_pages: int = None) -> str:
        """
        Process an entire news site by collecting URLs and parsing articles
        
        Args:
            base_url: Base URL of the news site
            suffix: URL suffix to identify article pages
            max_pages: Maximum number of pages to process
            
        Returns:
            JSON string containing all parsed articles
        """
        # Check if this is a court URL
        if is_court_url(base_url) and isinstance(self.parser, ParserAppealsAL):
            # Handle court case processing
            print("Processing court case data...")
            
            # Get paginated URLs for court portal
            urls = paginate_court_urls(base_url, self.parser)
            print(f"Found {len(urls)} pages to process")
            
            # Parse all court cases
            result = self.parser.parse_all_cases(base_url, urls)
            return json.dumps(result, indent=4, ensure_ascii=False)
        else:
            # Handle regular news site processing
            # Get all article URLs
            urls = get_all_news_urls(base_url, suffix, max_pages)
            print(f"Found {len(urls)} articles to process")

            # Parse all articles using the specified parser
            try:
                parsed_articles = json.loads(self.parser.parse_articles(urls))
                return json.dumps({
                    'success': True,
                    'total_articles': len(parsed_articles),
                    'articles': parsed_articles
                }, indent=4, ensure_ascii=False)
            except json.JSONDecodeError as e:
                return json.dumps({
                    'success': False,
                    'error': str(e),
                    'urls_found': len(urls)
                }, indent=4, ensure_ascii=False)
