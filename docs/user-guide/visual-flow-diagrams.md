# Visual Flow Diagrams

This page provides visual diagrams to help you understand how OPAL works internally. These flowcharts show the data flow, decision processes, and system architecture.

## OPAL System Overview

```mermaid
graph TD
    A[User Command] --> B{Parser Type?}
    B -->|News| C[News Parser Flow]
    B -->|Court| D[Court Parser Flow]
    
    C --> E[URL Collection]
    E --> F[Article Extraction]
    F --> G[JSON Output]
    
    D --> H[Court Portal Access]
    H --> I[Case Data Extraction]
    I --> J[JSON + CSV Output]
    
    G --> K[Data Analysis]
    J --> K
    K --> L[Insights & Reports]
```

## Data Flow Architecture

### News Scraping Flow

```mermaid
graph TD
    A[Website URL] --> B[BaseParser Detection]
    B --> C{Which Parser?}
    
    C -->|1819news.com| D[Parser1819]
    C -->|aldailynews.com| E[ParserDailyNews]
    C -->|Other| F[Generic Parser]
    
    D --> G[URL Collection Module]
    E --> G
    F --> G
    
    G --> H[Paginate Website]
    H --> I[Extract Article URLs]
    I --> J[Filter by Suffix]
    J --> K[Process Each Article]
    
    K --> L[Parse HTML]
    L --> M[Extract: Title, Author, Date, Content]
    M --> N[Validate Data]
    N --> O[Add to Results]
    
    O --> P{More Articles?}
    P -->|Yes| K
    P -->|No| Q[Generate JSON Output]
    
    Q --> R[Save to File]
    R --> S[Display Summary]
```

### Court Scraping Flow

```mermaid
graph TD
    A[Court Portal URL] --> B[Launch Chrome Browser]
    B --> C[Navigate to Search Page]
    C --> D[Wait for JavaScript Load]
    D --> E[Discover Court IDs]
    
    E --> F{Search Method?}
    F -->|Custom URL| G[Use Provided URL]
    F -->|Parameters| H[Build Search URL]
    
    H --> I[CourtSearchBuilder]
    I --> J[Set Court Type]
    J --> K[Set Date Range]
    K --> L[Set Filters]
    L --> M[Generate URL]
    
    G --> N[Load First Page]
    M --> N
    
    N --> O[Extract Page Count]
    O --> P[Generate All Page URLs]
    P --> Q[Process Each Page]
    
    Q --> R[Parse HTML Table]
    R --> S[Extract Case Data]
    S --> T[Validate Fields]
    T --> U[Add to Results]
    
    U --> V{More Pages?}
    V -->|Yes| Q
    V -->|No| W[Close Browser]
    
    W --> X[Generate JSON Output]
    X --> Y[Generate CSV Output]
    Y --> Z[Display Summary]
```

## Parser Selection Decision Tree

```mermaid
graph TD
    A[Start: User Provides URL] --> B{URL Contains?}
    
    B -->|1819news.com| C[Use Parser1819]
    B -->|aldailynews.com| D[Use ParserDailyNews]
    B -->|publicportal.alappeals.gov| E[Use ParserAppealsAL]
    B -->|Other| F[Error: Unsupported Site]
    
    C --> G[News Scraping Mode]
    D --> G
    E --> H[Court Scraping Mode]
    F --> I[Show Supported Sites]
    
    G --> J[Requires: --suffix parameter]
    H --> K[Requires: Chrome Browser]
    
    J --> L[Output: JSON with articles]
    K --> M[Output: JSON + CSV with cases]
```

## Pagination Handling

### News Site Pagination

```mermaid
graph TD
    A[Start: Base URL] --> B[Load Homepage]
    B --> C[Discover Navigation Pattern]
    C --> D{Pagination Type?}
    
    D -->|URL Parameters| E[Extract Page Numbers]
    D -->|Next/Previous Links| F[Follow Link Pattern]
    D -->|Load More Button| G[Simulate Clicks]
    
    E --> H[Generate Page URLs]
    F --> I[Crawl Sequential Pages]
    G --> J[Dynamic Loading]
    
    H --> K[Process All Pages]
    I --> K
    J --> K
    
    K --> L[Extract Article URLs]
    L --> M[Filter by Suffix]
    M --> N[Remove Duplicates]
    N --> O[Return URL List]
```

### Court Portal Pagination

```mermaid
graph TD
    A[Search Results URL] --> B[Parse URL Parameters]
    B --> C[Extract: criteria, page, size]
    C --> D[Determine Total Pages]
    
    D --> E{How Many Pages?}
    E -->|1 Page| F[Process Single Page]
    E -->|Multiple| G[Generate Page URLs]
    
    F --> H[Extract Cases]
    G --> I[For Each Page]
    
    I --> J[Update Page Parameter]
    J --> K[Load Page with Selenium]
    K --> L[Wait for Content]
    L --> M[Extract Cases]
    M --> N{More Pages?}
    
    N -->|Yes| I
    N -->|No| O[Combine All Results]
    
    H --> P[Return Cases]
    O --> P
```

## Data Transformation Process

### News Article Transformation

```mermaid
graph LR
    A[Raw HTML] --> B[BeautifulSoup Parse]
    B --> C[Element Selection]
    C --> D[Text Extraction]
    D --> E[Data Cleaning]
    E --> F[Structure Creation]
    
    subgraph "Before"
        G["<article><h1>Title</h1><p>Content...</p></article>"]
    end
    
    subgraph "After"
        H["{\n  'title': 'Title',\n  'content': 'Content...',\n  'author': 'Author',\n  'date': '2024-01-15'\n}"]
    end
    
    A -.-> G
    F -.-> H
```

