"""
opal_module.py - Opposing Positions and Lingo Parser
Base module for parsing different news sources
"""

from typing import List, Dict, Tuple, Any
import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

class BaseParser(ABC):
    """Base class defining the interface for all parsers (news, court cases, etc.)"""

    def make_request(self, urls: List[str]) -> Tuple[List[str], List[str]]:
        """Shared request functionality for all parsers"""
        responses = []
        successful_urls = []

        for url in urls:
            try:
                print(f"Requesting: {url}")
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                responses.append(response.text)
                successful_urls.append(url)
            except requests.exceptions.RequestException:
                print(f"Skipping URL due to error: {url}")
                # Skip this URL and continue with others
                continue

        # If all URLs failed, raise an exception
        if not responses:
            raise ValueError("All URLs failed to process")

        print(f"Successfully processed {len(responses)} out of {len(urls)} URLs")
        return responses, successful_urls
    #This becomes a required element for all subclasses.
    #This is done to ensure that class extensions have required functionality
    @abstractmethod
    def parse_article(self, html: str, url: str) -> Dict[str, Any]:
        """Each parser must implement this method"""

    #This parent function saves all the URLs extracted into a list for later
    def parse_articles(self, urls: List[str]) -> str:
        """Parse multiple articles and return JSON string"""
        responses, successful_urls = self.make_request(urls)
        all_articles = []

        # Make sure we have the same number of responses and URLs
        for i, response in enumerate(responses):
            # Pass both the HTML content and the URL to parse_article
            article = self.parse_article(response, successful_urls[i])
            all_articles.append(article)

        return json.dumps(all_articles, indent=4, ensure_ascii=False)

# Specific parser for 1819 News
class Parser1819(BaseParser):
    """Parser specifically for 1819news.com"""

    #defines the primary parsing function.
    def parse_article(self, html: str, url:str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        
        #json object structure for result
        article = {
            'url':'',
            'title': '',
            'author': '',
            'date': '',
            'line_count': 0,
            'line_content': {}
        }

        # Extract title
        title_tag = soup.title
        if title_tag:
            article['title'] = title_tag.string.strip() if title_tag.string else 'No Title'

        # Extract author and date - with error handling
        author_date_div = soup.find('div', class_='author-date')
        if author_date_div:
            author_link = author_date_div.find('a')
            if author_link:
                article['author'] = author_link.text.strip()
            else:
                article['author'] = 'Unknown Author'

            # Get date - assuming it's separated by '|'
            date_text = author_date_div.text
            if '|' in date_text:
                article['date'] = date_text.split('|')[1].strip()
        else:
            article['author'] = 'Unknown Author'
            article['date'] = 'Unknown Date'

        # Extract paragraphs
        paragraphs = soup.find_all(['p'])
        paragraph_texts = []

        for p in paragraphs:
            text = p.get_text().strip()
            lines = text.split('\n')
            for line in lines:
                if line.strip():
                    paragraph_texts.append(line.strip())

        article['line_count'] = len(paragraph_texts)
        for i, line in enumerate(paragraph_texts, 1):
            article['line_content'][f"line {i}"] = line

        return article

class ParserDailyNews(BaseParser):
    """Parser specific to Alabama Daily News"""

    #We redefine a parser withing this specific subclass because
    #Each news site has its own unique structure we have to navigate
    def parse_article(self, html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        article = {
            'url':'',
            'title': '',
            'author': '',
            'date': '',
            'line_count': 0,
            'line_content': {}
        }

        # Extract title
        title_tag = soup.title
        if title_tag:
            article['title'] = title_tag.string.strip() if title_tag.string else 'No Title'

        # Extract author and date from DailyNews specifically - with error handling
        author_div = soup.find('span', class_='author vcard')
        if author_div and author_div.find('a'):
            article['author'] = author_div.find('a').text.strip()
        else:
            # Explicitly handle the case when author is not found
            article['author'] = 'Unknown Author'
        
        #Extracts author date from DailyNews specifically
        author_date = soup.find('span', class_='post-date')
        if author_date and author_date.find('a'):
            article['date'] = author_date.find('a').text.strip()
        else:
            article['date'] = 'Unknown Date'

        # Extract paragraphs
        paragraphs = soup.find_all(['p'])
        paragraph_texts = []

        for p in paragraphs:
            text = p.get_text().strip()
            lines = text.split('\n')
            for line in lines:
                if line.strip():
                    paragraph_texts.append(line.strip())

        article['line_count'] = len(paragraph_texts)
        for i, line in enumerate(paragraph_texts, 1):
            article['line_content'][f"line {i}"] = line

        return article
