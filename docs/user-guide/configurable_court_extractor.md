# Configurable Court Extractor

The Configurable Court Extractor (`opal.configurable_court_extractor`) provides advanced searching and filtering capabilities for the Alabama Appeals Court portal. It includes both programmatic and command-line interfaces for extracting court data with precise control over search parameters.

## Overview

The configurable court extractor consists of:

- **`CourtSearchBuilder`** class for building complex search parameters
- **`extract_court_cases_with_params()`** function for programmatic extraction
- **Command-line interface** for terminal-based extraction

It supports:
- Dynamic court selection (Civil, Criminal, Supreme)
- Advanced search filtering
- Custom URL support for pre-built searches
- Multiple output formats (JSON, CSV)

## Classes and Functions

### CourtSearchBuilder

A builder class for constructing Alabama Court search URLs with court-specific parameters.

```python
from opal.configurable_court_extractor import CourtSearchBuilder

# Create search builder
builder = CourtSearchBuilder()

# Configure search parameters
builder.set_court("civil")
builder.set_date_range(period="1m")  # Last month
builder.set_case_category("Appeal")
builder.set_exclude_closed(True)

# Build the search URL
search_url = builder.build_url(page_number=0)
```

#### Available Methods

**Court Configuration:**
- `set_court(court_key)` - Set court type ('civil', 'criminal', 'supreme')
- `get_court_info()` - Get information about current court
- `discover_court_ids(parser_instance)` - Auto-discover court IDs from website
- `set_court_id_manually(court_key, court_id)` - Manually set court ID

**Date Filtering:**
- `set_date_range(start_date=None, end_date=None, period='1y')` - Set date filter
  - Periods: '7d', '1m', '3m', '6m', '1y', 'custom'
  - Custom requires start_date and end_date

**Case Filtering:**
- `set_case_category(category_name=None)` - Filter by case type
  - Categories: 'Appeal', 'Certiorari', 'Original Proceeding', 'Petition', 'Certified Question'
- `set_case_number_filter(case_number=None)` - Filter by case number
- `set_case_title_filter(title=None)` - Filter by case title
- `set_exclude_closed(exclude=False)` - Exclude closed cases

**URL Building:**
- `build_url(page_number=0)` - Build complete search URL
- `build_criteria_string()` - Build URL criteria parameters

### extract_court_cases_with_params()

Main extraction function that supports both parameter-based and URL-based searches.

```python
from opal.configurable_court_extractor import extract_court_cases_with_params

# Parameter-based search
results = extract_court_cases_with_params(
    court='civil',
    date_period='1m',
    case_category='Appeal',
    exclude_closed=True,
    max_pages=5,
    output_prefix="civil_appeals"
)

# Custom URL search
results = extract_court_cases_with_params(
    custom_url="https://publicportal.alappeals.gov/portal/search/case/results?criteria=...",
    max_pages=5,
    output_prefix="custom_search"
)
```

#### Parameters

**Search Parameters** (ignored if custom_url provided):
- `court` (str): Court type ('civil', 'criminal', 'supreme')
- `date_period` (str): Date period ('7d', '1m', '3m', '6m', '1y', 'custom')
- `start_date` (str): Start date for custom range (YYYY-MM-DD)
- `end_date` (str): End date for custom range (YYYY-MM-DD)
- `case_number` (str): Case number filter (partial match)
- `case_title` (str): Case title filter (partial match)
- `case_category` (str): Case category filter
- `exclude_closed` (bool): Whether to exclude closed cases

**Processing Options:**
- `max_pages` (int): Maximum pages to process (None for all)
- `output_prefix` (str): Prefix for output files
- `custom_url` (str): Pre-built search URL (overrides all search params)

## Court Definitions

The system supports three Alabama Appeals Courts:

```python
courts = {
    'civil': {
        'name': 'Alabama Civil Court of Appeals',
        'case_prefix': 'CL',
        'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition']
    },
    'criminal': {
        'name': 'Alabama Court of Criminal Appeals', 
        'case_prefix': 'CR',
        'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition']
    },
    'supreme': {
        'name': 'Alabama Supreme Court',
        'case_prefix': 'SC',
        'categories': ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition', 'Certified Question']
    }
}
```

## Command-Line Interface

### Basic Usage

```bash
# Extract civil court cases from last month
python -m opal.configurable_court_extractor --court civil --date-period 1m

# Extract criminal appeals with custom date range
python -m opal.configurable_court_extractor \
    --court criminal \
    --date-period custom \
    --start-date 2024-01-01 \
    --end-date 2024-01-31 \
    --case-category Appeal

# Use custom URL
python -m opal.configurable_court_extractor \
    --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..."
```

### CLI Options

**URL Option** (overrides all search parameters):
- `--url` - Pre-built search URL with embedded parameters

**Search Parameters** (ignored if --url provided):
- `--court {civil,criminal,supreme}` - Court to search (default: civil)
- `--date-period {7d,1m,3m,6m,1y,custom}` - Date period (default: 1y)
- `--start-date YYYY-MM-DD` - Start date for custom range
- `--end-date YYYY-MM-DD` - End date for custom range
- `--case-number TEXT` - Case number filter
- `--case-title TEXT` - Case title filter
- `--case-category {Appeal,Certiorari,Original Proceeding,Petition,Certified Question}` - Case category
- `--exclude-closed` - Exclude closed cases

**Output Options**:
- `--max-pages INT` - Maximum pages to process
- `--output-prefix TEXT` - Prefix for output files (default: court_cases)

## Programmatic Usage Examples

### Basic Search

