---
title: 1819 News Parser (Parser1819)
description: Guide to using the Parser1819 for scraping articles from 1819 News
---

[Home](/) > [User Guide](/user-guide/) > [Parsers](/user-guide/parsers/) > 1819 News Parser

# 1819 News Parser (Parser1819)

<span class="parser-badge">Parser1819</span>

The 1819 News Parser (`Parser1819`) is designed to extract articles from the 1819 News website, focusing on Alabama political and legal news coverage.

!!! abstract "Overview"
    This parser extracts article content, metadata, and structure from 1819 News, providing comprehensive data for analysis of Alabama news coverage.

## Prerequisites

- OPAL installed and configured
- Internet connection
- Basic command-line knowledge

## Basic Usage

### Simple Extraction
```bash
# Extract articles from 1819 News
python -m opal --url "https://1819news.com/" --parser Parser1819

# With pagination limit
python -m opal --url "https://1819news.com/" --parser Parser1819 --max_pages 5

# With URL suffix filter
python -m opal --url "https://1819news.com/" --parser Parser1819 --suffix "/news/item"
```

### Command Line Arguments
```bash
# Required arguments
--url        # Base URL (https://1819news.com/)
--parser     # Must be "Parser1819"

# Optional arguments
--suffix     # URL suffix to filter article pages
--max_pages  # Maximum number of pages to process
```

## Features

### Content Extraction
The parser extracts:
- Article title
- Author information
- Publication date
- Full article text (line by line)
- Article URL

### Structured Output
- Articles are parsed line by line
- Preserves paragraph structure
- Maintains text formatting
- Counts total lines for analysis

## Data Fields Extracted

| Field | Description | Example |
|-------|-------------|---------|
| url | Article URL | "https://1819news.com/news/item/..." |
| title | Article title | "Alabama Legislature Passes New Bill" |
| author | Article author | "John Smith" |
| date | Publication date | "March 15, 2024" |
| line_count | Number of text lines | 45 |
| line_content | Article text by line | {"line 1": "First paragraph...", ...} |

## Output Format

### JSON Structure
```json
{
  "success": true,
  "total_articles": 25,
  "timestamp": "2024-03-15T10:30:45",
  "site_info": {
    "base_url": "https://1819news.com/",
    "pages_processed": 5
  },
  "articles": [
    {
      "url": "https://1819news.com/news/item/example-article",
      "title": "Alabama Legislature Considers New Education Bill",
      "author": "Jane Doe",
      "date": "March 14, 2024",
      "line_count": 32,
      "line_content": {
        "line 1": "The Alabama Legislature is considering...",
        "line 2": "The bill, sponsored by Senator...",
        "line 3": "Education advocates say..."
      }
    }
  ]
}
```

## Advanced Usage

### Filtering by URL Pattern
```bash
# Only process articles with specific URL patterns
python -m opal --url "https://1819news.com/" --parser Parser1819 --suffix "/news/politics"

# Multiple patterns (in script)
python script_with_multiple_suffixes.py
```

### Processing Specific Sections
```python
from opal.parser_module import Parser1819
from opal.integrated_parser import IntegratedParser

# Create parser for specific section
news_parser = IntegratedParser(Parser1819)

# Process politics section
politics_articles = news_parser.process_site(
    base_url="https://1819news.com/news/politics/",
    max_pages=10
)
```

## Common Use Cases

### Daily News Monitoring
```bash
#!/bin/bash
# Daily news scrape
DATE=$(date +%Y-%m-%d)
python -m opal --url "https://1819news.com/" --parser Parser1819 --max_pages 3
echo "News saved to ${DATE}_Parser1819.json"
```

### Keyword Analysis
```python
import json

# Load parsed articles
with open('2024-03-15_Parser1819.json', 'r') as f:
    data = json.load(f)

# Search for keywords
keyword = "court"
matching_articles = []

for article in data['articles']:
    content = ' '.join(article['line_content'].values()).lower()
    if keyword in content:
        matching_articles.append(article)

print(f"Found {len(matching_articles)} articles mentioning '{keyword}'")
```

### Author Tracking
```python
# Track articles by specific authors
from collections import Counter

author_counts = Counter(
    article['author'] 
    for article in data['articles']
)

print("Articles by author:")
for author, count in author_counts.most_common():
    print(f"{author}: {count} articles")
```

## Parser-Specific Behavior

### HTML Structure Handling
- Looks for `div` with class `author-date` for metadata
- Extracts all `<p>` tags for article content
- Handles missing author/date gracefully

### Error Handling
- Returns "Unknown Author" if author not found
- Returns "Unknown Date" if date not found
- Continues processing even if some articles fail

## Troubleshooting

### Common Issues

**No Articles Found**
- Verify the base URL is correct
- Check if website structure has changed
- Ensure suffix parameter matches actual URLs

**Missing Metadata**
- Some articles may not have author information
- Date format may vary
- Parser provides defaults for missing data

**Incomplete Content**
- Check for JavaScript-rendered content
- Some articles may require authentication
- Verify network connectivity

### Debug Tips
```bash
# Run with verbose output
python -m opal --url "https://1819news.com/" --parser Parser1819 --max_pages 1

# Check specific article structure
curl -s "https://1819news.com/news/item/sample" | grep -E "(author-date|<p>)"
```

## Performance Optimization

1. **Use --max_pages**: Limit pages to process
2. **Filter with --suffix**: Reduce unnecessary requests
3. **Batch Processing**: Process sections separately
4. **Rate Limiting**: Built-in delays prevent blocking

## Integration Examples

### CSV Export
```python
import json
import csv

# Load JSON data
with open('2024-03-15_Parser1819.json', 'r') as f:
    data = json.load(f)

# Export to CSV
with open('articles.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'author', 'date', 'url'])
    writer.writeheader()
    
    for article in data['articles']:
        writer.writerow({
            'title': article['title'],
            'author': article['author'],
            'date': article['date'],
            'url': article['url']
        })
```

## Related Topics

- [Parser Overview](./index.md)
- [Alabama Appeals Court Parser](./ParserAppealsAL.md)
- [Daily News Parser](./ParserDailyNews.md)
- [Working with Output Data](../working-with-output-data.md)

## Next Steps

- Try the [ParserDailyNews](./ParserDailyNews.md) for other news sources
- Learn about [Creating Custom Parsers](../../developer/creating-custom-parsers.md)
- Explore [Output Examples](../output-examples.md)