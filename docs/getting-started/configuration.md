# Configuration

OPAL can be configured through command-line arguments, environment variables, and parser-specific options.

## Command-Line Arguments

### Required Arguments

- `--url`: The base URL to scrape
- `--parser`: The parser to use (Parser1819, ParserDailyNews, court)

### Optional Arguments

- `--suffix`: URL suffix for news articles (default: '')
- `--max_pages`: Maximum number of pages to scrape (default: 5)
- `--output`: Output file path (default: opal_output.json)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Parser-Specific Configuration

### News Parsers (Parser1819, ParserDailyNews)

- Require `--suffix` parameter for article URLs
- Support pagination with `--max_pages`

### Court Parser (ParserAppealsAL)

Basic configuration:
- Automatically handles Chrome WebDriver setup
- Processes all available court cases
- No pagination parameters needed

Advanced configuration options:
- `headless` (bool): Run browser in headless mode (default: True)
- `rate_limit_seconds` (int): Delay between requests (default: 3)

```python
from opal.court_case_parser import ParserAppealsAL

parser = ParserAppealsAL(
    headless=True,              # Run without visible browser
    rate_limit_seconds=2        # 2 second delay between pages
)
```

### Chrome WebDriver Options

The court parser configures Chrome with these options:
- `--disable-gpu`: Disable GPU hardware acceleration
- `--no-sandbox`: Required for some environments
- `--disable-dev-shm-usage`: Overcome limited resource problems
- `--window-size=1920,1080`: Set browser window size

Custom WebDriver options can be set:

```python
from selenium import webdriver
from opal.court_case_parser import ParserAppealsAL

# Custom Chrome options would need to be set in the parser's _setup_driver method
# The parser uses webdriver_manager for automatic ChromeDriver management
```

### Configurable Court Extractor

The configurable court extractor supports additional parameters through the main function:

```python
from opal.configurable_court_extractor import extract_court_cases_with_params

results = extract_court_cases_with_params(
    court="civil",              # Court selection
    date_period="1m",           # Date filtering
    case_category="Appeal",     # Case type filtering
    max_pages=10,               # Limit pages processed
    output_prefix="custom"      # Output file prefix
)
```

See [Configurable Court Extractor](../configurable_court_extractor.md) for detailed configuration options.

## Output Configuration

By default, OPAL outputs data in JSON format to `opal_output.json`. You can specify a different output file:

```bash
python -m opal --url https://example.com --parser Parser1819 --output my_data.json
```

## Logging

Control logging verbosity with `--log-level`:

```bash
python -m opal --url https://example.com --parser Parser1819 --log-level DEBUG
```