```python
from opal.configurable_court_extractor import CourtSearchBuilder, extract_court_cases_with_params
from opal.court_case_parser import ParserAppealsAL

# Simple extraction
results = extract_court_cases_with_params(
    court='civil',
    date_period='7d',
    exclude_closed=True
)

if results and results['status'] == 'success':
    print(f"Found {results['total_cases']} cases")
    for case in results['cases']:
        print(f"- {case['case_number']['text']}: {case['case_title']}")
```

### Advanced Search with Builder

```python
from opal.configurable_court_extractor import CourtSearchBuilder
from opal.court_case_parser import ParserAppealsAL

# Create builder and parser
builder = CourtSearchBuilder()
parser = ParserAppealsAL(headless=True)

# Discover court IDs
builder.discover_court_ids(parser)

# Configure search
builder.set_court('supreme')
builder.set_date_range(start_date='2024-01-01', end_date='2024-03-31', period='custom')
builder.set_case_category('Certiorari')
builder.set_exclude_closed(True)

# Get search URL and extract
search_url = builder.build_url()
results = extract_court_cases_with_params(custom_url=search_url)
```

### Processing Custom URLs

```python
# Handle session-based URLs from website
custom_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..."

results = extract_court_cases_with_params(
    custom_url=custom_url,
    max_pages=10,
    output_prefix="session_search"
)

# The function will warn about session expiration
```

## Court ID Discovery

The system automatically discovers court IDs from the website:

```python
builder = CourtSearchBuilder()
parser = ParserAppealsAL()

# Auto-discover court IDs
builder.discover_court_ids(parser)

# Check discovery results
for court_key, court_info in builder.courts.items():
    print(f"{court_info['name']}: {court_info['id']}")

# Manual override if needed
builder.set_court_id_manually('civil', '68f021c4-6a44-4735-9a76-5360b2e8af13')
```

## Output Format

### JSON Output Structure

```json
{
    "status": "success",
    "search_parameters": {
        "court": "civil",
        "date_period": "1m",
        "case_category": "Appeal",
        "exclude_closed": true
    },
    "total_cases": 25,
    "extraction_date": "2024-01-15",
    "extraction_time": "14:30:22",
    "pages_processed": 2,
    "cases": [
        {
            "court": "Alabama Civil Court of Appeals",
            "case_number": {
                "text": "CL-2024-0123",
                "link": "/portal/case/detail/12345"
            },
            "case_title": "Smith v. Jones",
            "classification": "Appeal",
            "filed_date": "01/10/2024",
            "status": "Open"
        }
    ]
}
```

### CSV Output

Automatically generated alongside JSON:
- Court, Case Number, Case Title, Classification, Filed Date, Status, Case Link

## Error Handling and Warnings

### Session URL Warnings

When using custom URLs:

```
⚠️  WARNING: Custom URLs contain session-specific parameters that expire.
   This URL will only work temporarily and may become invalid after your browser session ends.
   For reliable, repeatable searches, use the CLI search parameters instead of --url option.
```

### Court ID Discovery Failures

```python
# Graceful fallback to known IDs
if court_info['id'] is None:
    raise ValueError(f"Could not discover court ID for {court_name}. "
                   "Try using the --url option with a pre-built search URL instead.")
```

## Integration with Other Components

### With ParserAppealsAL

```python
from opal.configurable_court_extractor import CourtSearchBuilder
from opal.court_case_parser import ParserAppealsAL

# The extractor uses ParserAppealsAL internally
parser = ParserAppealsAL(headless=True, rate_limit_seconds=2)
builder = CourtSearchBuilder()

# Discovery requires parser instance
builder.discover_court_ids(parser)
```

### With Court URL Paginator

```python
from opal.configurable_court_extractor import extract_court_cases_with_params
from opal.court_url_paginator import parse_court_url

# Extract cases and check pagination
results = extract_court_cases_with_params(court='civil', date_period='1m')

# The function internally handles pagination automatically
print(f"Processed {results['pages_processed']} pages")
```

## Performance Considerations

- **Court ID Discovery**: Requires web scraping, cached after first discovery
- **Rate Limiting**: Built-in 2-second delays between requests
- **Memory Usage**: Processes pages sequentially to manage memory
- **Session Management**: Custom URLs expire, use parameters for reliability

## Troubleshooting

### Common Issues

1. **Court ID Discovery Fails**
   - Use `--url` option with pre-built search URL
   - Manually set court IDs with `set_court_id_manually()`

2. **Custom URL Stops Working**
   - URLs are session-based and expire
   - Switch to parameter-based search
   - Create new search on website to get fresh URL

3. **No Results Found**
   - Check date range (default is last year)
   - Verify court has cases in date range
   - Try broader search criteria

### Debug Mode

```bash
# Run with headless=False to see browser
# Modify the script to set headless=False in ParserAppealsAL
```

## Complete Example

```python
#!/usr/bin/env python3
from opal.configurable_court_extractor import extract_court_cases_with_params

def main():
    # Extract recent civil appeals
    results = extract_court_cases_with_params(
        court='civil',
        date_period='1m',
        case_category='Appeal',
        exclude_closed=True,
        max_pages=5,
        output_prefix='civil_appeals_recent'
    )
    
    if results and results['status'] == 'success':
        print(f"✓ Extracted {results['total_cases']} cases")
        print(f"✓ Processed {results['pages_processed']} pages")
        
        # Show sample cases
        for case in results['cases'][:3]:
            print(f"- {case['case_number']['text']}: {case['case_title']}")
    else:
        print("❌ Extraction failed")

if __name__ == "__main__":
    main()
```

This extractor provides a powerful interface for accessing Alabama Appeals Court data with flexible search capabilities and robust error handling.