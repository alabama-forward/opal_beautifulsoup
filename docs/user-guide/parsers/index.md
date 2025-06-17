---
title: Available Parsers
description: Overview of all parsers available in OPAL for scraping Alabama court data
---

# Available Parsers

OPAL includes several specialized parsers designed to extract court case data from different Alabama websites. Each parser is optimized for its specific data source.

## Parser Overview

| Parser | Source | Command | Description |
|--------|--------|---------|-------------|
| ParserAppealsAL | Alabama Appellate Courts | `ParserAppealsAL` | Extracts appellate court decisions |
| Parser1819 | 1819 News | `Parser1819` | Scrapes legal news from 1819 News |
| ParserDailyNews | Daily News sites | `ParserDailyNews` | Extracts court news from daily publications |

## Parser Details

### [Alabama Appeals Court Parser](./ParserAppealsAL.md)
<span class="parser-badge">ParserAppealsAL</span>

The primary parser for extracting appellate court decisions from Alabama's official court websites.

**Key Features:**
- JavaScript rendering with Selenium
- Court case metadata extraction
- Pagination handling
- Rate limiting protection

**Example:**
```bash
python -m opal --url "https://publicportal.alacourt.gov" --parser ParserAppealsAL
```

### [1819 News Parser](./Parser1819.md)
<span class="parser-badge">Parser1819</span>

Specialized parser for the 1819 News website, focusing on legal and court-related news.

**Key Features:**
- Article text extraction
- Author and date parsing
- Line-by-line content storage
- URL pattern filtering

**Example:**
```bash
python -m opal --url "https://1819news.com/" --parser Parser1819
```

### [Daily News Parser](./ParserDailyNews.md)
<span class="parser-badge">ParserDailyNews</span>

Parser for Alabama Daily News and similar news websites with compatible HTML structures.

**Key Features:**
- Specific HTML class targeting
- Author and date extraction
- Paragraph-based content parsing
- Error resilience with defaults

**Example:**
```bash
python -m opal --url "https://alabamadailynews.com/" --parser ParserDailyNews
```

## Choosing the Right Parser

### By Data Source

- **Official Court Documents**: Use `appeals-al` for authoritative appellate decisions
- **News Coverage**: Use `parser-1819` or `daily-news` for journalistic coverage
- **Historical Data**: Check parser-specific date ranges in individual guides

### By Use Case

- **Legal Research**: `appeals-al` provides full opinion texts
- **Media Monitoring**: `parser-1819` and `daily-news` track news coverage
- **Comprehensive Analysis**: Combine multiple parsers for complete coverage

## Common Options

All parsers support these common command-line options:

```bash
# Required options
--url          # Base URL of the website to scrape
--parser       # Parser name (ParserAppealsAL, Parser1819, ParserDailyNews)

# Optional options
--suffix       # URL suffix to filter pages
--max_pages    # Maximum number of pages to process

# Example with all options
python -m opal --url "https://example.com" --parser Parser1819 --suffix "/news/" --max_pages 5
```

Output files are automatically named with the format: `YYYY-MM-DD_ParserName.json`

## Parser Development

Interested in creating custom parsers? See our [Developer Guide](../../developer/creating-custom-parsers.md) for detailed instructions on extending OPAL with new parsers.

## Next Steps

- Choose a parser and view its [detailed documentation](./appeals-al.md)
- Learn about [common use cases](../common-use-cases.md)
- Explore [output formats](../output-examples.md)