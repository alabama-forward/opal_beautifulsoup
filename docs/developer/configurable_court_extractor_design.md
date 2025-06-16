---
layout: default
title: "Configurable Court Extractor Design"
---

# Configurable Court Extractor Design

## Problem Statement

A former version of `extract_all_court_cases.py` had hardcoded search parameters in the URL, making it inflexible for different search criteria. Users couldn't dynamically change:
- Date ranges
- Case number filters
- Case title filters
- Whether to include/exclude closed cases

## Solution Overview

I designed a configurable court extractor that separates URL construction from data extraction, allowing users to specify search parameters via command line arguments or function parameters.

## Architecture

### 1. CourtSearchBuilder Class

**Purpose**: Encapsulates the complex URL building logic for Alabama Appeals Court searches.

#### **Why I designed it this way**:

- **Separation of Concerns**: URL building is separate from data extraction

- **Maintainability**: Changes to URL structure only affect one class

- **Reusability**: Can be used by different scripts or tools

- **Readability**: Clear methods for each search parameter

```python
class CourtSearchBuilder:
    def __init__(self):
        self.base_url = "https://publicportal.alappeals.gov/portal/search/case/results"
        self.court_id = "68f021c4-6a44-4735-9a76-5360b2e8af13"
        self.reset_params()
```

### 2. Key Methods Explained

#### `set_date_range()`
**Purpose**: Handle different date range options
**Design rationale**:
- Supports both predefined periods (`-1y`, `-6m`) and custom date ranges
- Automatically converts dates to the portal's expected format (`*2f` encoding)
- Provides sensible defaults

#### `build_criteria_string()`
**Purpose**: Construct the complex URL-encoded criteria parameter
**Design rationale**:
- Handles the intricate URL encoding required by the portal
- Builds the nested parameter structure programmatically
- Reduces human error in URL construction

#### `build_url()`
**Purpose**: Create complete search URLs with pagination
**Design rationale**:
- Updates page numbers dynamically
- Maintains other search parameters across pages
- Returns ready-to-use URLs

## Configuration Options

### Court Selection
```python
# Available courts
courts = {
    'civil': 'Alabama Civil Court of Appeals',
    'criminal': 'Alabama Court of Criminal Appeals', 
    'supreme': 'Alabama Supreme Court'
}

# Select court
search_builder.set_court('civil')  # or 'criminal', 'supreme'
```

### Case Number Formats
```python
# Open-ended search
search_builder.set_case_number_filter('2024-001')

# Court-specific formats
search_builder.set_case_number_filter('CL-2024-0001')  # Civil Appeals
search_builder.set_case_number_filter('CR-2024-0001')  # Criminal Appeals  
search_builder.set_case_number_filter('SC-2024-0001')  # Supreme Court
```

### Case Categories
```python
# For Civil Appeals and Criminal Appeals
categories = ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition']

# For Supreme Court (includes additional option)
supreme_categories = ['Appeal', 'Certiorari', 'Original Proceeding', 'Petition', 'Certified Question']

# Set category
search_builder.set_case_category('Appeal')
```

### Date Filters
```python
# Predefined periods (matching portal options)
search_builder.set_date_range(period='7d')   # Last 7 days
search_builder.set_date_range(period='1m')   # Last month
search_builder.set_date_range(period='3m')   # Last 3 months
search_builder.set_date_range(period='6m')   # Last 6 months
search_builder.set_date_range(period='1y')   # Last year

# Custom date range
search_builder.set_date_range('2024-01-01', '2024-12-31', 'custom')
```

### Case Title and Status Filters
```python
# Filter by case title (partial match)
search_builder.set_case_title_filter('Smith v Jones')

# Exclude closed cases
search_builder.set_exclude_closed(True)
```

## Command Line Interface

**Why I included CLI arguments**:
- **User-friendly**: No need to modify code for different searches
- **Scriptable**: Can be integrated into automated workflows
- **Documented**: Built-in help shows all options

### Usage Examples

