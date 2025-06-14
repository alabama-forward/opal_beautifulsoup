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

### Scraping Court Records (ParserAppealsAL)

Basic court case extraction:

```bash
python -m opal \
    --url https://publicportal.alappeals.gov/portal/search/case/results \
    --parser court \
    --output court_cases.json
```

**Note**: For advanced court extraction with search filters, use the [Configurable Court Extractor](configurable_court_extractor.md) instead.

## ParserAppealsAL CLI Guide

The ParserAppealsAL parser (`--parser court`) is specifically designed for extracting case data from the Alabama Appeals Court Public Portal.

### Basic Usage

```bash
python -m opal --url <COURT_URL> --parser court [OPTIONS]
```

### Supported URLs

The parser works with Alabama Appeals Court URLs:

- **Search Results**: `https://publicportal.alappeals.gov/portal/search/case/results?criteria=...`
- **Direct Case Pages**: Individual case detail pages from the portal

### Command Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--url` | Court portal URL | Required | See examples below |
| `--parser` | Must be `court` | Required | `court` |
| `--output` | Output JSON file | `opal_output.json` | `appeals_cases.json` |
| `--max_pages` | Max pages to process | `5` | `10` |
| `--log-level` | Logging verbosity | `INFO` | `DEBUG` |

### Usage Examples

#### Extract from Search Results

```bash
# Extract court cases from a search results URL
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..." \
    --parser court \
    --output alabama_appeals.json \
    --log-level INFO
```

#### Extract with Custom Output

```bash
# Save to specific file with detailed logging
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser court \
    --output civil_appeals_2024.json \
    --log-level DEBUG
```

#### Limit Page Processing

```bash
# Process only first 3 pages of results
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser court \
    --max_pages 3 \
    --output limited_results.json
```

### What Gets Extracted

The ParserAppealsAL extracts the following information for each case:

- **Case Number**: Full case identifier and detail link
- **Case Title**: Complete case title/name
- **Court**: Which Appeals Court (Civil, Criminal, Supreme)
- **Classification**: Case type (Appeal, Certiorari, etc.)
- **Filing Date**: When the case was filed
- **Status**: Current case status (Open, Closed, etc.)

### Output Format

```json
{
  "cases": [
    {
      "court": "Alabama Civil Court of Appeals",
      "case_number": {
        "text": "CL-2024-0123",
        "link": "/portal/case/detail/12345"
      },
      "case_title": "Smith v. Jones Corp.",
      "classification": "Appeal",
      "filed_date": "01/15/2024",
      "status": "Open"
    }
  ],
  "metadata": {
    "extraction_date": "2024-01-20",
    "extraction_time": "14:30:22",
    "total_cases": 25,
    "pages_processed": 3,
    "parser": "ParserAppealsAL"
  }
}
```

### Performance Tips

1. **Use Specific URLs**: Direct search result URLs work better than general portal URLs
2. **Limit Pages**: Use `--max_pages` for faster processing of large result sets
3. **Enable Debug Logging**: Use `--log-level DEBUG` to monitor progress
4. **Check Output**: Verify results in the generated JSON file

### Common Issues and Solutions

#### Issue: "No cases found"
**Solution**: Ensure the URL contains actual search results with cases displayed

#### Issue: "Driver errors"
**Solution**: Make sure Chrome browser is installed and updated

#### Issue: "Slow processing"
**Solution**: Use `--max_pages` to limit the number of pages processed

### Advanced Usage

For more advanced court case extraction with search parameters, date filtering, and case categorization, use the dedicated [Configurable Court Extractor](configurable_court_extractor.md):

```bash
# Advanced extraction with search filters
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period 1m \
    --case-category Appeal \
    --max-pages 10
```

### Integration with Other Tools

#### Processing Results with jq

```bash
# Extract just case numbers
python -m opal --url "..." --parser court --output cases.json
cat cases.json | jq '.cases[].case_number.text'

# Count cases by status
cat cases.json | jq '.cases | group_by(.status) | map({status: .[0].status, count: length})'
```

#### Converting to CSV

```bash
# Use the configurable extractor for direct CSV output
python -m opal.configurable_court_extractor --court civil --format csv
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