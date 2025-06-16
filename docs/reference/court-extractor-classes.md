# Configurable Court Extractor Class Reference

This document provides the complete class reference for the Configurable Court Extractor, including class definitions, method signatures, and usage examples.

## Overview

The Configurable Court Extractor provides a flexible interface for searching and extracting court case data from the Alabama Appeals Court portal with various filtering options.

## Classes

### CourtSearchBuilder

A builder class that constructs URLs for searching the Alabama Appeals Court portal with configurable parameters.

```python
class CourtSearchBuilder:
    """
    Builder class for constructing court search URLs with configurable parameters.
    
    This class provides a flexible interface for building search queries for the
    Alabama Appeals Court portal with various filtering options.
    """
    
    def __init__(self):
        """Initialize the search builder with default values."""
        self.base_url = "https://publicportal.alappeals.gov/portal/search/case/results"
        self.params = {}
        
        # Court type mapping with their IDs
        self.courts = {
            'civil': 'ac1e3f4f-c03f-4fea-ad09-b83a0501c99f',
            'criminal': '2390512e-59b3-481a-8d15-a4377c12e5e0'
        }
        
        # Predefined date periods
        self.date_periods = {
            '1d': 1, '7d': 7, '1m': 30, '3m': 90, '6m': 180, '1y': 365
        }
```

#### Methods

##### set_court(court_type: str) -> 'CourtSearchBuilder'
```python
def set_court(self, court_type: str) -> 'CourtSearchBuilder':
    """
    Set the court type to search.
    
    Args:
        court_type: Either 'civil', 'criminal', or 'all'
        
    Returns:
        Self for method chaining
        
    Raises:
        ValueError: If invalid court type provided
    """
```

##### set_case_number(case_number: str) -> 'CourtSearchBuilder'
```python
def set_case_number(self, case_number: str) -> 'CourtSearchBuilder':
    """
    Set a specific case number to search for.
    
    Args:
        case_number: The case number (e.g., "2024-CA-001")
        
    Returns:
        Self for method chaining
    """
```

##### set_case_category(category: str) -> 'CourtSearchBuilder'
```python
def set_case_category(self, category: str) -> 'CourtSearchBuilder':
    """
    Set the case category to filter by.
    
    Common categories:
    - CV (Civil)
    - DV (Domestic Violence)
    - MC (Municipal Court)
    - PR (Probate)
    - SM (Small Claims)
    - TP (Traffic/Parking)
    
    Args:
        category: The case category code
        
    Returns:
        Self for method chaining
    """
```

##### set_date_range(start_date: str = None, end_date: str = None) -> 'CourtSearchBuilder'
```python
def set_date_range(self, start_date: str = None, end_date: str = None) -> 'CourtSearchBuilder':
    """
    Set a custom date range for filed dates.
    
    Args:
        start_date: Start date in MM/DD/YYYY format
        end_date: End date in MM/DD/YYYY format
        
    Returns:
        Self for method chaining
        
    Example:
        builder.set_date_range("01/01/2024", "12/31/2024")
    """
```

##### set_date_period(period: str) -> 'CourtSearchBuilder'
```python
def set_date_period(self, period: str) -> 'CourtSearchBuilder':
    """
    Set a predefined date period counting back from today.
    
    Args:
        period: One of '1d', '7d', '1m', '3m', '6m', '1y'
        
    Returns:
        Self for method chaining
        
    Raises:
        ValueError: If invalid period provided
    """
```

##### set_case_title(title: str) -> 'CourtSearchBuilder'
```python
def set_case_title(self, title: str) -> 'CourtSearchBuilder':
    """
    Set a case title to search for (partial match).
    
    Args:
        title: Part of the case title to search
        
    Returns:
        Self for method chaining
    """
```

##### set_case_status(status: str) -> 'CourtSearchBuilder'
```python
def set_case_status(self, status: str) -> 'CourtSearchBuilder':
    """
    Set the case status to filter by.
    
    Common statuses:
    - OPEN
    - CLOSED
    - PENDING
    - DISMISSED
    
    Args:
        status: The case status
        
    Returns:
        Self for method chaining
    """
```

##### exclude_closed_cases() -> 'CourtSearchBuilder'
```python
def exclude_closed_cases(self) -> 'CourtSearchBuilder':
    """
    Exclude closed cases from results.
    
    Returns:
        Self for method chaining
    """
```

##### build() -> str
```python
def build(self) -> str:
    """
    Build the final URL with all configured parameters.
    
    Returns:
        Complete URL with encoded parameters
    """
```

##### get_params() -> dict
```python
def get_params(self) -> dict:
    """
    Get the current parameters dictionary.
    
    Returns:
        Dictionary of current search parameters
    """
```

## Functions

### extract_court_cases_with_params

Main extraction function that uses the builder to fetch and parse court cases.