#### Option 1: Use Built-in Search Parameters (Recommended)
```bash
# Extract all cases from last year (default from all courts)
python configurable_court_extractor.py

# Extract cases from Alabama Supreme Court only
python configurable_court_extractor.py --court supreme

# Extract cases from last 7 days from Criminal Appeals
python configurable_court_extractor.py --court criminal --date-period 7d

# Extract Appeal cases from Civil Court
python configurable_court_extractor.py --court civil --case-category Appeal

# Extract cases with custom date range from Supreme Court
python configurable_court_extractor.py --court supreme --date-period custom --start-date 2024-01-01 --end-date 2024-06-30

# Filter by specific case number format
python configurable_court_extractor.py --court civil --case-number "CL-2024-"

# Filter by case title in Criminal Appeals
python configurable_court_extractor.py --court criminal --case-title "State v"

# Exclude closed cases from Supreme Court
python configurable_court_extractor.py --court supreme --exclude-closed

# Extract Certified Questions from Supreme Court (unique to Supreme Court)
python configurable_court_extractor.py --court supreme --case-category "Certified Question"

# Comprehensive search with multiple filters
python configurable_court_extractor.py --court civil --case-category Appeal --date-period 3m --exclude-closed --output-prefix "civil_appeals_q1"
```

#### Option 2: Use Pre-built URL with Embedded Search Terms
⚠️  **WARNING**: Custom URLs are temporary and session-based. They may stop working when the website session expires.

```bash
# Use your existing URL with search terms already embedded
python configurable_court_extractor.py --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29"

# Use custom URL with limited pages and custom output prefix
python configurable_court_extractor.py --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..." --max-pages 5 --output-prefix "my_custom_search"

# Any URL from the portal search interface works
python configurable_court_extractor.py --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=YOUR_CUSTOM_SEARCH_CRITERIA"
```

#### Hybrid Approach
```bash
# You can also programmatically call the function with a custom URL
from configurable_court_extractor import extract_court_cases_with_params

# Use your existing URL
your_url = "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..."
result = extract_court_cases_with_params(custom_url=your_url, max_pages=10)
```

## Dynamic Court ID Discovery

### The Problem with Dynamic IDs

Modern web applications often generate session-specific or dynamic identifiers that change between visits. The Alabama Appeals Court portal appears to use dynamic court IDs that are assigned during the user's session rather than being static, predictable values.

### Solution

**Chosen Solution: Automatic Discovery**
The `discover_court_ids()` method navigates to the court's search interface and programmatically extracts the current court IDs by:

1. **Loading the search page** - Navigates to the main case search interface
2. **Inspecting form elements** - Locates the court selection dropdown or form elements
3. **Extracting ID mappings** - Parses the HTML to find court names and their corresponding dynamic IDs
4. **Caching for session** - Stores the discovered IDs for the duration of the session

**Option 2: Manual Discovery**
If automatic discovery fails, users can:

1. **Inspect browser network traffic** - Use browser developer tools to monitor the search requests
2. **Extract court ID from URL** - Copy a working search URL and extract the court ID parameter
3. **Set manually** - Use `set_court_id_manually()` to override the discovered ID

**Option 3: URL Bypass (Fallback)**
When court ID discovery completely fails, users can:

1. **Use browser to build URL** - Manually configure search on the website
2. **Copy complete URL** - Get the full URL with embedded parameters
3. **Use --url option** - Pass the pre-built URL directly, bypassing all parameter building

### Implementation Benefits

1. **Resilient to changes** - Automatically adapts to new court ID schemes
2. **Fallback options** - Multiple strategies when automatic discovery fails
3. **User-friendly** - Handles complexity behind the scenes
4. **Transparent** - Shows discovered IDs to user for verification

### Usage Examples with Dynamic IDs

```bash
# Let the system discover court IDs automatically
python configurable_court_extractor.py --court civil --date-period 1m

# If discovery fails, fall back to custom URL
python configurable_court_extractor.py --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..."

# For debugging: manually set a court ID
search_builder = CourtSearchBuilder()
search_builder.set_court_id_manually('civil', 'discovered-session-id-12345')
```

## Technical Implementation Details

### URL Encoding Strategy

The Alabama Appeals Court portal uses a complex nested URL structure:
```
?criteria=~%28advanced~false~courtID~%27{court_id}~page~%28...%29~sort~%28...%29~case~%28...%29%29
```

