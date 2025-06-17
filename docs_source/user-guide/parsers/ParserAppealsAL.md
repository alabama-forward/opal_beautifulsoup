---
title: Alabama Appeals Court Parser (ParserAppealsAL)
description: Complete guide to using the ParserAppealsAL parser for scraping Alabama appellate court decisions
---

[Home](../../index.md) > [User Guide](../index.md) > [Parsers](./index.md) > Alabama Appeals Court Parser

# Alabama Appeals Court Parser (ParserAppealsAL)

<span class="parser-badge">ParserAppealsAL</span>

The Alabama Appeals Court Parser (`ParserAppealsAL`) is OPAL's specialized parser for extracting court case data from the Alabama Appeals Court Public Portal.

!!! abstract "Overview"
    This parser uses Selenium to handle JavaScript-rendered content on the Alabama Appeals Court website, extracting comprehensive case data including case numbers, titles, filing dates, and case status.

## Prerequisites

- OPAL installed and configured
- Chrome/Chromium browser installed
- Internet connection
- Basic understanding of command-line tools

## Basic Usage

### Simple Extraction
```bash
# Extract court cases from Alabama Appeals Court
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL

# With max pages limit
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL --max_pages 5
```

### Command Line Arguments
```bash
# Required arguments
--url        # Base URL of the court website
--parser     # Must be "ParserAppealsAL"

# Optional arguments
--max_pages  # Maximum number of pages to scrape
--suffix     # URL suffix (not typically used for court parser)
```

## Features

### JavaScript Rendering
The parser uses Selenium WebDriver to:
- Handle dynamic JavaScript content
- Navigate through court portal pages
- Extract data from rendered tables
- Handle pagination automatically

### Rate Limiting
- Built-in rate limiting (3 seconds default between requests)
- Prevents overwhelming the court website
- Configurable through parser initialization

### Headless Mode
- Runs in headless mode by default (no browser window)
- Can be configured to show browser for debugging

## Data Fields Extracted

The parser extracts the following information for each case:

| Field | Description | Example |
|-------|-------------|---------|
| court | Court name | "01-AUTAUGA" |
| case_number | Case number with link | {"text": "01-CC-1983-000002.00", "link": "url"} |
| case_title | Full case title | "JOHN DOE VS JANE DOE" |
| filed_date | Date case was filed | "06/28/1985" |
| status | Current case status | "CLOSED" |
| case_url | Direct link to case | Full URL to case details |

## Output Format

### JSON Structure
```json
{
  "status": "success",
  "timestamp": "2024-03-15T10:30:45",
  "total_cases": 150,
  "page_info": {
    "current_page": 1,
    "total_pages": 3,
    "results_per_page": 50
  },
  "cases": [
    {
      "court": "01-AUTAUGA",
      "case_number": {
        "text": "01-CC-1983-000002.00",
        "link": "https://v2.alacourt.com/frmCaseDetail.aspx?caseID=..."
      },
      "case_title": "JOHN DOE VS JANE DOE",
      "filed_date": "06/28/1985",
      "status": "CLOSED",
      "case_url": "https://v2.alacourt.com/frmCaseDetail.aspx?caseID=..."
    }
  ]
}
```

## Advanced Usage

### Processing Multiple Pages
```bash
# Process first 10 pages
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL --max_pages 10

# Process all available pages (use with caution)
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL
```

### Integration with Scripts
```python
from opal.court_case_parser import ParserAppealsAL
from opal.integrated_parser import IntegratedParser

# Create parser instance
court_parser = IntegratedParser(ParserAppealsAL)

# Process court website
results = court_parser.process_site(
    base_url="https://publicportal.alacourt.gov",
    max_pages=5
)

# Parse results
import json
data = json.loads(results)
print(f"Found {data['total_cases']} cases")
```

## Common Use Cases

### Daily Court Updates
```bash
# Daily scrape with date in filename
DATE=$(date +%Y-%m-%d)
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL --max_pages 3
# Output saved as: YYYY-MM-DD_ParserAppealsAL.json
```

### Specific Court Monitoring
Since the parser extracts court information, you can filter results post-processing:
```python
# Filter for specific court
import json

with open('2024-03-15_ParserAppealsAL.json', 'r') as f:
    data = json.load(f)

autauga_cases = [
    case for case in data['cases'] 
    if case['court'] == '01-AUTAUGA'
]
```

## Troubleshooting

### Common Issues

**Chrome Driver Issues**
- The parser automatically installs ChromeDriver using webdriver-manager
- Ensure Chrome/Chromium is installed on your system
- Check Chrome version compatibility

**Timeout Errors**
- Court website may be slow to respond
- Parser includes WebDriverWait for dynamic content
- Default timeout is 10 seconds

**No Data Found**
- Verify the URL is correct
- Check if the court website structure has changed
- Enable non-headless mode for debugging

### Debug Mode
```python
# Run with visible browser for debugging
from opal.court_case_parser import ParserAppealsAL

parser = ParserAppealsAL(headless=False)
```

## Performance Considerations

1. **Rate Limiting**: Default 3-second delay between page requests
2. **Memory Usage**: Selenium requires more memory than simple HTTP requests
3. **Processing Time**: Each page takes 10-15 seconds to fully load and parse
4. **Recommended Limits**: Use `--max_pages` to limit scope

## Error Handling

The parser includes robust error handling for:
- Network timeouts
- Missing elements on page
- Invalid page structures
- Browser crashes

Failed pages are logged but don't stop the entire process.

## Related Topics

- [Parser Overview](./index.md)
- [1819 News Parser](./Parser1819.md)
- [Daily News Parser](./ParserDailyNews.md)
- [Working with Output Data](../working-with-output-data.md)

## Next Steps

- Try the [Parser1819](./Parser1819.md) for news coverage
- Learn about [Creating Custom Parsers](../../developer/creating-custom-parsers.md)
- Explore [Common Use Cases](../common-use-cases.md)