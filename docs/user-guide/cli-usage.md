# CLI Usage

The OPAL command-line interface provides a simple way to scrape content from supported websites.

## Basic Command Structure

```bash
python -m opal --url <URL> --parser <PARSER> [OPTIONS]
```

## Arguments

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--url` | The base URL to scrape | `https://1819news.com/` |
| `--parser` | Parser to use | `Parser1819`, `ParserDailyNews`, `ParserAppealsAL` |

### Optional Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--suffix` | URL suffix for articles | `''` |
| `--max_pages` | Maximum pages to scrape | `5` |
| `--output` | Output file path | `opal_output.json` |
| `--log-level` | Logging level | `INFO` |

## Examples

### Scraping 1819 News

```bash
python -m opal \
    --url https://1819news.com/ \
    --parser Parser1819 \
    --suffix /news/item \
    --max_pages 10 \
    --output 1819_articles.json
```

### Scraping Alabama Daily News

```bash
python -m opal \
    --url https://www.aldailynews.com/ \
    --parser ParserDailyNews \
    --suffix /news/item \
    --max_pages 5
```

### Scraping Court Records (ParserAppealsAL)

Basic court case extraction:

```bash
python -m opal \
    --url https://publicportal.alappeals.gov/portal/search/case/results \
    --parser ParserAppealsAL \
    --output court_cases.json
```

**Note**: For advanced court extraction with search filters, use the [Configurable Court Extractor](configurable_court_extractor.md) instead.

For detailed court scraping examples and troubleshooting, see the [Quick Start Tutorial](../getting-started/quickstart-tutorial.md).

## Output

All scraped data is saved in JSON format. For detailed output examples and field explanations, see [Output Examples](output-examples.md).