### Court Case Transformation

```mermaid
graph LR
    A[HTML Table] --> B[Row Extraction]
    B --> C[Cell Processing]
    C --> D[Link Extraction]
    D --> E[Date Parsing]
    E --> F[JSON Structure]
    
    subgraph "Before"
        G["<tr><td>CL-2024-001</td><td>Case Title</td></tr>"]
    end
    
    subgraph "After"
        H["{\n  'case_number': {\n    'text': 'CL-2024-001',\n    'link': '/case/detail/123'\n  },\n  'case_title': 'Case Title'\n}"]
    end
    
    A -.-> G
    F -.-> H
```

## Error Handling Flow

```mermaid
graph TD
    A[Operation Start] --> B{Error Occurred?}
    B -->|No| C[Continue Processing]
    B -->|Yes| D{Error Type?}
    
    D -->|Network| E[Retry with Backoff]
    D -->|Element Not Found| F[Try Alternative Selector]
    D -->|Browser Crash| G[Restart Browser]
    D -->|Permission| H[Check File Access]
    D -->|Rate Limit| I[Wait and Retry]
    
    E --> J{Retry Successful?}
    F --> K{Alternative Found?}
    G --> L[Reinitialize Driver]
    H --> M[Change Output Location]
    I --> N[Resume Processing]
    
    J -->|Yes| C
    J -->|No| O[Log Error & Continue]
    K -->|Yes| C
    K -->|No| O
    L --> C
    M --> C
    N --> C
    
    C --> P[Complete Successfully]
    O --> Q[Partial Success]
```

## Integration Architecture

```mermaid
graph TD
    A[CLI Interface] --> B[main.py]
    B --> C[IntegratedParser]
    C --> D{URL Analysis}
    
    D -->|News URL| E[url_catcher_module]
    D -->|Court URL| F[court_url_paginator]
    
    E --> G[BaseParser Classes]
    F --> H[ParserAppealsAL]
    
    G --> I[Parser1819]
    G --> J[ParserDailyNews]
    
    I --> K[Article Processing]
    J --> K
    H --> L[Case Processing]
    
    K --> M[JSON Output]
    L --> N[JSON + CSV Output]
    
    M --> O[File System]
    N --> O
    
    subgraph "Configuration"
        P[CourtSearchBuilder]
        Q[Search Parameters]
        R[URL Building]
    end
    
    F --> P
    P --> Q
    Q --> R
    R --> H
```

## Performance Optimization Flow

```mermaid
graph TD
    A[Start Scraping] --> B[Check Rate Limits]
    B --> C[Monitor Memory Usage]
    C --> D[Process in Batches]
    
    D --> E{Resource Check}
    E -->|OK| F[Continue Processing]
    E -->|High Memory| G[Clear Cache]
    E -->|Rate Limited| H[Implement Delay]
    
    F --> I[Extract Data]
    G --> J[Garbage Collection]
    H --> K[Wait Period]
    
    J --> F
    K --> F
    
    I --> L{More Data?}
    L -->|Yes| B
    L -->|No| M[Finalize Output]
    
    M --> N[Performance Report]
    N --> O[Complete]
```

## Command Processing Flow

```mermaid
graph TD
    A[User Command] --> B[Parse Arguments]
    B --> C[Validate Parameters]
    C --> D{Validation Result?}
    
    D -->|Valid| E[Initialize Components]
    D -->|Invalid| F[Show Error & Help]
    
    E --> G[Set Up Environment]
    G --> H[Check Prerequisites]
    H --> I{Prerequisites Met?}
    
    I -->|Yes| J[Execute Scraping]
    I -->|No| K[Show Requirements]
    
    J --> L[Monitor Progress]
    L --> M[Handle Errors]
    M --> N[Generate Output]
    N --> O[Display Results]
    
    F --> P[Exit with Error]
    K --> P
    O --> Q[Exit Successfully]
```

## Session Management (Court Scraping)

```mermaid
graph TD
    A[Court URL Provided] --> B{URL Type?}
    
    B -->|Fresh Search| C[Build New Session]
    B -->|Custom URL| D[Check Session Age]
    
    C --> E[Navigate to Portal]
    D --> F{Session Valid?}
    
    F -->|Yes| G[Use Existing Session]
    F -->|No| H[Warn User]
    F -->|Unknown| I[Attempt to Use]
    
    E --> J[Discover Court IDs]
    G --> K[Start Extraction]
    H --> L[Suggest New Search]
    I --> M[Monitor for Errors]
    
    J --> N[Build Search Parameters]
    N --> O[Generate Search URL]
    O --> K
    
    K --> P[Extract Data]
    M --> Q{Session Expired?}
    
    Q -->|Yes| L
    Q -->|No| P
    
    P --> R[Complete Successfully]
    L --> S[Exit with Message]
```

## Visual Summary

These diagrams show how OPAL:

1. **Processes different types of content** (news vs court data)
2. **Handles complex pagination** across different website structures  
3. **Makes intelligent parser selections** based on URL patterns
4. **Transforms raw HTML** into structured, usable data
5. **Manages errors gracefully** with fallback strategies
6. **Optimizes performance** through batching and rate limiting
7. **Handles browser sessions** for JavaScript-heavy sites

Understanding these flows helps you:
- **Debug issues** by following the process step-by-step
- **Optimize your scraping** by understanding bottlenecks
- **Extend OPAL** by knowing where to add new functionality
- **Troubleshoot errors** by identifying which component failed

For more technical details, see the [Developer Guide](../developer/architecture.md).

For practical usage examples, see [Common Use Cases](common-use-cases.md).