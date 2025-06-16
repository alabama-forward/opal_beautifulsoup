# Quick Start

For a comprehensive hands-on tutorial with real examples, please see the [Quick Start Tutorial](quickstart-tutorial.md).

## Basic Commands

**News Scraping:**
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5
```

**Court Scraping:**
```bash
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court
```

## Learn More
- [Quick Start Tutorial](quickstart-tutorial.md) - Detailed walkthrough with examples
- [Output Examples](../user-guide/output-examples.md) - See what data you'll get
- [CLI Usage Guide](../user-guide/cli-usage.md) - All command options
- [Available Parsers](../user-guide/parsers.md) - Supported websites