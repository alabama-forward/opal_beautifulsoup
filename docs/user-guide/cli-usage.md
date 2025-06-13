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
| `--parser` | Parser to use | `Parser1819`, `ParserDailyNews`, `court` |

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

### Scraping Court Records

```bash
python -m opal \
    --url https://publicportal.alappeals.gov/portal/search/case/results \
    --parser court \
    --output court_cases.json
```

## Output

All scraped data is saved in JSON format with the following structure:

```json
{
  "results": [
    {
      "title": "Article Title",
      "content": "Article content...",
      "date": "2024-01-01",
      "url": "https://example.com/article"
    }
  ],
  "metadata": {
    "source": "Parser1819",
    "scraped_at": "2024-01-01T12:00:00",
    "total_items": 25
  }
}
```