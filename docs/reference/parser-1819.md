# Parser1819 API Reference

Parser for [1819 News](https://1819news.com/) website.

## Class Definition

```python
class Parser1819(BaseParser):
    def __init__(self, url="https://1819news.com/", suffix="/news/item", max_pages=5)
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | `"https://1819news.com/"` | Base URL for 1819 News |
| `suffix` | str | `"/news/item"` | URL suffix for article links |
| `max_pages` | int | `5` | Maximum pages to scrape |

## Methods

### extract_article_data()
```python
def extract_article_data(self) -> List[Dict]
```
Extracts articles from multiple pages of 1819 News.

**Returns**: List of article dictionaries with keys:
- `title`: Article headline
- `content`: Full article text
- `date`: Publication date
- `author`: Article author
- `url`: Article URL
- `tags`: List of article tags

### get_article_links()
```python
def get_article_links(self, page_url: str) -> List[str]
```
Extracts article URLs from a 1819 News page.

**Parameters**:
- `page_url`: URL of the page to scrape

**Returns**: List of article URLs matching the suffix pattern

### parse_article()
```python
def parse_article(self, article_url: str) -> Dict
```
Parses individual 1819 News article.

**Parameters**:
- `article_url`: URL of the article

**Returns**: Dictionary with article data

## Usage Example

```python
from opal.Parser1819 import Parser1819

# Create parser instance
parser = Parser1819(
    url="https://1819news.com/",
    suffix="/news/item",
    max_pages=10
)

# Extract articles
articles = parser.extract_article_data()

# Save to JSON
parser.save_to_json(articles, "1819_news_articles.json")

# Access article data
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Date: {article['date']}")
    print(f"Author: {article['author']}")
```

## Output Format

```json
{
  "title": "Alabama Legislature Passes New Education Bill",
  "content": "Full article text...",
  "date": "2024-01-15",
  "author": "John Smith",
  "url": "https://1819news.com/news/item/education-bill-2024",
  "tags": ["education", "legislature", "alabama"]
}
```

## Notes

- Uses BeautifulSoup for HTML parsing
- Handles pagination automatically
- Filters links by suffix to ensure only articles are scraped
- Includes error handling for missing elements