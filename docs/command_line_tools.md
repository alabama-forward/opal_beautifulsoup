# Command Line Tools

OPAL provides several command-line tools for extracting court and news data. This document covers all available CLI interfaces.

## Main OPAL CLI

The primary command-line interface for OPAL:

```bash
python -m opal [options]
```

### Basic Usage

```bash
# Extract news articles
python -m opal --url https://alabamanewscenter.com --parser Parser1819 --suffix "/news/"

# Extract court cases (uses ParserAppealsAL automatically)
python -m opal --url https://publicportal.alappeals.gov --parser court
```

### Available Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--url` | Yes | Base URL to scrape | - |
| `--parser` | Yes | Parser type (Parser1819, ParserDailyNews, court) | - |
| `--suffix` | No | URL suffix for news articles | '' |
| `--max_pages` | No | Maximum pages to scrape | 5 |
| `--output` | No | Output file path | opal_output.json |
| `--log-level` | No | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |

## Configurable Court Extractor CLI

Advanced court data extraction with flexible search parameters:

```bash
python -m opal.configurable_court_extractor [options]
```

### Quick Examples

```bash
# Extract civil court cases from last 7 days
python -m opal.configurable_court_extractor --court civil --date-period 7d

# Extract criminal appeals with custom date range
python -m opal.configurable_court_extractor \
    --court criminal \
    --date-period custom \
    --start-date 2024-01-01 \
    --end-date 2024-01-31 \
    --case-category Appeal

# Extract supreme court cases excluding closed ones
python -m opal.configurable_court_extractor \
    --court supreme \
    --date-period 3m \
    --exclude-closed \
    --max-pages 20
```

### All Available Options

#### Court Selection
- `--court {civil,criminal,supreme}` - Court type to search

#### Date Filtering
- `--date-period {7d,1m,3m,6m,1y,custom}` - Predefined date periods
- `--start-date YYYY-MM-DD` - Start date (required with custom period)
- `--end-date YYYY-MM-DD` - End date (required with custom period)

#### Case Filtering
- `--case-number TEXT` - Filter by case number (supports wildcards)
- `--case-title TEXT` - Filter by case title
- `--case-category {Appeal,Certiorari,Original Proceeding,Petition,Certified Question}` - Filter by case type
- `--exclude-closed` - Exclude closed cases

#### Processing Options
- `--max-pages INT` - Maximum pages to process (default: unlimited)
- `--rate-limit FLOAT` - Seconds between requests (default: 1.0)
- `--headless` / `--no-headless` - Browser visibility (default: headless)

#### Output Options
- `--output-prefix TEXT` - Prefix for output files (default: court_cases)
- `--format {json,csv,both}` - Output format (default: both)

#### Advanced Options
- `--url TEXT` - Use custom URL instead of building search
- `--court-id INT` - Override automatic court ID discovery
- `--verbose` - Enable verbose logging

### Complete Example

```bash
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period custom \
    --start-date 2024-01-01 \
    --end-date 2024-03-31 \
    --case-category Appeal \
    --case-number "2024-*" \
    --exclude-closed \
    --max-pages 50 \
    --rate-limit 2.0 \
    --output-prefix "civil_appeals_q1_2024" \
    --format both \
    --verbose
```

This command:
- Searches civil court
- For cases filed January-March 2024
- Only appeals
- With case numbers starting with "2024-"
- Excluding closed cases
- Processing up to 50 pages
- With 2-second delays between requests
- Outputting both JSON and CSV
- With verbose logging

## Extract All Court Cases Script

Standalone script for extracting all available court cases:

```bash
python -m opal.extract_all_court_cases
```

### Features

- Extracts all court cases across all pages
- Hardcoded to handle known pagination (318 cases across 13 pages)
- Outputs both JSON and CSV formats
- Includes progress tracking
- Automatically verifies extraction completeness
- Uses ParserAppealsAL internally

### Output Files

- `all_court_cases_TIMESTAMP.json` - JSON format with metadata
- `all_court_cases_TIMESTAMP.csv` - CSV format for analysis

### Usage

```bash
# Extract all cases
python -m opal.extract_all_court_cases

# The script is self-contained and requires no parameters
# Rate limiting and pagination are handled automatically
```

## Integration with Other Tools

### Using with jq (JSON processing)

