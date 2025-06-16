# Workflows

This document describes the internal workflows and processing patterns used by OPAL parsers. For comprehensive visual diagrams showing the complete data flow, architecture, and decision trees, see **[Visual Flow Diagrams](../user-guide/visual-flow-diagrams.md)**.

## Overview

OPAL uses several interconnected workflows:

- **Parser Selection**: Automatic detection based on URL patterns
- **URL Collection**: Site-specific pagination and link discovery  
- **Data Extraction**: HTML parsing and content extraction
- **Court Searching**: Advanced portal navigation and filtering
- **Error Handling**: Graceful fallbacks and retry logic

## Key Workflow Components

### 1. Court ID Discovery

The CourtSearchBuilder automatically discovers available courts:

1. **Navigation**: Load the court portal search page
2. **Element Detection**: Locate court selection dropdowns  
3. **Data Extraction**: Parse option elements for court names and IDs
4. **Fallback Strategy**: Use known court IDs if discovery fails

### 2. Search URL Building

For court extractor operations:

1. **Parameter Validation**: Verify court type, dates, filters
2. **URL Construction**: Build search URLs with proper parameters
3. **Session Management**: Handle portal session requirements
4. **Result Pagination**: Generate URLs for all result pages

### 3. Data Processing Pipeline

For all parser types:

1. **URL Collection**: Gather all target URLs for processing
2. **Content Extraction**: Parse HTML and extract structured data  
3. **Data Validation**: Verify extracted fields meet requirements
4. **Output Generation**: Format data as JSON/CSV with timestamps

## Implementation Details

### Parser Factory Pattern

```python
def get_parser(url, parser_name):
    """Select appropriate parser based on URL and name"""
    if 'appealscourts.gov' in url:
        return ParserAppealsAL()
    elif '1819news.com' in url:
        return Parser1819()
    # ... other parsers
```

### Error Recovery

- **Network Issues**: Exponential backoff with retry limits
- **Element Detection**: Alternative selector strategies  
- **Browser Crashes**: Automatic driver restart
- **Rate Limiting**: Adaptive delay mechanisms

## Visual References

For complete visual representations of these workflows:

- **📊 [Visual Flow Diagrams](../user-guide/visual-flow-diagrams.md)** - Comprehensive system diagrams
- **🔧 [Architecture Overview](architecture.md)** - System components and relationships
- **⚠️ [Error Handling](error_handling.md)** - Error recovery strategies

## Development Guidelines

When extending workflows:

1. Follow the established parser inheritance pattern
2. Implement proper error handling with fallbacks
3. Add appropriate logging for debugging
4. Consider rate limiting for respectful scraping
5. Update visual diagrams when adding new flows

## Testing Workflows

```bash
# Test court discovery
python -c "from opal.configurable_court_extractor import CourtSearchBuilder; CourtSearchBuilder().discover_court_ids()"

# Test parser selection  
python -c "from opal.main import get_parser; print(get_parser('https://1819news.com/', 'Parser1819'))"

# Validate search URL building
python -m opal.configurable_court_extractor --court civil --date-period 7d --dry-run
```