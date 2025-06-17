---
layout: default
title: "Alabama Appeals Court Public Portal Scraper - Implementation Instructions"
---

# Alabama Appeals Court Public Portal Scraper - Implementation Instructions

## Overview
Create a court case scraper extension for OPAL that extracts tabular data from the Alabama Appeals Court Public Portal. The scraper must handle JavaScript-rendered content, complex URL-based pagination, and preserve both text and link references.

## Step-by-Step Implementation Instructions

### Step 1: Update Dependencies
Add the following to `requirements.txt` and `pyproject.toml`:
- `selenium>=4.0.0` or `playwright>=1.40.0` (for JavaScript rendering)
- `webdriver-manager>=4.0.0` (if using Selenium for automatic driver management)

### Step 2: Create Court Case Parser Module
Create a new file `opal/court_case_parser.py` with the following specifications:

1. **Import necessary libraries**:
   - Selenium/Playwright for JavaScript rendering
   - BeautifulSoup for HTML parsing
   - Standard libraries for URL manipulation and JSON output

2. **Create `CourtCaseParser` class** that extends `BaseParser`:
   - Override `make_request()` to use Selenium/Playwright instead of requests
   - Implement JavaScript rendering with appropriate wait conditions
   - Add rate limiting (minimum 2-3 seconds between requests)

3. **Implement `parse_table_row()` method** to extract:
   - Court name from `<td class="text-start">` (column 1)
   - Case number text and href from `<a href="/portal/court/...">` (column 2)
   - Case title from `<td class="text-start">` (column 3)
   - Classification from `<td class="text-start">` (column 4)
   - Filed date from `<td class="text-start">` (column 5)
   - Open/Closed status from `<td class="text-start">` (column 6)

### Step 3: Create Custom URL Pagination Handler
Create `opal/court_url_paginator.py` with:

1. **URL parser function** to:
   - Extract and decode the complex URL parameters
   - Identify current page number from `page~(number~X)`
   - Extract total pages from `totalPages~X`

2. **URL builder function** to:
   - Take base URL and page number
   - Update `page~(number~X)` parameter
   - Maintain all other search parameters
   - Handle special encoding (`~`, `%2a2f`, etc.)

3. **Pagination iterator** that:
   - Starts at page 0
   - Continues until reaching `totalPages`
   - Yields properly formatted URLs for each page

### Step 4: Implement Data Extraction Logic
In `CourtCaseParser`, create `parse_all_cases()` method that:

1. **Initialize browser driver** (Selenium/Playwright)
2. **Load first page** and extract total pages from URL
3. **For each page**:
   - Navigate to page URL
   - Wait for table to load (use explicit waits)
   - Extract all table rows
   - Parse each row using `parse_table_row()`
   - Store results with preserved link references
4. **Close browser driver** when complete
5. **Return combined results** from all pages as single dataset

### Step 5: Define Output Format
Structure the output JSON as:
```json
{
  "status": "success",
  "total_cases": 317,
  "extraction_date": "2025-06-11",
  "cases": [
    {
      "court": "Alabama Supreme Court",
      "case_number": {
        "text": "SC-2025-0424",
        "link": "/portal/court/68f021c4-6a44-4735-9a76-5360b2e8af13/case/d024d958-58a1-41c9-9fae-39c645c7977e"
      },
      "case_title": "Frank Thomas Shumate, Jr. v. Berry Contracting L.P. d/b/a Bay Ltd.",
      "classification": "Appeal - Civil - Injunction Other",
      "filed_date": "06/10/2025",
      "status": "Open"
    }
  ]
}
```

### Step 6: Integrate with OPAL CLI
Modify existing OPAL files:

1. **Update `opal/__init__.py`**:
   - Add `from .court_case_parser import CourtCaseParser`
   - Add `from .court_url_paginator import paginate_court_urls`

2. **Update `opal/integrated_parser.py`**:
   - Add conditional logic to handle court case URLs differently
   - Use `paginate_court_urls` instead of `get_all_news_urls` for court sites

3. **Update `opal/main.py`**:
   - Add `--parser ParserAppealsAL` option to argparse choices
   - Add court parser to the parser selection logic
   - Adjust output filename format for court data

### Step 7: Handle Technical Requirements
Implement the following in `CourtCaseParser`:

1. **JavaScript rendering**:
   - Wait for table element to be present
   - Wait for data rows to load
   - Handle any loading spinners or dynamic content

2. **Error handling**:
   - Timeout exceptions for slow page loads
   - Missing table elements
   - Network errors
   - Browser crashes

3. **Rate limiting**:
   - Add configurable delay between page requests (default 3 seconds)
   - Respect server response times

### Step 8: Testing URLs
Use these URLs for testing:
- **First page**: `https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29`
- **Second page**: Same URL but with `page~(number~1)` and updated `totalElements~317~totalPages~13`

### Step 9: Final Integration
1. Test the complete flow with: `python -m opal --url [court_url] --parser ParserAppealsAL`
2. Ensure output file is created with court case data in tabular format
3. Verify all pages are scraped and combined into single result set
4. Confirm case number links are preserved in the output

## Expected Deliverables
1. `opal/court_case_parser.py` - Main parser for court data
2. `opal/court_url_paginator.py` - URL pagination handler
3. Updated `opal/__init__.py`, `opal/integrated_parser.py`, and `opal/main.py`
4. Updated `requirements.txt` and `pyproject.toml` with new dependencies
5. JSON output file with all court cases in structured format