# ParserDailyNews API Reference

Parser for [Alabama Daily News](https://www.aldailynews.com/) website.

## Class Definition

```python
class ParserDailyNews(BaseParser):
    def __init__(self, url="https://www.aldailynews.com/", suffix="/news/item", max_pages=5)
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | `"https://www.aldailynews.com/"` | Base URL for Alabama Daily News |
| `suffix` | str | `"/news/item"` | URL suffix for article links |
| `max_pages` | int | `5` | Maximum pages to scrape |

## Methods

### extract_article_data()
```python
def extract_article_data(self) -> List[Dict]
```
Extracts articles from Alabama Daily News.

**Returns**: List of article dictionaries with keys:
- `title`: Article headline
- `content`: Full article text
- `date`: Publication date
- `author`: Article author
- `url`: Article URL
- `category`: Article category

### get_article_links()
```python
def get_article_links(self, page_url: str) -> List[str]
```
Extracts article URLs from an Alabama Daily News page.

**Parameters**:
- `page_url`: URL of the page to scrape

**Returns**: List of article URLs

### parse_article()
```python
def parse_article(self, article_url: str) -> Dict
```
Parses individual Alabama Daily News article.

**Parameters**:
- `article_url`: URL of the article

**Returns**: Dictionary with article data

## Usage Example

```python
from opal.ParserDailyNews import ParserDailyNews

# Create parser instance
parser = ParserDailyNews(
    url="https://www.aldailynews.com/",
    suffix="/news/item",
    max_pages=5
)

# Extract articles
articles = parser.extract_article_data()

# Save to JSON
parser.save_to_json(articles, "adn_articles.json")

# Process articles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Category: {article['category']}")
    print(f"Date: {article['date']}")
```

## Output Format

```json
{
  "title": "Governor Announces Infrastructure Plan",
  "content": "Full article text...",
  "date": "2024-01-15",
  "author": "Jane Doe",
  "url": "https://www.aldailynews.com/news/item/infrastructure-plan",
  "category": "Politics"
}
```

## Notes

- Handles Alabama Daily News specific HTML structure
- Extracts category information when available
- Supports pagination through page parameters
- Includes robust error handling for missing elements