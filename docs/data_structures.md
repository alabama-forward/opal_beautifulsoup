# Data Structures

This document describes the data structures returned by OPAL parsers and extractors.

## Court Parser Data Structures

### Individual Court Case

Each court case is represented as a dictionary with the following structure:

```python
{
    "court": str,              # Court name (e.g., "Alabama Civil Appeals")
    "case_number": {
        "text": str,           # Case number (e.g., "2190259")
        "link": str            # URL to case details
    },
    "case_title": str,         # Full case title
    "classification": str,     # Case type (e.g., "Appeal", "Certiorari")
    "filed_date": str,         # Filing date (MM/DD/YYYY format)
    "status": str              # Case status (e.g., "Open", "Closed")
}
```

### Court Search Results

When using the court parser or configurable extractor, the complete results structure is:

```python
{
    "status": str,                    # "success" or "error"
    "search_parameters": {            # Parameters used for search
        "court": str,
        "date_period": str,
        "start_date": str | None,
        "end_date": str | None,
        "case_number": str | None,
        "case_title": str | None,
        "case_category": str | None,
        "exclude_closed": bool
    },
    "total_cases": int,               # Total number of cases found
    "extraction_date": str,           # Date of extraction (YYYY-MM-DD)
    "extraction_time": str,           # Time of extraction (HH:MM:SS)
    "pages_processed": int,           # Number of pages processed
    "cases": List[Dict]               # List of case dictionaries (see above)
}
```

### Paginated Results

For paginated court results:

```python
{
    "page": int,                      # Current page number
    "total_pages": int,               # Total number of pages
    "cases_on_page": int,             # Number of cases on this page
    "cases": List[Dict]               # List of cases for this page
}
```

## News Parser Data Structures

### News Article

News articles from alabamanewscenter.com:

```python
{
    "title": str,                     # Article title
    "link": str,                      # Article URL
    "date": str,                      # Publication date
    "author": str | None,             # Article author
    "summary": str | None,            # Article summary/excerpt
    "content": str,                   # Full article content
    "tags": List[str],                # Article tags/categories
    "image_url": str | None           # Main article image URL
}
```

### News Search Results

```python
{
    "status": str,                    # "success" or "error"
    "search_term": str | None,        # Search term used (if any)
    "category": str | None,           # Category filter (if any)
    "total_articles": int,            # Total articles found
    "articles": List[Dict]            # List of article dictionaries
}
```

## Integrated Parser Results

When using the integrated parser, results include a parser type indicator:

```python
{
    "parser_type": str,               # "court" or "news"
    "url": str,                       # Original URL processed
    "data": Dict                      # Parser-specific results (see above)
}
```

## CSV Output Formats

### Court Cases CSV

When exporting court cases to CSV:

| Column | Description | Example |
|--------|-------------|---------|
| court | Court name | Alabama Civil Appeals |
| case_number | Case number text | 2190259 |
| case_number_link | URL to case | https://... |
| case_title | Full case title | Smith v. Jones |
| classification | Case type | Appeal |
| filed_date | Filing date | 01/15/2024 |
| status | Case status | Open |

### News Articles CSV

When exporting news articles to CSV:

| Column | Description | Example |
|--------|-------------|---------|
| title | Article title | Breaking News... |
| link | Article URL | https://... |
| date | Publication date | 2024-01-15 |
| author | Author name | John Doe |
| summary | Article excerpt | This article... |
| tags | Comma-separated tags | politics,local |

## Error Response Structure

When errors occur:

```python
{
    "status": "error",
    "error_type": str,                # Type of error
    "error_message": str,             # Detailed error message
    "timestamp": str,                 # When error occurred
    "context": Dict | None            # Additional error context
}
```

## Metadata Fields

Common metadata fields across parsers:

```python
{
    "extraction_date": str,           # YYYY-MM-DD format
    "extraction_time": str,           # HH:MM:SS format
    "parser_version": str,            # OPAL version
    "processing_time_seconds": float, # Time taken to process
    "source_url": str                 # Original URL processed
}
```

## Type Definitions

For TypeScript or type-aware Python development:

```python
from typing import TypedDict, List, Optional, Union

class CaseNumber(TypedDict):
    text: str
    link: str

class CourtCase(TypedDict):
    court: str
    case_number: CaseNumber
    case_title: str
    classification: str
    filed_date: str
    status: str

class SearchParameters(TypedDict):
    court: str
    date_period: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    case_number: Optional[str]
    case_title: Optional[str]
    case_category: Optional[str]
    exclude_closed: bool

class CourtSearchResults(TypedDict):
    status: str
    search_parameters: SearchParameters
    total_cases: int
    extraction_date: str
    extraction_time: str
    pages_processed: int
    cases: List[CourtCase]

class NewsArticle(TypedDict):
    title: str
    link: str
    date: str
    author: Optional[str]
    summary: Optional[str]
    content: str
    tags: List[str]
    image_url: Optional[str]
```

## Data Validation

### Required Fields

**Court Cases**: All fields are required except `case_number.link` may be empty for some cases.

**News Articles**: Required fields are `title`, `link`, `date`, and `content`. Other fields may be null/empty.

### Date Formats

- Court filing dates: `MM/DD/YYYY` format
- News publication dates: `YYYY-MM-DD` format
- Extraction timestamps: ISO 8601 format

### Status Values

Court case status values:
- `Open` - Active case
- `Closed` - Completed case
- `Unknown` - Status not determined

### Classification Values

Common court case classifications:
- `Appeal`
- `Certiorari`
- `Original Proceeding`
- `Petition`
- `Certified Question`
- `Other`

## Usage Examples

### Accessing Court Case Data

```python
results = parser.extract_all_court_cases()

for case in results['cases']:
    print(f"Case: {case['case_number']['text']}")
    print(f"Title: {case['case_title']}")
    print(f"Filed: {case['filed_date']}")
    print(f"Status: {case['status']}")
    
    # Access case details URL
    if case['case_number']['link']:
        print(f"Details: {case['case_number']['link']}")
```

### Working with Search Parameters

```python
# Access search parameters used
params = results['search_parameters']
if params['date_period'] == 'custom':
    print(f"Date range: {params['start_date']} to {params['end_date']}")

# Check filters applied
if params['exclude_closed']:
    print("Closed cases were excluded")
```

### Error Handling

```python
if results['status'] == 'error':
    print(f"Error: {results['error_message']}")
    if 'context' in results:
        print(f"Context: {results['context']}")
else:
    process_cases(results['cases'])
```