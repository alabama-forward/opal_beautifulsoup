---
layout: default
title: "ParserAppealsAL CLI Reference"
---

# ParserAppealsAL CLI Reference

Complete command-line reference for the Alabama Appeals Court parser.

## Overview

ParserAppealsAL is the specialized parser for extracting case data from the Alabama Appeals Court Public Portal. It's accessed through the main OPAL CLI using `--parser ParserAppealsAL`.

## Quick Start

```bash
# Basic court case extraction
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL \
    --output my_cases.json
```

## Command Syntax

```bash
python -m opal --url <COURT_URL> --parser ParserAppealsAL [OPTIONS]
```

## Required Arguments

### `--url <URL>`
The Alabama Appeals Court portal URL to scrape.

**Supported URL Types:**
- Search results pages with case listings
- Individual case detail pages
- Paginated search results

**Examples:**
```bash
--url "https://publicportal.alappeals.gov/portal/search/case/results"
--url "https://publicportal.alappeals.gov/portal/search/case/results?criteria=..."
```

### `--parser ParserAppealsAL`
Specifies to use the ParserAppealsAL court parser.

**Must be exactly:** `ParserAppealsAL`

## Optional Arguments

### `--output <FILENAME>`
Specify the output JSON file path.

**Default:** `opal_output.json`

**Examples:**
```bash
--output court_cases.json
--output /path/to/appeals_data.json
--output "cases_$(date +%Y%m%d).json"
```

### `--max_pages <NUMBER>`
Limit the number of pages to process from paginated results.

**Default:** `5`  
**Range:** 1 or higher

**Examples:**
```bash
--max_pages 1      # Process only first page
--max_pages 10     # Process up to 10 pages
--max_pages 50     # Process up to 50 pages
```

### `--log-level <LEVEL>`
Set the logging verbosity level.

**Default:** `INFO`  
**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`

**Examples:**
```bash
--log-level DEBUG    # Detailed progress information
--log-level INFO     # Standard progress updates
--log-level WARNING  # Only warnings and errors
--log-level ERROR    # Only error messages
```

## Complete Examples

### Basic Extraction

```bash
# Extract court cases with default settings
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL
```

### Custom Output File

```bash
# Save to specific file
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL \
    --output alabama_appeals_2024.json
```

### Limited Page Processing

```bash
# Process only first 3 pages for faster results
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL \
    --max_pages 3 \
    --output quick_sample.json
```

### Debug Mode

```bash
# Enable detailed logging to monitor progress
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL \
    --log-level DEBUG \
    --output debug_cases.json
```

### Production Extraction

```bash
# Extract with timestamp in filename
python -m opal \
    --url "https://publicportal.alappeals.gov/portal/search/case/results" \
    --parser ParserAppealsAL \
    --max_pages 20 \
    --output "court_cases_$(date +%Y%m%d_%H%M%S).json" \
    --log-level INFO
```

## Output Structure

The parser generates JSON output with this structure:

```json
{
  "cases": [
    {
      "court": "Alabama Civil Court of Appeals",
      "case_number": {
        "text": "CL-2024-0123",
        "link": "/portal/case/detail/12345"
      },
      "case_title": "Smith v. Jones Corporation",
      "classification": "Appeal",
      "filed_date": "01/15/2024",
      "status": "Open"
    }
  ],
  "metadata": {
    "extraction_date": "2024-01-20",
    "extraction_time": "14:30:22", 
    "total_cases": 156,
    "pages_processed": 7,
    "parser": "ParserAppealsAL",
    "source_url": "https://publicportal.alappeals.gov/..."
  }
}
```

### Field Descriptions

**Case Fields:**
- `court`: Which Appeals Court handled the case
- `case_number.text`: The case identifier (e.g., "CL-2024-0123")
- `case_number.link`: Relative URL to case details page
- `case_title`: Full case title/name
- `classification`: Type of case (Appeal, Certiorari, etc.)
- `filed_date`: Date case was filed (MM/DD/YYYY format)
- `status`: Current case status (Open, Closed, etc.)

**Metadata Fields:**
- `extraction_date`: Date of extraction (YYYY-MM-DD)
- `extraction_time`: Time of extraction (HH:MM:SS)
- `total_cases`: Number of cases extracted
- `pages_processed`: Number of pages processed
- `parser`: Parser used (always "ParserAppealsAL")
- `source_url`: Original URL scraped

## Working with Results

### View Case Count

```bash
# Extract and show total cases
python -m opal --url "..." --parser ParserAppealsAL --output cases.json
cat cases.json | jq '.metadata.total_cases'
```

### Extract Specific Fields

```bash
# Get just case numbers
cat cases.json | jq '.cases[].case_number.text'

# Get case titles
cat cases.json | jq '.cases[].case_title'

# Get cases by status
cat cases.json | jq '.cases[] | select(.status == "Open")'
```

### Convert to CSV

```bash
# Basic CSV conversion
cat cases.json | jq -r '.cases[] | [.case_number.text, .case_title, .status, .filed_date] | @csv'

# CSV with headers
echo "Case Number,Title,Status,Filed Date" > cases.csv
cat cases.json | jq -r '.cases[] | [.case_number.text, .case_title, .status, .filed_date] | @csv' >> cases.csv
```

## Performance Considerations

### Processing Speed
- **Typical rate**: 1-2 pages per minute
- **Factors**: Network speed, page complexity, rate limiting
- **Recommendation**: Use `--max_pages` for initial testing

### Memory Usage
- **Low memory**: Processes pages sequentially
- **Scalable**: Can handle large result sets
- **Storage**: JSON output size varies by case count

### Rate Limiting
- **Built-in delays**: 3-second delays between requests
- **Respectful**: Designed not to overwhelm the server
- **Adjustable**: Modify in source code if needed

## Troubleshooting

### Common Issues

#### "No cases found"
**Cause**: URL doesn't contain case listings  
**Solution**: Verify URL shows cases in browser first

#### "WebDriver error"
**Cause**: Chrome browser not installed or outdated  
**Solution**: Install/update Chrome browser

#### "Connection timeout"
**Cause**: Network issues or server problems  
**Solution**: Check internet connection, try again later

#### "Permission denied writing output"
**Cause**: No write access to output directory  
**Solution**: Use different output path or fix permissions

### Debug Steps

1. **Test URL in browser**: Verify cases are visible
2. **Enable debug logging**: Use `--log-level DEBUG`
3. **Limit pages**: Use `--max_pages 1` for testing
4. **Check output**: Verify JSON file is created and valid

### Getting Help

If issues persist:
1. Check the [Error Handling Guide](../developer/error_handling.md)
2. Review [Troubleshooting Documentation](../developer/workflows.md)
3. Enable debug logging to see detailed error messages

## Advanced Usage

For more sophisticated court case extraction with search parameters, filtering, and automation, see:

- **[Configurable Court Extractor](configurable_court_extractor.md)**: Advanced search parameters
- **[Command Line Tools](command_line_tools.md)**: Complete CLI reference
- **[API Reference](../api_reference.md)**: Programmatic usage

## Comparison with Alternatives

| Feature | Basic CLI (`--parser ParserAppealsAL`) | Configurable Extractor |
|---------|------------------------------|------------------------|
| Search filters | ❌ None | ✅ Date, category, court, case number |
| Output formats | JSON only | JSON + CSV |
| Multiple courts | Single URL only | All courts in one command |
| Automation | Manual URLs | Parameterized searches |
| Complexity | Simple | Advanced |

**Recommendation**: Use basic CLI for simple extractions, Configurable Extractor for advanced needs.