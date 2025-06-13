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

## Notes

- Requires Chrome browser installed
- Uses Selenium for JavaScript support
- Handles pagination automatically
- Extracts both case list and detailed case information
- Includes comprehensive error handling for web automation