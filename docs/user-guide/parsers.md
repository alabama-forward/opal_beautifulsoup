---
layout: default
title: "Available Parsers"
---

# Available Parsers

OPAL includes several parsers for different Alabama news and government websites.

## News Parsers

### Parser1819

- **Website**: [1819 News](https://1819news.com/)
- **Content**: Conservative news outlet covering Alabama politics and culture
- **Usage**: 
  ```bash
  python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item
  ```

### ParserDailyNews

- **Website**: [Alabama Daily News](https://www.aldailynews.com/)
- **Content**: Daily news covering Alabama politics, business, and current events
- **Usage**:
  ```bash
  python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --suffix /news/item
  ```

## Government Parsers

### Court Parser (ParserAppealsAL)

- **Website**: [Alabama Appeals Court Public Portal](https://publicportal.alappeals.gov/)
- **Content**: Court cases, opinions, and legal documents
- **Features**:
  - Automated Chrome WebDriver handling
  - JavaScript-rendered content support
  - Case details extraction
- **Usage**:
  ```bash
  python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL
  ```

## Parser Capabilities

| Parser | Pagination | JavaScript Support | Authentication |
|--------|------------|-------------------|----------------|
| Parser1819 | ✓ | ✗ | ✗ |
| ParserDailyNews | ✓ | ✗ | ✗ |
| ParserAppealsAL | ✓ | ✓ | ✗ |

## Adding New Parsers

To add support for a new website, see the [Creating New Parsers](../developer/creating-parsers.md) guide.