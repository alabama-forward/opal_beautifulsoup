# CLI Usage

OPAL provides a command-line interface for scraping Alabama news sites and court records. For the easiest way to build commands, use our **[Interactive Command Builder](command-builder.md)** which provides a visual interface with examples and real-time validation.

## Quick Reference

### Basic Command Structure
```bash
python -m opal --url <URL> --parser <PARSER> [OPTIONS]
```

### Essential Examples

**News Scraping:**
```bash
# 1819 News articles
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5

# Alabama Daily News
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 3
```

**Court Records:**
```bash
# Basic court scraping
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court

# Advanced court search
python -m opal.configurable_court_extractor --court civil --date-period 1m --exclude-closed
```

## Need More Help?

- **🛠️ [Interactive Command Builder](command-builder.md)** - Build commands visually with examples and validation
- **📋 [Common Use Cases](common-use-cases.md)** - Real-world scenarios and complete workflows
- **💾 [Output Examples](output-examples.md)** - See what data you'll get
- **🚀 [Quick Start Tutorial](../getting-started/quickstart-tutorial.md)** - Step-by-step first scrape