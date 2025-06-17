---
title: User Guide
description: Comprehensive guide for using OPAL's features and capabilities
---

# User Guide

This guide covers everything you need to know about using OPAL effectively for scraping Alabama court data.

## In This Section

### [CLI Reference](./cli-reference.md)
Complete command-line interface documentation with all available commands and options.

### [Interactive Command Builder](./command-builder.md)
Build complex OPAL commands with our interactive tool.

### [Available Parsers](./parsers.md)
Overview of all available parsers and their capabilities.

### [Configurable Court Extractor](./configurable_court_extractor.md)
Learn about OPAL's flexible court data extraction system.

### [Visual Flow Diagrams](./visual-flow-diagrams.md)
Understand OPAL's architecture and data flow through visual diagrams.

### [Output Examples](./output-examples.md)
See real examples of OPAL's output formats and data structures.

### [Common Use Cases](./common-use-cases.md)
Practical examples and patterns for common scraping tasks.

### [Working with Output Data](./working-with-output-data.md)
Process and analyze the data extracted by OPAL.

### [Understanding Errors](./understanding-errors.md)
Troubleshoot common issues and error messages.

## Quick Reference

### Basic Commands

```bash
# Scrape Alabama Appeals Court
opal parse appeals-al

# Scrape with date range
opal parse appeals-al --start-date 2024-01-01 --end-date 2024-12-31

# Export to different formats
opal parse appeals-al --output-format json
opal parse appeals-al --output-format csv
```

### Parser-Specific Guides

- [Alabama Appeals Court Parser](./parser-appeals-al-cli.md)
- [1819 News Parser](./parsers/parser-1819.md)
- [Daily News Parser](./parsers/daily-news.md)

## Most Common Tasks

| Task | Command | Guide |
|------|---------|-------|
| Scrape recent cases | `opal parse appeals-al` | [Quick Start](../getting-started/quickstart-tutorial.md) |
| Filter by date | `opal parse appeals-al --start-date YYYY-MM-DD` | [CLI Reference](./cli-reference.md) |
| Export as JSON | `opal parse appeals-al --output-format json` | [Output Examples](./output-examples.md) |
| Debug issues | `opal parse appeals-al --verbose` | [Understanding Errors](./understanding-errors.md) |

## Next Steps

- Explore [specific parsers](./parsers.md) for different Alabama websites
- Learn about [advanced configuration](./configurable_court_extractor.md)
- See [common use cases](./common-use-cases.md) for inspiration