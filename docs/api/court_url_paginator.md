# Court URL Paginator

The Court URL Paginator module (`opal.court_url_paginator`) provides utilities for handling pagination in the Alabama Appeals Court Public Portal. It includes functions for parsing, building, and generating paginated URLs.

## Overview

The Alabama Appeals Court portal (`publicportal.alappeals.gov`) uses URL-encoded pagination parameters. This module handles:

- Parsing page numbers from encoded URLs
- Building URLs for specific pages
- Extracting total page count from initial loads
- Generating complete sets of paginated URLs
- Validating Appeals Court portal URLs

## Functions

### `parse_court_url(url)`

Extracts current page number and total pages from a court URL.

```python
from opal.court_url_paginator import parse_court_url

url = "https://publicportal.alappeals.gov/portal/search/case/results?..."
current_page, total_pages = parse_court_url(url)

print(f"Current page: {current_page}, Total pages: {total_pages}")
# Current page: 0, Total pages: 5
```

**Parameters:**
- `url` (str): The court URL to parse

**Returns:**
- `Tuple[Optional[int], Optional[int]]`: (current_page, total_pages) or (None, None) if parsing fails

**URL Pattern Parsed:**
The function looks for these patterns in decoded URLs:
- `page~(.*?number~(\d+)` - extracts current page number
- `totalPages~(\d+)` - extracts total page count

### `build_court_url(base_url, page_number)`

Constructs a URL for a specific page number.

```python
from opal.court_url_paginator import build_court_url

base_url = "https://publicportal.alappeals.gov/portal/search/case/results?..."
page_2_url = build_court_url(base_url, 2)
```

**Parameters:**
- `base_url` (str): The original court URL (any page)
- `page_number` (int): The desired page number (0-indexed)

**Returns:**
- `str`: URL for the specified page

**Implementation:**
Uses regex to replace the page number in the pattern: `page~%28.*?number~X`

### `extract_total_pages_from_first_load(url, parser)`

Extracts the total number of pages by loading the first page and checking for JavaScript updates.

```python
from opal.court_url_paginator import extract_total_pages_from_first_load
from opal.parser_appeals_al import ParserAppealsAL

parser = ParserAppealsAL()
total_pages = extract_total_pages_from_first_load(court_url, parser)
print(f"Total pages: {total_pages}")
```

**Parameters:**
- `url` (str): Initial URL (typically page 0)
- `parser`: ParserAppealsAL instance to make the request

**Returns:**
- `int`: Total number of pages (1 if extraction fails)

**Process:**
1. Makes request using the parser
2. Waits for JavaScript to update the URL
3. Parses the updated URL for total page count
4. Falls back to 1 if unable to determine

### `paginate_court_urls(base_url, parser=None)`

Generates a list of URLs for all pages in the search results.

```python
from opal.court_url_paginator import paginate_court_urls
from opal.parser_appeals_al import ParserAppealsAL

parser = ParserAppealsAL()

# With parser for dynamic total page detection
urls = paginate_court_urls(first_url, parser)

# Without parser (uses URL info only)
urls = paginate_court_urls(first_url)

for i, url in enumerate(urls):
    print(f"Page {i}: {url}")
```

**Parameters:**
- `base_url` (str): Initial court search URL
- `parser` (optional): ParserAppealsAL instance for dynamic page detection

**Returns:**
- `List[str]`: List of URLs for all pages (0-indexed)

**Logic:**
1. Try to parse total pages from URL
2. If not available and parser provided, load first page to detect
3. Generate URLs for all pages (0 to total_pages-1)
4. Return just base URL if pagination cannot be determined

### `is_court_url(url)`

Validates if a URL is from the Alabama Appeals Court portal.

```python
from opal.court_url_paginator import is_court_url

if is_court_url(url):
    print("Valid Appeals Court URL")
else:
    print("Not an Appeals Court URL")
```

**Parameters:**
- `url` (str): URL to validate

**Returns:**
- `bool`: True if URL contains both `publicportal.alappeals.gov` and `/portal/search/case/results`

## URL Structure

Appeals Court URLs use encoded pagination parameters:

```
https://publicportal.alappeals.gov/portal/search/case/results?searchParams=...page~%28size~25~number~0~totalElements~125~totalPages~5%29
```

Key components:
- `page~%28` - Start of page parameter block
- `size~25` - Results per page
- `number~0` - Current page (0-indexed)
- `totalElements~125` - Total result count
- `totalPages~5` - Total number of pages

## Integration Examples

### With ParserAppealsAL

