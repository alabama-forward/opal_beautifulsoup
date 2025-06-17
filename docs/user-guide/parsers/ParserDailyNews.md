---
title: Alabama Daily News Parser (ParserDailyNews)
description: Guide to using the ParserDailyNews for scraping Alabama Daily News articles
---

[Home](/) > [User Guide](/user-guide/) > [Parsers](/user-guide/parsers/) > Alabama Daily News Parser

# Alabama Daily News Parser (ParserDailyNews)

<span class="parser-badge">ParserDailyNews</span>

The Alabama Daily News Parser (`ParserDailyNews`) is designed to extract articles from Alabama Daily News and similar news websites with compatible HTML structures.

!!! abstract "Overview"
    This parser is optimized for Alabama Daily News website structure, extracting articles with specific HTML class patterns for author and date information.

## Prerequisites

- OPAL installed and configured
- Internet connection
- Basic command-line knowledge

## Basic Usage

### Simple Extraction
```bash
# Extract articles from Alabama Daily News
python -m opal --url "https://alabamadailynews.com/" --parser ParserDailyNews

# With pagination limit
python -m opal --url "https://alabamadailynews.com/" --parser ParserDailyNews --max_pages 5

# With URL suffix filter
python -m opal --url "https://alabamadailynews.com/" --parser ParserDailyNews --suffix "/news/"
```

### Command Line Arguments
```bash
# Required arguments
--url        # Base URL of the news site
--parser     # Must be "ParserDailyNews"

# Optional arguments
--suffix     # URL suffix to filter article pages
--max_pages  # Maximum number of pages to process
```

## Features

### Specialized Content Extraction
The parser looks for specific HTML patterns:
- Author in `<span class="author vcard">`
- Date in `<span class="post-date">`
- Article paragraphs in `<p>` tags

### Robust Error Handling
- Provides default values for missing metadata
- Continues processing if individual articles fail
- Handles various date formats

## Data Fields Extracted

| Field | Description | Example |
|-------|-------------|---------|
| url | Article URL | "https://alabamadailynews.com/news/..." |
| title | Article title | "Governor Signs New Legislation" |
| author | Article author | "Staff Writer" or "Unknown Author" |
| date | Publication date | "March 15, 2024" or "Unknown Date" |
| line_count | Number of text lines | 28 |
| line_content | Article text by line | {"line 1": "Text...", ...} |

## Output Format

### JSON Structure
```json
{
  "success": true,
  "total_articles": 15,
  "timestamp": "2024-03-15T10:30:45",
  "site_info": {
    "base_url": "https://alabamadailynews.com/",
    "pages_processed": 3
  },
  "articles": [
    {
      "url": "https://alabamadailynews.com/news/state-budget-update",
      "title": "State Budget Negotiations Continue",
      "author": "Political Reporter",
      "date": "March 14, 2024",
      "line_count": 24,
      "line_content": {
        "line 1": "Budget negotiations in Montgomery...",
        "line 2": "Legislative leaders met today...",
        "line 3": "The proposed budget includes..."
      }
    }
  ]
}
```

## Advanced Usage

### Section-Specific Scraping
```bash
# Politics section only
python -m opal --url "https://alabamadailynews.com/politics/" --parser ParserDailyNews

# Business news
python -m opal --url "https://alabamadailynews.com/business/" --parser ParserDailyNews
```

### Custom Integration
```python
from opal.parser_module import ParserDailyNews
from opal.integrated_parser import IntegratedParser

# Create parser instance
daily_parser = IntegratedParser(ParserDailyNews)

# Process specific section
results = daily_parser.process_site(
    base_url="https://alabamadailynews.com/politics/",
    suffix="/2024/",  # Only 2024 articles
    max_pages=5
)
```

## Parser-Specific Behavior

### HTML Class Detection
The parser specifically looks for:
```html
<!-- Author -->
<span class="author vcard">
    <a href="/author/...">Author Name</a>
</span>

<!-- Date -->
<span class="post-date">
    <a href="/2024/03/15/">March 15, 2024</a>
</span>

<!-- Content -->
<p>Article paragraph text...</p>
```

### Fallback Behavior
- If author span not found: Returns "Unknown Author"
- If date span not found: Returns "Unknown Date"
- If no paragraphs found: Returns empty content

## Common Use Cases

### Daily News Archive
```bash
#!/bin/bash
# Archive daily news
DATE=$(date +%Y-%m-%d)
python -m opal \
    --url "https://alabamadailynews.com/" \
    --parser ParserDailyNews \
    --max_pages 2

# Move to archive
mkdir -p archives
mv "${DATE}_ParserDailyNews.json" "archives/"
```

### Author Statistics
```python
import json
from collections import defaultdict

# Load data
with open('2024-03-15_ParserDailyNews.json', 'r') as f:
    data = json.load(f)

# Analyze authors
author_stats = defaultdict(int)
for article in data['articles']:
    if article['author'] != 'Unknown Author':
        author_stats[article['author']] += 1

# Display results
for author, count in sorted(author_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"{author}: {count} articles")
```

### Content Analysis
```python
# Analyze article lengths
lengths = []
for article in data['articles']:
    lengths.append(article['line_count'])

avg_length = sum(lengths) / len(lengths)
print(f"Average article length: {avg_length:.1f} lines")
print(f"Shortest: {min(lengths)} lines")
print(f"Longest: {max(lengths)} lines")
```

## Troubleshooting

### Common Issues

**No Author/Date Found**
- Website may have changed HTML structure
- Check for different class names
- View page source to verify structure

**Empty Articles**
```bash
# Debug HTML structure
curl -s "https://alabamadailynews.com/sample-article" | \
    grep -E "(author vcard|post-date|<p>)" | head -20
```

**Slow Performance**
- Reduce `--max_pages`
- Process during off-peak hours
- Check network connectivity

### Debugging Tips
1. Start with `--max_pages 1` to test
2. Check output for "Unknown" values
3. Verify URL patterns match expectations
4. Use browser developer tools to inspect HTML

## Performance Considerations

1. **Request Rate**: Automatic delays between requests
2. **Memory Usage**: Line-by-line storage can use significant memory for long articles
3. **Network Timeouts**: 5-second timeout per request
4. **Error Recovery**: Failed URLs are skipped, not retried

## Extending the Parser

### Adapting for Similar Sites
The ParserDailyNews can work with sites that use similar HTML structures:

```python
# Sites with compatible structure:
compatible_sites = [
    "https://alabamadailynews.com/",
    "https://similar-news-site.com/",
    # Add sites with matching HTML classes
]
```

### Custom Modifications
See [Creating Custom Parsers](../../developer/creating-custom-parsers.md) for guidance on adapting this parser for other news sites.

## Related Topics

- [Parser Overview](./index.md)
- [Alabama Appeals Court Parser](./ParserAppealsAL.md)
- [1819 News Parser](./Parser1819.md)
- [Working with Output Data](../working-with-output-data.md)

## Next Steps

- Explore [Output Examples](../output-examples.md)
- Learn about [Common Use Cases](../common-use-cases.md)
- Try [Creating Custom Parsers](../../developer/creating-custom-parsers.md)