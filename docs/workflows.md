# Workflows

This document describes the internal workflows and processing patterns used by OPAL parsers, particularly focusing on the court parsing system.

## Court ID Discovery Workflow

The CourtSearchBuilder automatically discovers available courts and their IDs from the Alabama Appeals Court portal:

```mermaid
graph TD
    A[Navigate to Search Page] --> B[Wait for Page Load]
    B --> C{Court Elements Found?}
    C -->|Yes| D[Extract Court Options]
    C -->|No| E[Use Fallback IDs]
    D --> F[Parse Court Names and IDs]
    F --> G[Store Court Mapping]
    E --> G
```

### Implementation Details

1. **Navigation**: Load `https://publicportal.alappeals.gov/portal/search/case`
2. **Element Detection**: Look for court selection elements
3. **Data Extraction**: Parse option elements for court names and values
4. **Fallback Strategy**: Use known court ID for civil court if discovery fails

```python
# Actual implementation in CourtSearchBuilder
def discover_court_ids(self, parser_instance):
    try:
        # Navigate to search page
        parser_instance.driver.get("https://publicportal.alappeals.gov/portal/search/case")
        
        # Wait for page load
        time.sleep(3)
        
        # Try to find court selection elements
        court_elements = parser_instance.driver.find_elements(
            By.XPATH, 
            "//select[@id='court'] | //select[contains(@name, 'court')] | //div[contains(@class, 'court')]"
        )
        
        if court_elements:
            # Extract court IDs from dropdown options
            for element in court_elements:
                options = element.find_elements(By.TAG_NAME, "option")
                for option in options:
                    court_name = option.text.lower()
                    court_id = option.get_attribute("value")
                    
                    # Map court names to internal keys
                    if "civil" in court_name and "appeals" in court_name:
                        self.courts['civil']['id'] = court_id
                    elif "criminal" in court_name and "appeals" in court_name:
                        self.courts['criminal']['id'] = court_id
                    elif "supreme" in court_name:
                        self.courts['supreme']['id'] = court_id
        else:
            # Use known working ID for civil court
            self.courts['civil']['id'] = '68f021c4-6a44-4735-9a76-5360b2e8af13'
            
    except Exception as e:
        # Fallback to known civil court ID
        self.courts['civil']['id'] = '68f021c4-6a44-4735-9a76-5360b2e8af13'
```

## Dynamic Pagination Workflow

The system handles JavaScript-based pagination:

```mermaid
graph TD
    A[Load First Page] --> B[Extract Current URL]
    B --> C[Parse Page Info from URL]
    C --> D{Total Pages > 1?}
    D -->|Yes| E[Generate Page URLs]
    D -->|No| F[Process Single Page]
    E --> G[Process Each Page]
    G --> H[Aggregate Results]
    F --> H
```

### Steps:

1. **Initial Load**: Load search results first page
2. **URL Analysis**: Extract pagination data from JavaScript-updated URL
3. **Page Generation**: Create URLs for all result pages
4. **Sequential Processing**: Load and extract data from each page
5. **Result Aggregation**: Combine all extracted cases

## Session Management Workflow

Handling session-based URLs and expiration:

```mermaid
graph TD
    A[Receive Custom URL] --> B{Check URL Age}
    B -->|Fresh| C[Use URL Directly]
    B -->|Possibly Expired| D[Warn User]
    D --> E{User Proceeds?}
    E -->|Yes| C
    E -->|No| F[Request New Search]
    C --> G[Process Results]
    G --> H{Session Valid?}
    H -->|Yes| I[Continue Processing]
    H -->|No| J[Session Expired Error]
```

### Key Considerations:

- URLs contain session tokens that expire after ~30 minutes
- System warns users about potentially expired URLs
- Provides clear error messages when sessions expire
- Suggests creating new search for expired sessions

## Error Recovery Workflow

Robust error handling throughout the extraction process:

```mermaid
graph TD
    A[Start Extraction] --> B{Error Occurred?}
    B -->|No| C[Continue Processing]
    B -->|Yes| D{Error Type}
    D -->|Timeout| E[Retry with Backoff]
    D -->|Element Not Found| F[Skip and Log]
    D -->|Driver Crash| G[Restart Driver]
    D -->|Network Error| H[Wait and Retry]
    E --> I{Retry Successful?}
    I -->|Yes| C
    I -->|No| J[Log Error and Continue]
    F --> J
    G --> K[Reinitialize and Resume]
    H --> I
```

### Error Types and Handling:

1. **Selenium Timeouts**: Retry with exponential backoff
2. **Stale Elements**: Re-locate elements before interaction
3. **Driver Crashes**: Restart driver and resume from last page
4. **Network Errors**: Implement retry logic with delays

## Data Extraction Workflow

Extracting case information from court pages:

```mermaid
graph TD
    A[Page Loaded] --> B[Locate Case Table]
    B --> C[Find All Case Rows]
    C --> D[For Each Row]
    D --> E[Extract Case Number]
    E --> F[Extract Case Link]
    F --> G[Extract Case Title]
    G --> H[Extract Metadata]
    H --> I[Validate Data]
    I --> J{Valid?}
    J -->|Yes| K[Add to Results]
    J -->|No| L[Log Warning]
    K --> M{More Rows?}
    L --> M
    M -->|Yes| D
    M -->|No| N[Return Results]
```

### Data Points Extracted:

- Case number and detail link
- Case title
- Court name
- Classification/type
- Filing date
- Current status

## Integration Workflow

How OPAL components work together:

```mermaid
graph TD
    A[User Request] --> B{Use Custom URL?}
    B -->|Yes| C[extract_court_cases_with_params with custom_url]
    B -->|No| D[CourtSearchBuilder]
    D --> E[discover_court_ids with ParserAppealsAL]
    E --> F[Build Search Parameters]
    F --> G[build_url]
    C --> H[ParserAppealsAL.parse_article]
    G --> H
    H --> I[court_url_paginator functions]
    I --> J[Process All Pages]
    J --> K[Aggregate Results]
    K --> L[Generate JSON/CSV Output]
```

## Command-Line Workflow

Processing flow for CLI usage:

```mermaid
graph TD
    A[Parse CLI Arguments] --> B{URL Provided?}
    B -->|Yes| C[Use Custom URL Path]
    B -->|No| D[Validate Search Parameters]
    D --> E[extract_court_cases_with_params]
    C --> E
    E --> F[CourtSearchBuilder.discover_court_ids]
    F --> G[Build Search URL]
    G --> H[ParserAppealsAL Processing]
    H --> I[Paginate Results]
    I --> J[Save JSON Output]
    J --> K[Save CSV Output]
    K --> L[Display Summary]
```

## Performance Optimization Workflow

Strategies for efficient extraction:

1. **Batch Processing**
   - Process multiple pages concurrently where possible
   - Aggregate results before writing to disk

2. **Caching Strategy**
   - Cache court IDs after discovery
   - Reuse WebDriver instance across pages

3. **Rate Limiting**
   - Implement delays between requests
   - Respect server resources

4. **Memory Management**
   - Process large result sets in chunks
   - Clear driver cache periodically

## Testing Workflow

Ensuring reliability:

```mermaid
graph TD
    A[Unit Tests] --> B[Integration Tests]
    B --> C[End-to-End Tests]
    C --> D{All Pass?}
    D -->|Yes| E[Deploy]
    D -->|No| F[Fix Issues]
    F --> A
```

### Test Categories:

1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Component interaction
3. **End-to-End Tests**: Full extraction workflows
4. **Performance Tests**: Load and speed testing

## Debugging Workflow

Troubleshooting extraction issues:

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Run in Non-Headless Mode**
   ```python
   parser = ParserAppealsAL(headless=False)
   ```

3. **Add Breakpoints**
   - Inspect page state
   - Verify element selection
   - Check data extraction

4. **Save Screenshots**
   ```python
   driver.save_screenshot("debug_state.png")
   ```

5. **Export Page Source**
   ```python
   with open("page_source.html", "w") as f:
       f.write(driver.page_source)
   ```