# Creating Court Parsers with OPAL

## Overview

This guide explains how to create parsers for court websites using OPAL's framework. We'll use `ParserAppealsAL` as our reference implementation, which extracts court case data from the Alabama Appeals Court Public Portal. Court parsers typically differ from news parsers because they often need to handle JavaScript-rendered content, complex table structures, and paginated results.

## Key Features

- **JavaScript Support**: Uses Selenium WebDriver to render JavaScript-heavy pages
- **Automatic Browser Management**: Handles Chrome driver setup and teardown
- **Rate Limiting**: Built-in configurable delays between requests to avoid overwhelming the server
- **Table Parsing**: Specialized logic for extracting structured data from HTML tables
- **Error Handling**: Robust error handling with graceful fallbacks
- **Headless Operation**: Can run with or without a visible browser window

## Architecture

### Class Hierarchy

```
BaseParser (Abstract Base Class)
    └── ParserAppealsAL
```

ParserAppealsAL inherits from the `BaseParser` base class, which defines the common interface for all parsers in the OPAL system. It overrides key methods to provide court-specific functionality.

## Dependencies

```python
# Core Dependencies
selenium >= 4.0.0          # Browser automation
webdriver-manager >= 4.0.0 # Automatic ChromeDriver management
beautifulsoup4            # HTML parsing
requests                  # HTTP requests (inherited from base)

# Standard Library
json                      # JSON data handling
time                      # Rate limiting
datetime                  # Timestamp generation
typing                    # Type hints
```

## Implementation Guide

### 1. Basic Structure

To implement your own court parser based on ParserAppealsAL, start with this structure:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from your_project.parser_module import BaseParser

class YourCourtParser(BaseParser):
    def __init__(self, headless=True, rate_limit_seconds=3):
        super().__init__()
        self.headless = headless
        self.rate_limit_seconds = rate_limit_seconds
        self.driver = None
```

### 2. Core Methods

#### `__init__(self, headless: bool = True, rate_limit_seconds: int = 3)`

Initializes the parser with configuration options.

**Parameters:**
- `headless`: Run Chrome in headless mode (no visible window)
- `rate_limit_seconds`: Delay between requests to avoid rate limiting

#### `_setup_driver(self)`

Sets up the Chrome WebDriver with appropriate options:

```python
def _setup_driver(self):
    chrome_options = Options()
    if self.headless:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    self.driver = webdriver.Chrome(service=service, options=chrome_options)
```

#### `make_request(self, url: str, timeout: int = 30) -> Optional[str]`

Overrides the base class method to use Selenium instead of requests library.

**Key Features:**
- Lazy driver initialization
- Waits for specific elements to load
- Implements rate limiting
- Returns page source HTML

```python
def make_request(self, url, timeout=30):
    if not self.driver:
        self._setup_driver()
    
    self.driver.get(url)
    
    # Wait for your specific element
    WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
    )
    
    time.sleep(self.rate_limit_seconds)
    return self.driver.page_source
```

#### `parse_table_row(self, row) -> Optional[Dict]`

Extracts data from a single table row. This method is specific to the table structure of your court portal.

**Expected Table Structure:**
1. Court Name
2. Case Number (with optional link)
3. Case Title
4. Classification
5. Filed Date
6. Status

**Returns:**
```python
{
    "court": "Court of Civil Appeals",
    "case_number": {
        "text": "2230123",
        "link": "/case/details/..."
    },
    "case_title": "Smith v. Jones",
    "classification": "Civil",
    "filed_date": "06/11/2024",
    "status": "Active"
}
```

#### `parse_article(self, url: str) -> Dict`

Main parsing method that processes a single page of court results.

**Process:**
1. Loads the page using `make_request`
2. Parses HTML with BeautifulSoup
3. Finds the main data table
4. Extracts data from each row
5. Returns structured results

#### `parse_all_cases(self, base_url: str, page_urls: List[str]) -> Dict`

Processes multiple pages of results and combines them.

**Returns:**
```python
{
    "status": "success",
    "total_cases": 318,
    "extraction_date": "2025-01-13",
    "cases": [
        # List of case dictionaries
    ]
}
```

### 3. Integration with OPAL System

The parser integrates with OPAL through the `IntegratedParser` class:

```python
from opal.integrated_parser import IntegratedParser
from your_parser import YourCourtParser

# Create parser instance
parser = IntegratedParser(YourCourtParser)