```python
def extract_court_cases_with_params(
    court_type: str = 'all',
    case_number: str = None,
    case_category: str = None,
    filed_after: str = None,
    filed_before: str = None,
    date_period: str = None,
    case_title: str = None,
    case_status: str = None,
    exclude_closed: bool = False,
    output_csv: bool = False,
    debug: bool = False
) -> dict:
    """
    Extract court cases with configurable search parameters.
    
    Args:
        court_type: 'civil', 'criminal', or 'all'
        case_number: Specific case number to search
        case_category: Case category (CV, DV, MC, etc.)
        filed_after: Start date (MM/DD/YYYY)
        filed_before: End date (MM/DD/YYYY)
        date_period: Predefined period ('1d', '7d', '1m', '3m', '6m', '1y')
        case_title: Partial case title to search
        case_status: Case status filter
        exclude_closed: Whether to exclude closed cases
        output_csv: Whether to also save as CSV
        debug: Whether to print debug information
        
    Returns:
        Dictionary containing:
            - status: 'success' or 'error'
            - total_cases: Number of cases found
            - cases: List of case dictionaries
            - extraction_date: When data was extracted
            - search_params: Parameters used for search
            - files_created: List of output files created
    """
```

## Command Line Interface

The module can be run directly from the command line:

```bash
python -m opal.configurable_court_extractor [options]
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--court` | Court type: civil, criminal, or all | all |
| `--case-number` | Specific case number to search | None |
| `--case-category` | Case category (CV, DV, MC, etc.) | None |
| `--filed-after` | Cases filed after date (MM/DD/YYYY) | None |
| `--filed-before` | Cases filed before date (MM/DD/YYYY) | None |
| `--date-period` | Predefined period: 1d, 7d, 1m, 3m, 6m, 1y | None |
| `--case-title` | Search in case title | None |
| `--case-status` | Filter by status | None |
| `--exclude-closed` | Exclude closed cases | False |
| `--output-csv` | Also save as CSV | False |
| `--debug` | Show debug information | False |

### CLI Examples

```bash
# Search civil cases from last 7 days
python -m opal.configurable_court_extractor --court civil --date-period 7d

# Search for specific case number
python -m opal.configurable_court_extractor --case-number "2024-CA-001"

# Search criminal cases excluding closed, save as CSV
python -m opal.configurable_court_extractor --court criminal --exclude-closed --output-csv

# Search by date range
python -m opal.configurable_court_extractor --filed-after 01/01/2024 --filed-before 12/31/2024

# Complex search with multiple filters
python -m opal.configurable_court_extractor \
    --court civil \
    --case-category CV \
    --date-period 1m \
    --case-status OPEN \
    --exclude-closed \
    --output-csv
```

## Usage Examples

### Basic Usage

```python
from opal.configurable_court_extractor import CourtSearchBuilder, extract_court_cases_with_params

# Using the builder directly
builder = CourtSearchBuilder()
url = builder.set_court('civil').set_date_period('7d').build()
print(f"Search URL: {url}")

# Using the extraction function
result = extract_court_cases_with_params(
    court_type='civil',
    date_period='7d',
    exclude_closed=True
)

print(f"Found {result['total_cases']} cases")
```

### Advanced Usage

```python
# Complex search with multiple filters
result = extract_court_cases_with_params(
    court_type='criminal',
    case_category='CV',
    filed_after='01/01/2024',
    filed_before='06/30/2024',
    case_status='OPEN',
    exclude_closed=True,
    output_csv=True,
    debug=True
)

# Process results
for case in result['cases']:
    print(f"Case: {case['case_number']['text']}")
    print(f"Title: {case['case_title']}")
    print(f"Status: {case['status']}")
    print("---")
```

### Integration with OPAL

```python
from opal.integrated_parser import IntegratedParser
from opal.court_case_parser import ParserAppealsAL
from opal.configurable_court_extractor import CourtSearchBuilder

# Build custom search URL
builder = CourtSearchBuilder()
search_url = builder.set_court('civil').set_date_period('1m').build()

# Use with integrated parser
parser = IntegratedParser(ParserAppealsAL)
result = parser.process_site(search_url)
```

## Output Format

The extractor returns data in the following format:

```json
{
    "status": "success",
    "total_cases": 150,
    "extraction_date": "2024-01-15",
    "search_params": {
        "court_type": "civil",
        "date_period": "7d",
        "exclude_closed": true
    },
    "cases": [
        {
            "court": "Court of Civil Appeals",
            "case_number": {
                "text": "2024-CA-001",
                "link": "https://..."
            },
            "case_title": "Smith v. Jones",
            "classification": "Civil",
            "filed_date": "01/10/2024",
            "status": "OPEN"
        }
    ],
    "files_created": [
        "2024-01-15_court_extractor_civil.json",
        "2024-01-15_court_extractor_civil.csv"
    ]
}
```

## Error Handling

The extractor includes comprehensive error handling:

- Network errors are caught and reported
- Invalid parameters raise `ValueError` with descriptive messages
- Partial failures (some pages fail) still return successful results
- All errors are logged with context

## Performance Considerations

- The extractor includes automatic rate limiting (3 seconds between requests)
- Large result sets may take several minutes to complete
- Progress is printed to console during extraction
- Consider using date filters to limit result size