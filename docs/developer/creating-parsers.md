# Creating New Parsers

This guide explains how to create a new parser for OPAL to support additional websites.

## Overview

All parsers inherit from the `BaseParser` class, which provides common functionality for web scraping.

## Step 1: Create Parser Class

Create a new Python file in the `opal` directory:

```python
from opal.BaseParser import BaseParser
from bs4 import BeautifulSoup
import requests

class ParserExample(BaseParser):
    def __init__(self, url, suffix="", max_pages=5):
        super().__init__(url, suffix, max_pages)
        self.name = "ExampleParser"
```

## Step 2: Implement Required Methods

### get_article_links()

Extract article URLs from the main page:

```python
def get_article_links(self, page_url):
    """Extract article links from a page."""
    response = requests.get(page_url, headers=self.headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    for article in soup.find_all('article'):
        link = article.find('a')
        if link and link.get('href'):
            full_url = self.url + link['href']
            links.append(full_url)
    
    return links
```

### parse_article()

Extract data from individual articles:

```python
def parse_article(self, article_url):
    """Parse individual article."""
    response = requests.get(article_url, headers=self.headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return {
        'title': soup.find('h1').text.strip(),
        'content': soup.find('div', class_='content').text.strip(),
        'date': soup.find('time')['datetime'],
        'author': soup.find('span', class_='author').text.strip(),
        'url': article_url
    }
```

### extract_article_data()

Main method that orchestrates the scraping:

```python
def extract_article_data(self):
    """Main extraction method."""
    all_articles = []
    
    for page in range(1, self.max_pages + 1):
        page_url = f"{self.url}/page/{page}"
        links = self.get_article_links(page_url)
        
        for link in links:
            try:
                article_data = self.parse_article(link)
                all_articles.append(article_data)
            except Exception as e:
                self.logger.error(f"Error parsing {link}: {e}")
    
    return all_articles
```

## Step 3: Handle Special Cases

### JavaScript-Rendered Content

Use Selenium for dynamic content:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(self):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
```

### Pagination

Handle different pagination styles:

```python
def get_next_page_url(self, current_page):
    # URL parameter style
    return f"{self.url}?page={current_page}"
    
    # Or path style
    return f"{self.url}/page/{current_page}"
    
    # Or offset style
    offset = (current_page - 1) * 20
    return f"{self.url}?offset={offset}"
```

## Step 4: Register Parser

Add your parser to `__main__.py`:

```python
from opal.ParserExample import ParserExample

# In the parser selection logic
if args.parser == 'example':
    parser = ParserExample(args.url, args.suffix, args.max_pages)
```

## Best Practices

1. **Error Handling**: Always wrap parsing logic in try-except blocks
2. **Logging**: Use self.logger for debugging information
3. **Headers**: Use appropriate User-Agent headers
4. **Rate Limiting**: Add delays between requests if needed
5. **Testing**: Test with various edge cases (empty content, missing elements)

## Example: Complete Parser

```python
from opal.BaseParser import BaseParser
from bs4 import BeautifulSoup
import requests
import time

class ParserNewsSite(BaseParser):
    def __init__(self, url, suffix="", max_pages=5):
        super().__init__(url, suffix, max_pages)
        self.name = "NewsSiteParser"
        
    def get_article_links(self, page_url):
        response = requests.get(page_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = []
        for item in soup.select('.article-item'):
            link = item.select_one('a.title-link')
            if link:
                full_url = self.url + link['href']
                links.append(full_url)
                
        return links
    
    def parse_article(self, article_url):
        response = requests.get(article_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'title': soup.select_one('h1.article-title').text.strip(),
            'content': soup.select_one('.article-body').text.strip(),
            'date': soup.select_one('time.publish-date')['datetime'],
            'author': soup.select_one('.author-name').text.strip(),
            'url': article_url,
            'tags': [tag.text for tag in soup.select('.tag')]
        }
    
    def extract_article_data(self):
        all_articles = []
        
        for page in range(1, self.max_pages + 1):
            page_url = f"{self.url}/articles?page={page}"
            self.logger.info(f"Scraping page {page}")
            
            links = self.get_article_links(page_url)
            
            for link in links:
                try:
                    article = self.parse_article(link)
                    all_articles.append(article)
                    time.sleep(1)  # Be respectful
                except Exception as e:
                    self.logger.error(f"Error: {e}")
                    
        return all_articles
```

## Testing Your Parser

```bash
# Test with a small number of pages first
python -m opal --url https://example.com --parser example --max_pages 2

# Check the output
cat opal_output.json | python -m json.tool
```