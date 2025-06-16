---
layout: default
title: "CLI Reference"
---

# CLI Reference

OPAL provides command-line tools for scraping Alabama news sites and court records. For the easiest way to build commands, use our **[Interactive Command Builder](command-builder.md)** which provides a visual interface with examples and real-time validation.

## Command Structure

### Basic Syntax
```bash
python -m opal --url <URL> --parser <PARSER> [OPTIONS]
```

### Available Tools

1. **Main OPAL CLI** - For news articles and basic court scraping
   ```bash
   python -m opal --url <URL> --parser <PARSER> [options]
   ```

2. **Configurable Court Extractor** - For advanced court searches with filters
   ```bash
   python -m opal.configurable_court_extractor --court <TYPE> [options]
   ```

## Common Examples

### News Scraping

**1819 News Articles:**
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5
```

**Alabama Daily News:**
```bash
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 3
```

### Court Records

**Basic Court Scraping:**
```bash
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL
```

**Advanced Court Search:**
```bash
# Last 7 days of civil cases, excluding closed
python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed

# Last month of criminal cases, CSV output
python -m opal.configurable_court_extractor --court criminal --date-period 1m --output-csv
```

## Complete Parameter Reference

### Main OPAL Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `--url` | Base URL of the website to scrape | Yes | `https://1819news.com/` |
| `--parser` | Parser to use (`Parser1819`, `ParserDailyNews`, `ParserAppealsAL`) | Yes | `Parser1819` |
| `--suffix` | URL suffix to filter articles | No | `/news/item` |
| `--max_pages` | Maximum number of pages to scrape | No | `5` |

### Court Extractor Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--court` | Court type (`civil`, `criminal`, `all`) | `all` | `civil` |
| `--date-period` | Time period (`7d`, `1m`, `3m`, `6m`, `1y`) | `1m` | `7d` |
| `--exclude-closed` | Exclude closed cases | False | `--exclude-closed` |
| `--output-csv` | Also save as CSV file | False | `--output-csv` |
| `--case-number` | Search specific case number | None | `2024-CA-001` |
| `--filed-after` | Cases filed after date (YYYY-MM-DD) | None | `2024-01-01` |
| `--filed-before` | Cases filed before date (YYYY-MM-DD) | None | `2024-12-31` |

## Getting Help

### Command-Line Help
```bash
# Main OPAL help
python -m opal --help

# Court extractor help
python -m opal.configurable_court_extractor --help
```

### Interactive Resources
- **🛠️ [Interactive Command Builder](command-builder.md)** - Build commands visually with examples
- **📋 [Common Use Cases](common-use-cases.md)** - Real-world scenarios and workflows
- **💾 [Output Examples](output-examples.md)** - See what data you'll get
- **🚀 [Quick Start Tutorial](../getting-started/quickstart-tutorial.md)** - Step-by-step first scrape

## Tips and Best Practices

1. **Start Small**: Use `--max_pages 1` when testing to verify your command works
2. **Use Suffixes**: For news sites, use `--suffix` to filter only article pages
3. **Check Output**: Review the JSON output format in [Output Examples](output-examples.md)
4. **Rate Limiting**: The court scraper includes automatic delays to respect server limits
5. **Virtual Environment**: Always run OPAL in a virtual environment to avoid conflicts

## Troubleshooting

If you encounter errors:
1. Check your URL is correct and accessible
2. Verify you're using the right parser for your target site
3. Ensure Chrome is installed (for court scraping)
4. See [Understanding Errors](understanding-errors.md) for detailed error explanations