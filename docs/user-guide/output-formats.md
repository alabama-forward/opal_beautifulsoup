# Output Formats

OPAL outputs scraped data in structured JSON format for easy analysis and processing.

## JSON Structure

### News Articles

```json
{
  "results": [
    {
      "title": "Article headline",
      "content": "Full article text...",
      "date": "2024-01-15",
      "author": "John Doe",
      "url": "https://example.com/article-url",
      "tags": ["politics", "alabama"],
      "image_url": "https://example.com/image.jpg"
    }
  ],
  "metadata": {
    "source": "Parser1819",
    "base_url": "https://1819news.com/",
    "scraped_at": "2024-01-15T10:30:00Z",
    "total_items": 50,
    "pages_scraped": 5
  }
}
```

### Court Cases

```json
{
  "results": [
    {
      "case_number": "2024-CV-001234",
      "case_title": "State v. Defendant",
      "court": "Alabama Court of Civil Appeals",
      "date_filed": "2024-01-10",
      "status": "Active",
      "parties": {
        "plaintiff": "State of Alabama",
        "defendant": "John Doe"
      },
      "docket_entries": [
        {
          "date": "2024-01-10",
          "description": "Case filed",
          "document_url": "https://example.com/doc.pdf"
        }
      ]
    }
  ],
  "metadata": {
    "source": "ParserAppealsAL",
    "scraped_at": "2024-01-15T10:30:00Z",
    "total_cases": 25
  }
}
```

## Working with Output

### Python Example

```python
import json

# Load scraped data
with open('opal_output.json', 'r') as f:
    data = json.load(f)

# Access articles
for article in data['results']:
    print(f"Title: {article['title']}")
    print(f"Date: {article['date']}")
    print(f"URL: {article['url']}")
    print("---")

# Get metadata
print(f"Total items: {data['metadata']['total_items']}")
```

### Data Analysis

The JSON output can be easily imported into:
- Pandas DataFrames for analysis
- Excel/CSV for spreadsheet work
- Database systems for storage
- Visualization tools for insights

## Error Handling

Failed scrapes include error information:

```json
{
  "results": [],
  "metadata": {
    "source": "Parser1819",
    "error": "Connection timeout",
    "scraped_at": "2024-01-15T10:30:00Z"
  }
}
```