# Configuration

OPAL can be configured through command-line arguments and environment variables.

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

### Court Parser

- Automatically handles Chrome WebDriver setup
- Processes all available court cases
- No pagination parameters needed

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