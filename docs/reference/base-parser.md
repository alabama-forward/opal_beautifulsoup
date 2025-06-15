# BaseParser API Reference

The `BaseParser` class provides the foundation for all OPAL parsers.

## Class Definition

```python
class BaseParser:
    def __init__(self, url, suffix="", max_pages=5)
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | Base URL to scrape |
| `suffix` | str | `""` | URL suffix for article links |
| `max_pages` | int | `5` | Maximum pages to scrape |

## Attributes

### headers
```python
self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```
HTTP headers for requests

### logger
```python
self.logger: logging.Logger
```
Logger instance for debugging

## Methods

### extract_article_data()
```python
def extract_article_data(self) -> List[Dict]
```
Main method to extract articles. Must be implemented by subclasses.

**Returns**: List of dictionaries containing article data

### get_article_links()
```python
def get_article_links(self, page_url: str) -> List[str]
```
Extract article URLs from a page. Must be implemented by subclasses.

**Parameters**:
- `page_url`: URL of the page to extract links from

**Returns**: List of article URLs

### parse_article()
```python
def parse_article(self, article_url: str) -> Dict
```
Parse individual article data. Must be implemented by subclasses.

**Parameters**:
- `article_url`: URL of the article to parse

**Returns**: Dictionary with article data

### save_to_json()
```python
def save_to_json(self, data: List[Dict], filename: str = "opal_output.json")
```
Save extracted data to JSON file.

**Parameters**:
- `data`: List of article dictionaries
- `filename`: Output filename

## Usage Example

```python
from opal.BaseParser import BaseParser

class MyParser(BaseParser):
    def __init__(self, url, suffix="", max_pages=5):
        super().__init__(url, suffix, max_pages)
        self.name = "MyParser"
    
    def extract_article_data(self):
        # Implementation
        pass
    
    def get_article_links(self, page_url):
        # Implementation
        pass
    
    def parse_article(self, article_url):
        # Implementation
        pass

# Use the parser
parser = MyParser("https://example.com", suffix="/articles", max_pages=10)
data = parser.extract_article_data()
parser.save_to_json(data)
```