# Architecture

OPAL follows a modular architecture that makes it easy to add new parsers and extend functionality.

## Core Components

### BaseParser

The foundation of all parsers, providing:
- Common web scraping functionality
- Error handling and retry logic
- Logging infrastructure
- Output formatting

### Parser Classes

Each website has its own parser class that inherits from BaseParser:
- `Parser1819`: For 1819 News
- `ParserDailyNews`: For Alabama Daily News
- `ParserAppealsAL`: For Alabama Appeals Court

### Main Module

The `__main__.py` module handles:
- Command-line argument parsing
- Parser instantiation
- Execution flow
- Output management

## Class Hierarchy

```
BaseParser
├── Parser1819
├── ParserDailyNews
└── ParserAppealsAL
```

## Data Flow

1. **Input**: User provides URL and parser type via CLI
2. **Initialization**: Main module creates parser instance
3. **Scraping**: Parser fetches and processes web pages
4. **Extraction**: Parser extracts structured data
5. **Output**: Data saved to JSON file

## Key Design Patterns

### Template Method Pattern

BaseParser defines the scraping workflow:
```python
class BaseParser:
    def scrape(self):
        self.setup()
        data = self.extract_data()
        self.save_output(data)
```

### Factory Pattern

Parser selection based on command-line argument:
```python
parsers = {
    'Parser1819': Parser1819,
    'ParserDailyNews': ParserDailyNews,
    'court': ParserAppealsAL
}
parser_class = parsers[args.parser]
```

## Extension Points

### Adding New Parsers

1. Create new class inheriting from BaseParser
2. Implement required methods:
   - `extract_article_data()`
   - `get_article_links()`
   - `parse_article()`
3. Register in main module

### Customizing Output

Override `format_output()` method to customize data structure.

### Adding Features

- Authentication: Add login methods
- Caching: Implement request caching
- Rate limiting: Add delay mechanisms