**My approach**:

1. Build parameters as nested dictionaries
2. Convert to the portal's specific encoding format
3. Handle special characters and escaping automatically

### Error Handling

**Graceful degradation**:
- If total page count can't be determined, process incrementally
- Continue processing if individual pages fail
- Provide detailed error messages with stack traces

### Performance Considerations

**Rate limiting**: 
- Configurable delays between requests
- Respectful of server resources

**Memory efficiency**:
- Process pages incrementally
- Don't load all data into memory at once

**Progress reporting**:
- Real-time feedback on processing status
- Clear indication of completion

## Advantages Over Former Implementation

### 1. Flexibility
- **Before**: Fixed search parameters in hardcoded URL
- **After**: Configurable search criteria via parameters OR custom URLs

### 2. Maintainability
- **Before**: URL changes require code modification
- **After**: URL structure centralized in builder class with dynamic discovery

### 3. Usability
- **Before**: Developers need to understand complex URL structure
- **After**: Simple method calls and CLI arguments

### 4. Reusability
- **Before**: Single-purpose script
- **After**: Reusable components for different use cases

### 5. Documentation
- **Before**: Search parameters hidden in URL
- **After**: Clear parameter documentation and examples

### 6. Resilience to Changes
- **Before**: Hardcoded court IDs break when website changes
- **After**: Automatic discovery adapts to dynamic court ID schemes

### 7. Multiple Fallback Options
- **Before**: Script fails completely if URL structure changes
- **After**: Automatic discovery → manual discovery → custom URL bypass

## Integration with Existing Code

The new extractor coexists with the current implementation:
- Uses the same `ParserAppealsAL` class
- Produces the same JSON/CSV output format
- Follows the same error handling patterns

## Future Enhancements

### Advanced Features
- Save/load search configurations
- Scheduled extractions
- Differential updates (only new cases)
- Export to additional formats (Excel, XML)

### Performance Improvements
- Parallel page processing
- Caching of search results
- Resume interrupted extractions

## Code Structure

```
configurable_court_extractor.py
├── CourtSearchBuilder class
│   ├── Parameter management methods
│   ├── URL building methods
│   └── Validation methods
├── extract_court_cases_with_params() function
│   ├── Search execution logic
│   ├── Progress reporting
│   └── Output generation
└── main() function
    ├── CLI argument parsing
    ├── Parameter validation
    └── Function orchestration
```

## Why This Design is Better

1. **Single Responsibility**: Each class/function has one clear purpose
2. **Open/Closed Principle**: Easy to extend without modifying existing code
3. **DRY (Don't Repeat Yourself)**: URL logic is centralized
4. **User-Centered**: Designed around user needs, not technical constraints
5. **Testable**: Components can be unit tested independently
6. **Documented**: Self-documenting code with clear method names

This design transforms a rigid, single-purpose script into a flexible, user-friendly tool that can adapt to various research needs while maintaining the reliability and performance of the original implementation.

## Implementation Reference

> **Note**: The complete implementation code has been moved to the reference documentation for better organization. Please refer to the [Configurable Court Extractor Reference](/reference/configurable_court_extractor/) for the full source code, API documentation, and detailed implementation examples.

## Key Design Decisions Explained

1. **Builder Pattern**: Separates URL construction complexity from business logic
2. **Dual-Mode Operation**: Supports both parameter-based search and pre-built URL input
3. **Parameter Validation**: Ensures required combinations are provided (custom dates)
4. **Progressive Enhancement**: Starts with defaults, allows selective customization
5. **Error Recovery**: Graceful handling when page counts can't be determined
6. **Output Consistency**: Maintains same format as original extractor
7. **User Feedback**: Real-time progress and parameter confirmation
8. **URL Flexibility**: Custom URLs override all search parameters for maximum flexibility

## Summary

This design transforms a rigid, single-purpose script into a flexible, user-friendly tool that can adapt to various research needs while maintaining the reliability and performance of the original implementation. The modular architecture ensures that each component has a single responsibility, making the system easy to extend, test, and maintain.