```bash
# Extract specific fields from court results
python -m opal.configurable_court_extractor --court civil --date-period 1m | \
    jq '.cases[] | {case_number: .case_number.text, title: .case_title}'

# Count cases by status
python -m opal.configurable_court_extractor --court civil --date-period 1m | \
    jq '.cases | group_by(.status) | map({status: .[0].status, count: length})'
```

### Using with csvkit (CSV processing)

```bash
# Generate CSV and analyze
python -m opal.configurable_court_extractor --court civil --format csv
csvstat court_cases.csv --count
csvcut -c case_title,status court_cases.csv | csvlook
```

### Piping to Other Commands

```bash
# Count total cases
python -m opal.configurable_court_extractor --court civil --format json | \
    jq '.total_cases'

# Extract case numbers only
python -m opal.configurable_court_extractor --court civil --format json | \
    jq -r '.cases[].case_number.text'
```

## Automation and Scripting

### Bash Script Example

```bash
#!/bin/bash
# extract_monthly_reports.sh

COURTS=("civil" "criminal" "supreme")
DATE=$(date +%Y-%m)

for court in "${COURTS[@]}"; do
    echo "Extracting $court court cases for $DATE"
    
    python -m opal.configurable_court_extractor \
        --court "$court" \
        --date-period 1m \
        --output-prefix "${court}_${DATE}" \
        --format both \
        --exclude-closed
    
    echo "Completed $court extraction"
done

echo "All extractions complete"
```

### Python Script Integration

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def extract_court_data(court_type, date_period="1m"):
    """Extract court data using CLI tool"""
    cmd = [
        "python", "-m", "opal.configurable_court_extractor",
        "--court", court_type,
        "--date-period", date_period
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # CLI saves to files, check for output files
        timestamp = datetime.now().strftime('%Y%m%d')
        json_file = f"court_cases_{timestamp}*.json"
        # Read the most recent output file
        import glob
        files = glob.glob(json_file)
        if files:
            with open(files[-1]) as f:
                return json.load(f)
    else:
        print(f"Error extracting {court_type}: {result.stderr}")
        return None

# Direct import approach (preferred)
from opal.configurable_court_extractor import extract_court_cases_with_params

def extract_court_data_direct(court_type, date_period="1m"):
    """Extract court data using direct function call"""
    return extract_court_cases_with_params(
        court=court_type,
        date_period=date_period,
        max_pages=5
    )

# Usage
for court in ["civil", "criminal", "supreme"]:
    data = extract_court_data_direct(court)
    if data and data['status'] == 'success':
        print(f"{court}: {data['total_cases']} cases found")
```

## Environment Variables

Control CLI behavior with environment variables:

```bash
# Set default output directory
export OPAL_OUTPUT_DIR="/path/to/outputs"

# Set default rate limiting
export OPAL_RATE_LIMIT=2.0

# Enable debug mode
export OPAL_DEBUG=1

# Set Chrome options
export OPAL_CHROME_OPTIONS="--proxy-server=proxy.example.com:8080"
```

## Error Handling and Debugging

### Verbose Output

Enable detailed logging:

```bash
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period 7d \
    --verbose
```

### Debug Mode

Run with debug logging:

```bash
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period 7d \
    --log-level DEBUG
```

### Non-Headless Mode

See browser activity:

```bash
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period 7d \
    --no-headless
```

## Performance Tips

### Optimize for Speed

```bash
# Use higher rate limiting for faster extraction
python -m opal.configurable_court_extractor \
    --court civil \
    --rate-limit 0.5 \
    --max-pages 10
```

### Optimize for Server Resources

```bash
# Be gentle with the server
python -m opal.configurable_court_extractor \
    --court civil \
    --rate-limit 3.0 \
    --max-pages 5
```

## Exit Codes

The CLI tools use standard exit codes:

- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Network error
- `4` - Parser error
- `5` - Output error

### Checking Exit Codes

```bash
python -m opal.configurable_court_extractor --court civil --date-period 7d
if [ $? -eq 0 ]; then
    echo "Extraction successful"
else
    echo "Extraction failed with code $?"
fi
```

## Help and Documentation

Get help for any command:

```bash
# Main OPAL help
python -m opal --help

# Configurable extractor help
python -m opal.configurable_court_extractor --help

# Get version information
python -m opal --version
```