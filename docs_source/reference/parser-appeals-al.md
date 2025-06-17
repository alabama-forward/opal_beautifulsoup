---
layout: default
title: "ParserAppealsAL API Reference"
---

# ParserAppealsAL API Reference

Parser for [Alabama Appeals Court Public Portal](https://publicportal.alappeals.gov/).

## Class Definition

```python
class ParserAppealsAL(BaseParser):
    def __init__(self, url="https://publicportal.alappeals.gov/portal/search/case/results")
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | Portal URL | Base URL for court portal |
| `headless` | bool | True | Run browser in headless mode |
| `rate_limit_seconds` | float | 1.0 | Delay between requests |

## Methods

### setup_driver()
```python
def setup_driver(self) -> webdriver.Chrome
```
Sets up Chrome WebDriver with appropriate options.

**Returns**: Configured Chrome WebDriver instance

### extract_court_data()
```python
def extract_court_data(self) -> List[Dict]
```
Main method to extract court case data.

**Returns**: List of court case dictionaries

### parse_case_row()
```python
def parse_case_row(self, row: WebElement) -> Dict
```
Parses individual case row from search results.

**Parameters**:
- `row`: Selenium WebElement representing a case row

**Returns**: Dictionary with case information

### get_case_details()
```python
def get_case_details(self, case_url: str) -> Dict
```
Fetches detailed information for a specific case.

**Parameters**:
- `case_url`: URL to the case details page

**Returns**: Dictionary with detailed case information

## Usage Example

```python
from opal.ParserAppealsAL import ParserAppealsAL

# Create parser instance
parser = ParserAppealsAL()

# Extract court cases
cases = parser.extract_court_data()

# Save to JSON
parser.save_to_json(cases, "court_cases.json")

# Process cases
for case in cases:
    print(f"Case: {case['case_number']}")
    print(f"Title: {case['case_title']}")
    print(f"Status: {case['status']}")
```

## Output Format

```json
{
  "case_number": "2024-CV-001234",
  "case_title": "State of Alabama v. John Doe",
  "court": "Alabama Court of Civil Appeals",
  "date_filed": "2024-01-10",
  "status": "Active",
  "judge": "Hon. Jane Smith",
  "parties": {
    "appellant": "John Doe",
    "appellee": "State of Alabama"
  },
  "attorneys": [
    {
      "name": "James Johnson",
      "role": "Attorney for Appellant"
    }
  ],
  "docket_entries": [
    {
      "date": "2024-01-10",
      "description": "Notice of Appeal Filed",
      "document_url": "https://publicportal.alappeals.gov/document/12345"
    }
  ]
}
```

## Special Features

### Selenium WebDriver
- Automatically installs ChromeDriver
- Handles JavaScript-rendered content
- Supports dynamic page interactions

### Error Handling
- Retries failed page loads
- Handles stale element exceptions
- Logs detailed error information

### Rate Limiting
- Includes delays between requests
- Respects server load

## Integration with Other Components

### With Configurable Court Extractor

```python
from opal.configurable_court_extractor import extract_court_cases_with_params
from opal.court_case_parser import ParserAppealsAL

# The configurable extractor uses ParserAppealsAL internally
results = extract_court_cases_with_params(
    court="civil",
    date_period="1m",
    max_pages=5
)

# Direct parser usage
parser = ParserAppealsAL(headless=True, rate_limit_seconds=2)
result = parser.parse_article(url)
```

### With Court URL Paginator

```python
from opal.court_url_paginator import paginate_court_urls
from opal.court_case_parser import ParserAppealsAL

parser = ParserAppealsAL()

# Get all page URLs (requires parser for dynamic page detection)
page_urls = paginate_court_urls(search_url, parser)

# Process each page
all_cases = []
for url in page_urls:
    result = parser.parse_article(url)
    if 'cases' in result:
        all_cases.extend(result['cases'])

parser._close_driver()
```

### With Integrated Parser

```python
from opal.integrated_parser import IntegratedParser
from opal.court_case_parser import ParserAppealsAL

# Integrated parser requires parser class as parameter
integrated = IntegratedParser(ParserAppealsAL)
result = integrated.process_site("https://publicportal.alappeals.gov/...")

# Result contains processed data
if result:
    data = json.loads(result)
```

## Advanced Usage

### Custom Chrome Options

```python
from selenium import webdriver
from opal.court_case_parser import ParserAppealsAL

# Note: Chrome options are set in the _setup_driver method
# To customize, you would need to modify the parser's _setup_driver method
parser = ParserAppealsAL(headless=False)  # Run with visible browser
```

### Error Handling Integration

```python
from opal.court_case_parser import ParserAppealsAL
import logging

logging.basicConfig(level=logging.DEBUG)

parser = ParserAppealsAL(
    headless=False,  # For debugging
    rate_limit_seconds=2  # Slower for observation (int, not float)
)

try:
    result = parser.parse_article(url)
    cases = result.get('cases', [])
except Exception as e:
    logging.error(f"Extraction failed: {e}")
    # Handle error appropriately
finally:
    parser._close_driver()
```

## Notes

- Requires Chrome browser installed
- Uses Selenium for JavaScript support
- Handles pagination automatically
- Extracts both case list and detailed case information
- Includes comprehensive error handling for web automation
- Integrates with all other OPAL components
- Supports extensive customization through configuration