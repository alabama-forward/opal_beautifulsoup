# BaseParser: Web Scraping Fundamentals Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [HTTP Requests](#http-requests)
4. [HTML Parsing](#html-parsing)
5. [Beautiful Soup](#beautiful-soup)
6. [BaseParser Architecture](#baseparser-architecture)
7. [Implementation Examples](#implementation-examples)
8. [Best Practices](#best-practices)

## Introduction

The `BaseParser` class is the foundation of OPAL's web scraping system. It provides a standardized interface for extracting structured data from websites, whether they're news articles or court records. This guide explains the core concepts behind web scraping and how BaseParser implements them.

## Core Concepts

### What is Web Scraping?

Web scraping is the process of extracting data from websites programmatically. It involves:

1. **Fetching** - Downloading the HTML content from a web server
2. **Parsing** - Analyzing the HTML structure to find specific data
3. **Extracting** - Pulling out the desired information
4. **Structuring** - Organizing the data into a useful format (like JSON)

### The Web Scraping Pipeline

```
URL → HTTP Request → HTML Response → Parse HTML → Extract Data → Structure Output
```

## HTTP Requests

### What are HTTP Requests?

HTTP (HyperText Transfer Protocol) requests are how programs communicate with web servers. When you visit a website, your browser sends an HTTP request to the server, which responds with the HTML content.

### Key Components of HTTP Requests

1. **Method**: Usually GET for retrieving data
2. **URL**: The address of the resource
3. **Headers**: Metadata about the request (User-Agent, Accept types, etc.)
4. **Response**: The server's reply containing status code and content

### Example from BaseParser

```python
def make_request(self, urls: List[str]) -> Tuple[List[str], List[str]]:
    """Shared request functionality for all parsers"""
    responses = []
    successful_urls = []
    
    for url in urls:
        try:
            print(f"Requesting: {url}")
            response = requests.get(url, timeout=5)  # HTTP GET request
            response.raise_for_status()  # Check for HTTP errors
            responses.append(response.text)  # Store HTML content
            successful_urls.append(url)
        except requests.exceptions.RequestException:
            print(f"Skipping URL due to error: {url}")
            continue
```

### Common HTTP Status Codes
- **200**: Success - the page loaded correctly
- **404**: Not Found - the page doesn't exist
- **403**: Forbidden - access denied
- **500**: Server Error - problem on the website's end

## HTML Parsing

### Understanding HTML Structure

HTML (HyperText Markup Language) is the standard markup language for web pages. It uses a tree-like structure of nested elements:

```html
<html>
  <body>
    <div class="article">
      <h1>Article Title</h1>
      <p class="author">By John Doe</p>
      <div class="content">
        <p>First paragraph...</p>
        <p>Second paragraph...</p>
      </div>
    </div>
  </body>
</html>
```

### The Document Object Model (DOM)

The DOM represents HTML as a tree structure where:
- Each HTML tag is a **node**
- Nodes can have **attributes** (class, id, href)
- Nodes can contain **text** or other nodes
- Nodes have **parent-child relationships**

### Parsing Strategy

1. **Identify patterns**: Find consistent HTML structures
2. **Use selectors**: Target specific elements by tag, class, or ID
3. **Navigate relationships**: Move between parent/child/sibling elements
4. **Extract data**: Get text content or attribute values

## Beautiful Soup

### What is Beautiful Soup?

Beautiful Soup is a Python library designed for parsing HTML and XML documents. It creates a parse tree from page source code that can be used to extract data in a more Pythonic way.

### Key Features

1. **Automatic encoding detection**: Handles different character encodings
2. **Lenient parsing**: Works with poorly formatted HTML
3. **Powerful searching**: Find elements using various methods
4. **Tree navigation**: Move through the document structure easily

### Beautiful Soup Methods

#### Finding Elements

```python
# Find single elements
soup.find('tag')                    # First occurrence of tag
soup.find('tag', class_='classname') # First tag with specific class
soup.find('tag', {'attribute': 'value'}) # First tag with attribute

# Find multiple elements
soup.find_all('tag')                # All occurrences of tag
soup.find_all(['tag1', 'tag2'])    # All occurrences of multiple tags
```

#### Extracting Data

```python
# Get text content
element.text          # All text including nested elements
element.get_text()    # Same as .text but with options
element.string        # Direct text only (no nested elements)

# Get attributes
element.get('href')   # Get specific attribute
element['class']      # Get class attribute (returns list)
element.attrs         # Get all attributes as dictionary
```

### Real Examples from OPAL Parsers

#### Parser1819 - News Article Extraction

```python
def parse_article(self, html: str, url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title from <title> tag
    title_tag = soup.title
    if title_tag:
        article['title'] = title_tag.string.strip()
    
    # Extract author from specific div structure
    author_date_div = soup.find('div', class_='author-date')
    if author_date_div:
        author_link = author_date_div.find('a')
        if author_link:
            article['author'] = author_link.text.strip()
    
    # Extract all paragraphs
    paragraphs = soup.find_all(['p'])
    for p in paragraphs:
        text = p.get_text().strip()
        # Process paragraph text...
```

#### ParserAppealsAL - Table Data Extraction

```python
def parse_table_row(self, row) -> Optional[Dict]:
    cells = row.find_all('td')  # Find all table cells
    if len(cells) < 6:
        return None
    
    # Extract text from specific cells
    court = cells[0].get_text(strip=True)
    
    # Extract both text and link from anchor tag
    case_number_elem = cells[1].find('a')
    if case_number_elem:
        case_number = {
            "text": case_number_elem.get_text(strip=True),
            "link": case_number_elem.get('href', '')
        }
```

## BaseParser Architecture

### Abstract Base Class Design

BaseParser uses Python's ABC (Abstract Base Class) to define a contract that all parsers must follow:

```python
from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Base class defining the interface for all parsers"""
    
    @abstractmethod
    def parse_article(self, html: str, url: str) -> Dict[str, Any]:
        """Each parser must implement this method"""
        pass
```

### Why Use Abstract Base Classes?

1. **Consistency**: Ensures all parsers have required methods
2. **Polymorphism**: Different parsers can be used interchangeably
3. **Documentation**: Clear contract for what parsers must implement
4. **Error Prevention**: Catches missing implementations at instantiation

### BaseParser Methods

#### make_request()
- **Purpose**: Fetch HTML content from URLs
- **Input**: List of URLs
- **Output**: HTML content and successful URLs
- **Error Handling**: Continues on failure, reports errors


#### parse_article() (abstract)
- **Purpose**: Extract data from single HTML page
- **Input**: HTML content and URL
- **Output**: Dictionary of extracted data
- **Implementation**: Must be defined by each parser subclass


#### parse_articles()
- **Purpose**: Coordinate parsing of multiple URLs
- **Input**: List of URLs
- **Output**: JSON string of all parsed data
- **Process**: Fetches HTML, calls parse_article(), combines results


## Implementation Examples

### Creating a New Parser

```python
from opal.parser_module import BaseParser
from bs4 import BeautifulSoup

class MyNewsParser(BaseParser):
    """Custom parser for a specific news site"""
    
    def parse_article(self, html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Initialize data structure
        article = {
            'url': url,
            'title': '',
            'author': '',
            'date': '',
            'content': []
        }
        
        # Extract title
        title_element = soup.find('h1', class_='article-title') #These classes are website specific
        if title_element:
            article['title'] = title_elem.get_text(strip=True)
        
        # Extract author
        author_element = soup.find('span', class_='byline')
        if author_element:
            article['author'] = author_elem.get_text(strip=True)
        
        # Extract content paragraphs
        content_div = soup.find('div', class_='article-body')
        if content_div:
            paragraphs = content_div.find_all('p')
            article['content'] = [p.get_text(strip=True) for p in paragraphs]
        
        return article
```

### Handling Complex HTML Structures

Sometimes data is nested or spread across multiple elements:

```python
# Handle nested structures
article_div = soup.find('div', class_='article')
if article_div:
    # Navigate to nested elements
    header = article_div.find('header')
    if header:
        title = header.find('h1')
        meta = header.find('div', class_='meta')
        
    # Find siblings
    content = article_div.find_next_sibling('div', class_='content')
```

### Error Handling Best Practices

```python
def parse_article(self, html: str, url: str) -> Dict[str, Any]:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        article = {'url': url}
        
        # Always check if elements exist
        title_elem = soup.find('h1')
        if title_elem:
            article['title'] = title_elem.get_text(strip=True)
        else:
            article['title'] = 'No title found'
            
        # Handle missing attributes safely
        link_elem = soup.find('a', class_='author-link')
        if link_elem:
            article['author_url'] = link_elem.get('href', '')
            
        return article
        
    except Exception as e:
        # Return partial data rather than failing completely
        return {
            'url': url,
            'error': str(e),
            'partial_data': True
        }
```

## Best Practices

### 1. Respect Website Policies
- Check robots.txt (example: https://1819news.com/robots.txt)
- Add delays between requests
- Use appropriate User-Agent headers
- Don't overwhelm servers

### 2. Handle Errors Gracefully
- Expect missing elements
- Provide default values
- Log errors for debugging
- Continue processing other data

### 3. Write Maintainable Code
- Use descriptive variable names
- Comment complex selections
- Create reusable helper functions
- Test with various page structures

### 4. Optimize Performance
- Reuse parser instances
- Batch process URLs
- Cache results when appropriate
- Close resources properly

### 5. Structure Data Consistently
- Use consistent field names
- Provide empty defaults
- Validate data types
- Document output format

## Common Challenges and Solutions

### Dynamic Content
**Problem**: Content loaded by JavaScript isn't in initial HTML
**Solution**: Use Selenium (like ParserAppealsAL) for JavaScript rendering

### Changing HTML Structure
**Problem**: Website updates break selectors
**Solution**: Use multiple fallback selectors, test regularly

### Rate Limiting
**Problem**: Too many requests trigger blocking
**Solution**: Add delays, rotate User-Agents, respect rate limits

### Encoding Issues
**Problem**: Special characters appear corrupted
**Solution**: Beautiful Soup handles most encoding automatically

## Conclusion

The BaseParser provides a robust foundation for web scraping by:
- Standardizing the parsing interface
- Handling HTTP requests with error recovery
- Leveraging Beautiful Soup for HTML parsing
- Supporting both simple and complex extraction needs

Whether scraping news articles or court records, understanding these fundamentals enables you to create effective parsers that extract structured data from any website.