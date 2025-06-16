# Creating Custom Parsers

This comprehensive guide covers everything you need to know about creating custom parsers for OPAL, from web scraping fundamentals to practical implementation.

## Table of Contents
1. [Introduction to Web Scraping](#introduction-to-web-scraping)
2. [Core Concepts](#core-concepts)
3. [Beautiful Soup Fundamentals](#beautiful-soup-fundamentals)
4. [BaseParser Architecture](#baseparser-architecture)
5. [Step-by-Step Parser Creation](#step-by-step-parser-creation)
6. [Real-World Examples](#real-world-examples)
7. [Special Cases & Advanced Topics](#special-cases--advanced-topics)
8. [Registration & Testing](#registration--testing)
9. [Best Practices & Common Challenges](#best-practices--common-challenges)

## Introduction to Web Scraping

Web scraping is the process of programmatically extracting data from websites. OPAL uses web scraping to gather news articles and court records from Alabama-based websites.

### Key Components
1. **HTTP Requests**: Fetching web pages from servers
2. **HTML Parsing**: Extracting structured data from HTML
3. **Data Extraction**: Finding specific information within the parsed content
4. **Error Handling**: Gracefully managing network issues and unexpected content

## Core Concepts

### HTTP Requests and Responses

When scraping websites, you're making HTTP requests to web servers:

```python
import requests

response = requests.get('https://example.com')
print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.headers.get('Content-Type')}")
```

Common status codes:
- **200**: Success
- **404**: Not Found
- **403**: Forbidden
- **500**: Server Error

### HTML Structure and DOM

HTML documents have a tree-like structure called the DOM (Document Object Model):

```html
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <div class="article">
      <h1>Article Title</h1>
      <p>Article content...</p>
    </div>
  </body>
</html>
```

## Beautiful Soup Fundamentals

Beautiful Soup is Python's primary HTML parsing library. OPAL uses it extensively for extracting data.

### Basic Usage

```python
from bs4 import BeautifulSoup

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find elements
title = soup.find('title')
all_links = soup.find_all('a')
article_div = soup.find('div', class_='article')
```

### Key Methods

| Method | Description | Example |
|--------|-------------|---------|
| `find()` | Find first matching element | `soup.find('h1')` |
| `find_all()` | Find all matching elements | `soup.find_all('p')` |
| `select()` | CSS selector | `soup.select('.article h1')` |
| `get_text()` | Extract text content | `element.get_text(strip=True)` |
| `get()` | Get attribute value | `link.get('href')` |

### Navigation

```python
# Parent/child navigation
parent = element.parent
children = element.children
next_sibling = element.next_sibling

# Finding by attributes
articles = soup.find_all('div', {'class': 'article', 'data-type': 'news'})
```

## BaseParser Architecture

OPAL uses an Abstract Base Class (ABC) design pattern for parsers. This ensures consistency while allowing flexibility.

### The BaseParser Class

```python
from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Abstract base class for all OPAL parsers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OPAL Web Scraper'
        })
    
    @abstractmethod
    def parse_article(self, url):
        """Must be implemented by each parser"""
        pass
    
    @abstractmethod
    def extract_article_data(self, soup):
        """Must be implemented by each parser"""
        pass
```

### Why Abstract Base Classes?

1. **Enforces Interface**: All parsers must implement required methods
2. **Code Reuse**: Common functionality in base class
3. **Type Safety**: Better IDE support and error detection
4. **Extensibility**: Easy to add new parsers

## Step-by-Step Parser Creation

### Step 1: Create Your Parser Class

Create a new file in the `opal/` directory:

```python
# opal/parser_mynews.py
from opal.parser_module import BaseParser
from bs4 import BeautifulSoup
import requests

class ParserMyNews(BaseParser):
    def __init__(self):
        super().__init__()
        self.source_name = "My News Site"
```

### Step 2: Implement Required Methods

```python
def parse_article(self, url):
    """Parse a single article from the given URL"""
    try:
        response = self.make_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self.extract_article_data(soup, url)
    except Exception as e:
        print(f"Error parsing article {url}: {e}")
    return None

def make_request(self, url):
    """Make HTTP request with error handling"""
    try:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None
```

### Step 3: Implement Data Extraction

```python
def extract_article_data(self, soup, url):
    """Extract structured data from the parsed HTML"""
    try:
        # Extract title
        title_element = soup.find('h1', class_='article-title')
        title = title_element.get_text(strip=True) if title_element else "No title"
        
        # Extract author
        author_element = soup.find('span', class_='author-name')
        author = author_element.get_text(strip=True) if author_element else "Unknown"
        
        # Extract date
        date_element = soup.find('time', class_='publish-date')
        date = date_element.get('datetime', 'Unknown date') if date_element else "Unknown date"
        
        # Extract content
        content_div = soup.find('div', class_='article-content')
        paragraphs = content_div.find_all('p') if content_div else []
        
        # Format content
        line_content = {}
        for i, p in enumerate(paragraphs, 1):
            text = p.get_text(strip=True)
            if text:  # Skip empty paragraphs
                line_content[f"line {i}"] = text
        
        return {
            'url': url,
            'title': title,
            'author': author,
            'date': date,
            'line_count': len(line_content),
            'line_content': line_content
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None
```

### Step 4: Handle Article Discovery

```python
def get_article_links(self, base_url, suffix=None, max_pages=None):
    """Discover article links from the news site"""
    all_links = set()
    page = 1
    
    while True:
        if max_pages and page > max_pages:
            break
            
        page_url = f"{base_url}?page={page}"
        response = self.make_request(page_url)
        
        if not response:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find article links
        articles = soup.find_all('a', class_='article-link')
        
        if not articles:
            break  # No more articles
            
        for article in articles:
            href = article.get('href')
            if href:
                # Make absolute URL
                full_url = urljoin(base_url, href)
                
                # Apply suffix filter if provided
                if not suffix or suffix in full_url:
                    all_links.add(full_url)
        
        page += 1
    
    return list(all_links)
```

## Real-World Examples

### Example 1: Parser1819 (Simple News Site)

```python
class Parser1819(BaseParser):
    def extract_article_data(self, soup, url):
        # Real implementation from OPAL
        title = soup.find('title').text.strip() if soup.find('title') else "No title"
        
        # Author extraction with multiple fallbacks
        author = "Unknown author"
        author_tags = soup.find_all('a', {'rel': 'author'})
        if author_tags:
            author = author_tags[0].text.strip()
        
        # Date extraction from meta tag
        date = "Unknown date"
        date_tag = soup.find('meta', {'property': 'article:published_time'})
        if date_tag:
            date = date_tag.get('content', 'Unknown date')
```

### Example 2: ParserAppealsAL (JavaScript-Heavy Site)

```python
class ParserAppealsAL(BaseParser):
    def __init__(self):
        super().__init__()
        # Uses Selenium for JavaScript rendering
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)
    
    def parse_article(self, url):
        # Load page with JavaScript
        self.driver.get(url)
        # Wait for content to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "case-table"))
        )
        # Parse rendered HTML
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
```

## Special Cases & Advanced Topics

### JavaScript-Rendered Content

Some sites load content dynamically with JavaScript. Use Selenium:

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_selenium_parser(self):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run without GUI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    self.driver = webdriver.Chrome(options=options)
```

### Handling Pagination

```python
def handle_pagination(self, base_url, max_pages=None):
    """Navigate through paginated content"""
    page = 1
    all_data = []
    
    while True:
        if max_pages and page > max_pages:
            break
            
        # Different pagination patterns
        page_url = f"{base_url}?page={page}"  # Query parameter
        # OR: page_url = f"{base_url}/page/{page}"  # Path-based
        
        response = self.make_request(page_url)
        if not response or response.status_code == 404:
            break  # No more pages
            
        # Extract data from page
        data = self.extract_page_data(response)
        if not data:
            break  # No data found
            
        all_data.extend(data)
        page += 1
    
    return all_data
```

### Rate Limiting

Respect server resources:

```python
import time

def parse_with_rate_limit(self, urls, delay=1):
    """Parse URLs with delay between requests"""
    results = []
    
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(delay)  # Delay between requests
            
        result = self.parse_article(url)
        if result:
            results.append(result)
    
    return results
```

## Registration & Testing

### Register Your Parser

Add your parser to `opal/__main__.py`:

```python
from opal.parser_mynews import ParserMyNews

# In the parser dictionary
parsers = {
    'Parser1819': Parser1819,
    'ParserDailyNews': ParserDailyNews,
    'ParserAppealsAL': ParserAppealsAL,
    'ParserMyNews': ParserMyNews  # Add your parser here
}
```

### Test Your Parser

1. **Unit Test**:
```python
# tests/test_parser_mynews.py
import pytest
from opal.parser_mynews import ParserMyNews

def test_parser_initialization():
    parser = ParserMyNews()
    assert parser.source_name == "My News Site"

def test_extract_article_data():
    parser = ParserMyNews()
    # Test with sample HTML
    html = '<h1 class="article-title">Test Article</h1>'
    soup = BeautifulSoup(html, 'html.parser')
    data = parser.extract_article_data(soup, 'http://test.com')
    assert data['title'] == 'Test Article'
```

2. **Integration Test**:
```bash
# Test with one page
python -m opal --url https://mynews.com --parser ParserMyNews --max_pages 1

# Verify output
cat YYYY-MM-DD_ParserMyNews.json
```

## Best Practices & Common Challenges

### Best Practices

1. **Error Handling**
   - Always use try-except blocks
   - Log errors with context
   - Return None or empty data on failure
   - Never let parser crash the entire application

2. **Respect robots.txt**
   ```python
   from urllib.robotparser import RobotFileParser
   
   def check_robots_txt(self, url):
       rp = RobotFileParser()
       rp.set_url(urljoin(url, '/robots.txt'))
       rp.read()
       return rp.can_fetch('*', url)
   ```

3. **User-Agent Headers**
   - Always set a descriptive User-Agent
   - Include contact information if scraping extensively

4. **Data Validation**
   - Verify extracted data makes sense
   - Handle missing fields gracefully
   - Validate URLs before making requests

5. **Performance**
   - Use session objects for connection pooling
   - Implement caching for repeated requests
   - Consider concurrent requests for large datasets

### Common Challenges

1. **Dynamic Content**
   - **Problem**: Content loaded by JavaScript
   - **Solution**: Use Selenium or analyze API calls

2. **Anti-Scraping Measures**
   - **Problem**: IP blocking, CAPTCHAs
   - **Solution**: Rotate user agents, add delays, respect rate limits

3. **Changing HTML Structure**
   - **Problem**: Site redesigns break selectors
   - **Solution**: Use multiple selectors, flexible matching

4. **Encoding Issues**
   - **Problem**: Special characters display incorrectly
   - **Solution**: Specify encoding: `response.encoding = 'utf-8'`

5. **Large Datasets**
   - **Problem**: Memory issues with thousands of articles
   - **Solution**: Process in batches, write incrementally

### Debugging Tips

```python
# Debug HTML structure
print(soup.prettify())  # See formatted HTML

# Check element existence
if not soup.find('div', class_='article'):
    print("Article container not found!")

# Log selector results
elements = soup.select('.article-title')
print(f"Found {len(elements)} title elements")

# Save problematic HTML
with open('debug.html', 'w') as f:
    f.write(str(soup))
```

## Conclusion

Creating custom parsers for OPAL involves understanding web scraping fundamentals, implementing the BaseParser interface, and handling real-world challenges. Start simple, test thoroughly, and always respect the websites you're scraping.

For more examples, examine the existing parsers in the OPAL codebase. Each demonstrates different techniques for handling various website structures and challenges.