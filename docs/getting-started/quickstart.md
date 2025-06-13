# Quick Start

This guide will help you get started with OPAL quickly.

## Basic Usage

### News Scraping

To scrape news articles from 1819news.com:

```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5
```

### Court Records Scraping

To scrape court cases from Alabama Appeals Court:

```bash
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court
```

## Common Options

- `--url`: The base URL to scrape
- `--parser`: The parser to use (Parser1819, ParserDailyNews, court)
- `--suffix`: URL suffix for news articles
- `--max_pages`: Maximum number of pages to scrape
- `--output`: Output file path (default: opal_output.json)

## Next Steps

- Read the [CLI Usage Guide](../user-guide/cli-usage.md) for detailed command options
- Check [Available Parsers](../user-guide/parsers.md) for all supported websites
- Learn about [Output Formats](../user-guide/output-formats.md) for data analysis