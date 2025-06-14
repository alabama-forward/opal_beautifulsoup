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
from opal.configurable_court_extractor import ConfigurableCourtExtractor
from opal.parser_appeals_al import ParserAppealsAL

# The configurable extractor uses ParserAppealsAL internally
extractor = ConfigurableCourtExtractor(
    court_type="civil",
    search_parameters={...}
)

# Access the underlying parser
parser = extractor.parser  # This is a ParserAppealsAL instance
```

### With Court URL Paginator

```python
from opal.court_url_paginator import paginate_court_urls
from opal.parser_appeals_al import ParserAppealsAL

parser = ParserAppealsAL()
driver = parser.setup_driver()

# Get all page URLs
page_urls = paginate_court_urls(search_url)

# Process each page
for url in page_urls:
    driver.get(url)
    cases = parser._extract_cases_from_page(driver)
```

### With Integrated Parser

```python
from opal.integrated_parser import IntegratedParser

# Automatically detects court URLs and uses ParserAppealsAL
integrated = IntegratedParser()
result = integrated.parse_url("https://publiccourts.alacourt.gov/...")

if result['parser_type'] == 'court':
    court_cases = result['data']['cases']
```

## Advanced Usage

### Custom Chrome Options

```python
from selenium import webdriver
from opal.parser_appeals_al import ParserAppealsAL

# Create custom Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=proxy.example.com:8080')
chrome_options.add_argument('--user-agent=Custom User Agent')

# Use with parser
parser = ParserAppealsAL()
parser.chrome_options = chrome_options
```

### Error Handling Integration

```python
from opal.parser_appeals_al import ParserAppealsAL
import logging

logging.basicConfig(level=logging.DEBUG)

parser = ParserAppealsAL(
    headless=False,  # For debugging
    rate_limit_seconds=2.0  # Slower for observation
)

try:
    cases = parser.extract_court_data()
except Exception as e:
    logging.error(f"Extraction failed: {e}")
    # Handle error appropriately
```

## Notes

- Requires Chrome browser installed
- Uses Selenium for JavaScript support
- Handles pagination automatically
- Extracts both case list and detailed case information
- Includes comprehensive error handling for web automation
- Integrates with all other OPAL components
- Supports extensive customization through configuration