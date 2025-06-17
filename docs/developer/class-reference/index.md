---
title: Class Reference
description: Detailed documentation of OPAL's core classes and their methods
---

# Class Reference

This section provides comprehensive documentation for all core classes in the OPAL system. Each class is designed with specific responsibilities following object-oriented principles.

## Core Classes Overview

### Parser Classes

| Class | Module | Description |
|-------|--------|-------------|
| [BaseParser](./base-parser.md) | `opal.base_parser` | Abstract base class for all parsers |
| [ParserAppealsAL](./parser-appeals-al.md) | `opal.parser_module` | Alabama Appeals Court parser |
| [Parser1819](./parser-1819.md) | `opal.parser_module` | 1819 News parser |
| [ParserDailyNews](./parser-daily-news.md) | `opal.parser_module` | Daily news sites parser |

### Extractor Classes

| Class | Module | Description |
|-------|--------|-------------|
| [ConfigurableCourtExtractor](./configurable-court-extractor.md) | `opal.configurable_court_extractor` | Flexible court data extractor |
| [CourtExtractor](./court-extractor.md) | `opal.court_case_parser` | Core extraction logic |
| [URLPaginator](./url-paginator.md) | `opal.court_url_paginator` | Handles pagination |

### Data Structures

| Class | Module | Description |
|-------|--------|-------------|
| [CourtCase](./court-case.md) | `opal.data_structures` | Court case data model |
| [ParseResult](./parse-result.md) | `opal.data_structures` | Parser result container |
| [ExtractorConfig](./extractor-config.md) | `opal.data_structures` | Configuration model |

## Class Hierarchy

```
BaseParser (Abstract)
├── ParserAppealsAL
├── Parser1819
└── ParserDailyNews

Extractor (Abstract)
├── ConfigurableCourtExtractor
└── CourtExtractor

DataModel (Abstract)
├── CourtCase
├── ParseResult
└── ExtractorConfig
```

## Design Patterns

### Factory Pattern
Used for creating parser instances based on command-line arguments:

```python
def create_parser(parser_type: str) -> BaseParser:
    parsers = {
        'appeals-al': ParserAppealsAL,
        'parser-1819': Parser1819,
        'daily-news': ParserDailyNews
    }
    return parsers[parser_type]()
```

### Strategy Pattern
Extractors use different strategies for different content types:

```python
class ExtractionStrategy:
    def extract(self, soup: BeautifulSoup) -> dict:
        pass

class TableExtractionStrategy(ExtractionStrategy):
    def extract(self, soup: BeautifulSoup) -> dict:
        # Table-specific extraction
        pass
```

### Template Method Pattern
BaseParser defines the parsing workflow:

```python
class BaseParser:
    def parse(self):
        self.setup()
        data = self.extract_data()
        self.validate(data)
        return self.format_output(data)
```

## Common Interfaces

### Parser Interface
All parsers implement these methods:

- `parse(start_date, end_date)` - Main parsing method
- `validate_date_range(start_date, end_date)` - Date validation
- `format_output(data)` - Output formatting
- `save_results(data, format, filename)` - Result persistence

### Extractor Interface
All extractors implement:

- `extract(url)` - Extract data from URL
- `parse_content(html)` - Parse HTML content
- `validate_data(data)` - Validate extracted data
- `transform_data(data)` - Transform to standard format

## Usage Examples

### Creating a Parser
```python
from opal.parser_module import ParserAppealsAL

parser = ParserAppealsAL()
results = parser.parse(
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Using an Extractor
```python
from opal.configurable_court_extractor import ConfigurableCourtExtractor

extractor = ConfigurableCourtExtractor(config)
court_cases = extractor.extract("https://example.com/cases")
```

## Extension Points

### Custom Parser Creation
1. Inherit from `BaseParser`
2. Override required methods
3. Register in parser factory
4. Add command-line integration

### Custom Extractor Creation
1. Inherit from base extractor
2. Implement extraction logic
3. Define data mappings
4. Add validation rules

## Best Practices

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Implement retry logic for network issues
- Log errors appropriately

### Performance
- Implement caching where appropriate
- Use connection pooling
- Respect rate limits
- Optimize parsing algorithms

### Testing
- Mock external dependencies
- Test edge cases
- Validate data transformations
- Ensure thread safety

## Next Steps

- Review individual [class documentation](./base-parser.md)
- Learn about [creating custom parsers](../creating-custom-parsers.md)
- Explore [architecture patterns](../architecture.md)