```python
from opal.parser_appeals_al import ParserAppealsAL
from opal.court_url_paginator import paginate_court_urls, extract_total_pages_from_first_load

parser = ParserAppealsAL()

# Get total pages dynamically
total_pages = extract_total_pages_from_first_load(search_url, parser)
print(f"Found {total_pages} pages")

# Generate all page URLs
all_urls = paginate_court_urls(search_url, parser)

# Process each page
all_cases = []
for i, url in enumerate(all_urls):
    print(f"Processing page {i+1}/{len(all_urls)}")
    cases = parser.extract_page_data(url)
    all_cases.extend(cases)
```

### With Configurable Court Extractor

The configurable court extractor uses these functions internally:

```python
# Internal usage in configurable_court_extractor.py
def _process_paginated_results(self, first_page_url):
    # Generate URLs for all pages
    page_urls = paginate_court_urls(first_page_url, self.parser)
    
    # Process each page
    for url in page_urls:
        self._process_page(url)
```

### Manual Pagination Handling

```python
from opal.court_url_paginator import parse_court_url, build_court_url

# Parse current state
current_page, total_pages = parse_court_url(search_url)

if total_pages and total_pages > 1:
    # Process remaining pages
    for page_num in range(current_page + 1, total_pages):
        next_url = build_court_url(search_url, page_num)
        # Process next_url...
```

## Error Handling

The paginator functions are designed to fail gracefully:

- `parse_court_url`: Returns (None, None) if parsing fails
- `extract_total_pages_from_first_load`: Returns 1 if extraction fails
- `build_court_url`: Returns original URL if building fails
- `paginate_court_urls`: Returns single-item list with base URL if pagination fails

```python
# Safe usage pattern
from opal.court_url_paginator import paginate_court_urls

try:
    urls = paginate_court_urls(court_url, parser)
    if len(urls) == 1:
        print("Single page or pagination detection failed")
except Exception as e:
    print(f"Pagination error: {e}")
    urls = [court_url]  # Fallback to original URL
```

## Performance Considerations

- URL parsing is fast and doesn't require network requests
- Dynamic page detection requires loading the first page
- Consider caching total page counts for repeated searches
- Use with rate limiting to avoid overwhelming the server

## Debugging

Enable debug output by checking the console messages:

```python
from opal.court_url_paginator import extract_total_pages_from_first_load

# Function prints debug messages:
# "Detected X total pages from URL"
# "Error parsing URL: ..."
# "Error extracting total pages: ..."

total_pages = extract_total_pages_from_first_load(url, parser)
```

## Limitations

1. **Appeals Court Specific**: Only works with `publicportal.alappeals.gov` URLs
2. **JavaScript Dependency**: Requires browser/parser for dynamic page detection
3. **URL Structure Dependency**: May break if portal changes URL encoding
4. **0-Based Indexing**: Page numbers are 0-indexed (page 0 is first page)
5. **Session Dependency**: URLs may be session-based and expire

## Complete Example

```python
from opal.court_url_paginator import (
    is_court_url, 
    parse_court_url,
    paginate_court_urls,
    extract_total_pages_from_first_load
)
from opal.parser_appeals_al import ParserAppealsAL

def process_all_appeals_court_pages(search_url):
    # Validate URL
    if not is_court_url(search_url):
        raise ValueError("Not a valid Appeals Court URL")
    
    # Parse initial URL
    current_page, total_pages = parse_court_url(search_url)
    print(f"Starting from page {current_page}, total: {total_pages}")
    
    # Setup parser
    parser = ParserAppealsAL()
    
    # Get total pages if not in URL
    if total_pages is None:
        total_pages = extract_total_pages_from_first_load(search_url, parser)
        print(f"Detected {total_pages} total pages")
    
    # Generate all URLs
    all_urls = paginate_court_urls(search_url, parser)
    
    # Process each page
    results = []
    for i, url in enumerate(all_urls):
        print(f"Processing page {i}/{len(all_urls)-1}")
        page_data = parser.extract_page_data(url)
        results.extend(page_data)
    
    return results

# Usage
search_url = "https://publicportal.alappeals.gov/portal/search/case/results?..."
all_cases = process_all_appeals_court_pages(search_url)
print(f"Extracted {len(all_cases)} total cases")
```

## Key Differences from Other Court Systems

This module is specifically designed for the Alabama **Appeals Court** portal, which differs from other Alabama court systems:

- **URL Domain**: `publicportal.alappeals.gov` (not `alacourt.gov`)
- **Pagination**: URL-encoded parameters (not JavaScript/AJAX)
- **Page Indexing**: 0-based (page 0 is first page)
- **Search Path**: `/portal/search/case/results` (not `/ajax/courts.aspx`)

Make sure you're using the correct parser and URLs for the Appeals Court system.