# Process court data
result = parser.process_site(
    base_url="https://your-court-portal.gov/search",
    suffix="",  # Not used for court parsers
    max_pages=None  # Will process all available pages
)
```

### 4. URL Pagination

Court portals often use complex URL parameters for pagination. The system includes helper functions in `court_url_paginator.py`:

- `parse_court_url()`: Extracts page number and total pages from URL
- `build_court_url()`: Constructs URLs for specific pages
- `paginate_court_urls()`: Generates list of all page URLs

### 5. Best Practices

1. **Error Handling**: Always wrap operations in try-except blocks
2. **Resource Management**: Ensure driver is closed in finally blocks
3. **Rate Limiting**: Respect server limits to avoid IP bans
4. **Dynamic Waits**: Use WebDriverWait instead of fixed sleep times when possible
5. **Memory Management**: Close driver after processing to free resources

### 6. Testing

Create test scripts to validate your parser:

```python
from your_parser import YourCourtParser

def test_single_page():
    parser = YourCourtParser(headless=True)
    result = parser.parse_article("https://court-url.gov/page1")
    
    assert result["cases"]
    assert len(result["cases"]) > 0
    
    # Validate case structure
    case = result["cases"][0]
    assert "court" in case
    assert "case_number" in case
    assert "case_title" in case
```

## Customization Guide

### Adapting for Different Court Systems

1. **Table Structure**: Modify `parse_table_row()` to match your court's table columns
2. **Wait Conditions**: Update the element selector in `make_request()` 
3. **URL Patterns**: Adjust pagination logic in helper functions
4. **Data Fields**: Add or remove fields based on available data

### Common Modifications

1. **Different Table Selectors**:
```python
# Instead of generic "table"
WebDriverWait(self.driver, timeout).until(
    EC.presence_of_element_located((By.ID, "case-results-table"))
)
```

2. **Additional Data Extraction**:
```python
# Add judge information if available
judge = cells[6].get_text(strip=True) if len(cells) > 6 else ""
```

3. **Custom Headers**:
```python
# Some courts require authentication headers
self.driver.add_cookie({"name": "session", "value": "your-session-id"})
```

## Troubleshooting

### Common Issues

1. **ChromeDriver Not Found**: 
   - Solution: webdriver-manager should handle this automatically
   - Manual fix: Download ChromeDriver matching your Chrome version

2. **Elements Not Loading**:
   - Increase timeout in WebDriverWait
   - Check if element selectors have changed
   - Verify JavaScript is executing properly

3. **Rate Limiting**:
   - Increase `rate_limit_seconds`
   - Implement exponential backoff
   - Consider using proxy rotation

4. **Memory Leaks**:
   - Ensure driver is closed after use
   - Implement periodic driver restarts for long runs

## Performance Considerations

- **Headless Mode**: Significantly faster than visible browser
- **Parallel Processing**: Not recommended due to rate limits
- **Caching**: Consider caching parsed results to avoid re-parsing
- **Resource Usage**: Each driver instance uses ~100-200MB RAM

## Example Output

```json
{
    "status": "success",
    "total_cases": 318,
    "extraction_date": "2025-01-13",
    "cases": [
        {
            "court": "Court of Civil Appeals",
            "case_number": {
                "text": "CL-2024-000123",
                "link": "/portal/case/details/123"
            },
            "case_title": "Smith v. Jones Corporation",
            "classification": "Civil Appeal",
            "filed_date": "01/10/2025",
            "status": "Pending"
        },
        {
            "court": "Court of Criminal Appeals",
            "case_number": {
                "text": "CR-2024-000456",
                "link": "/portal/case/details/456"
            },
            "case_title": "State of Alabama v. Doe",
            "classification": "Criminal Appeal",
            "filed_date": "01/09/2025",
            "status": "Active"
        }
    ]
}
```

## Security Considerations

1. **Input Validation**: Always validate URLs before processing
2. **Sandbox Mode**: Chrome runs with --no-sandbox for compatibility
3. **Credential Storage**: Never hardcode credentials in parser
4. **SSL Verification**: Selenium handles SSL by default

## Future Enhancements

Consider these improvements for production use:

1. **Retry Logic**: Implement automatic retries for failed requests
2. **Progress Tracking**: Add callbacks for progress updates
3. **Data Validation**: Implement schema validation for parsed data
4. **Export Formats**: Support multiple output formats (CSV, Excel)
5. **Incremental Updates**: Track previously parsed cases to avoid duplicates