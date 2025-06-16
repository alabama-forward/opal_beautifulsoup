# Command Line Tools

OPAL provides several command-line tools for extracting court and news data. For the easiest way to build and understand these commands, use our **[Interactive Command Builder](command-builder.md)**.

## Available Tools

### 1. Main OPAL CLI
```bash
python -m opal --url <URL> --parser <PARSER> [options]
```
For news articles and basic court scraping.

### 2. Configurable Court Extractor
```bash
python -m opal.configurable_court_extractor --court <TYPE> [options]
```
For advanced court searches with filters and date ranges.

## Getting Started

Instead of memorizing command syntax, we recommend:

1. **🛠️ [Interactive Command Builder](command-builder.md)** - Visual interface with examples, validation, and one-click copying
2. **📋 [Common Use Cases](common-use-cases.md)** - Real-world examples and complete workflows
3. **🚀 [Quick Start Tutorial](../getting-started/quickstart-tutorial.md)** - Step-by-step guide for your first scrape

## Quick Examples

**News Scraping:**
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5
```

**Court Scraping:**
```bash
python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed
```

## Complete Reference

For all command options, parameters, and advanced usage:
- **Full parameter list**: Use `python -m opal --help` or `python -m opal.configurable_court_extractor --help`
- **Interactive builder**: [Command Builder](command-builder.md) with tooltips and validation
- **Output examples**: [Output Examples](output-examples.md) to see what data you'll get