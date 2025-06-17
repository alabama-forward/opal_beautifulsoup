---
title: Available Parsers
description: Overview of all parsers available in OPAL for scraping Alabama court data
---

# Available Parsers

OPAL includes several specialized parsers designed to extract court case data from different Alabama websites. Each parser is optimized for its specific data source.

## Parser Overview

| Parser | Source | Command | Description |
|--------|--------|---------|-------------|
| ParserAppealsAL | Alabama Appellate Courts | `appeals-al` | Extracts appellate court decisions |
| Parser1819 | 1819 News | `parser-1819` | Scrapes legal news from 1819 News |
| ParserDailyNews | Daily News sites | `daily-news` | Extracts court news from daily publications |

## Parser Details

### [Alabama Appeals Court Parser](./appeals-al.md)
<span class="parser-badge">appeals-al</span>

The primary parser for extracting appellate court decisions from Alabama's official court websites.

**Key Features:**
- Date range filtering
- Case type categorization
- Full opinion text extraction
- Metadata parsing (case numbers, parties, judges)

**Example:**
```bash
opal parse appeals-al --start-date 2024-01-01
```

### [1819 News Parser](./parser-1819.md)
<span class="parser-badge">parser-1819</span>

Specialized parser for the 1819 News website, focusing on legal and court-related news.

**Key Features:**
- Article categorization
- Author extraction
- Related case linking
- Comment parsing

**Example:**
```bash
opal parse parser-1819 --category legal
```

### [Daily News Parser](./daily-news.md)
<span class="parser-badge">daily-news</span>

General-purpose parser for various Alabama daily news websites covering court cases.

**Key Features:**
- Multiple site support
- Flexible content extraction
- Date-based filtering
- Keyword search capabilities

**Example:**
```bash
opal parse daily-news --site "montgomery-advertiser"
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

All parsers support these common options:

```bash
# Output format
--output-format [json|csv]

# Date filtering
--start-date YYYY-MM-DD
--end-date YYYY-MM-DD

# Verbose output
--verbose

# Custom output file
--output-file path/to/file
```

## Parser Development

Interested in creating custom parsers? See our [Developer Guide](../../developer/creating-custom-parsers.md) for detailed instructions on extending OPAL with new parsers.

## Next Steps

- Choose a parser and view its [detailed documentation](./appeals-al.md)
- Learn about [common use cases](../common-use-cases.md)
- Explore [output formats](../output-examples.md)