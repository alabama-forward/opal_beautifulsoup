# OPAL - Oppositional Positions in Alabama

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Custom](https://img.shields.io/badge/license-custom-green.svg)](LICENSE)

OPAL is a powerful web scraping tool designed to extract and analyze content from Alabama news sites and court records. Built for progressive organizations and researchers in Alabama, OPAL transforms unstructured web content into structured JSON data for analysis, research, and advocacy work.

## 📚 Documentation

For comprehensive documentation, tutorials, and examples, visit our **[Documentation Website](https://alabama-forward.github.io/opal/)**.

### Quick Links
- [Complete Setup Guide](https://alabama-forward.github.io/opal/getting-started/complete-setup-guide/)
- [Quick Start Tutorial](https://alabama-forward.github.io/opal/getting-started/quickstart-tutorial/)
- [CLI Reference](https://alabama-forward.github.io/opal/user-guide/cli-reference/)
- [Output Examples](https://alabama-forward.github.io/opal/user-guide/output-examples/)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Chrome (for court scraping)
- Internet connection

### Installation

```bash
# 1. Check your system is ready
python check_prerequisites.py

# 2. Clone the repository
git clone https://github.com/alabama-forward/opal
cd opal

# 3. Install OPAL
pip install -e .
```

### Basic Usage

```bash
# Scrape news articles from 1819 News
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5

# Scrape court cases from Alabama Appeals Court
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL
```

## 🎯 Features

- **Multiple Content Sources**: Extract data from various Alabama news sites and court portals
- **Flexible Parsers**: Extensible architecture for adding new content sources
- **JavaScript Support**: Selenium integration for dynamic content extraction
- **Structured Output**: Clean JSON format for easy analysis and processing
- **Rate Limiting**: Respectful scraping with configurable delays
- **Error Handling**: Robust error management and recovery

## 📊 Supported Sources

### News Sites
- **1819 News** (`Parser1819`): Alabama's conservative news outlet
- **Alabama Daily News** (`ParserDailyNews`): State and local news coverage

### Court Records
- **Alabama Appeals Court** (`ParserAppealsAL`): Civil and criminal appeals cases
- **Configurable Court Extractor**: Advanced filtering for court searches

## 💡 Use Cases

OPAL is designed for:
- **Media Analysis**: Track coverage patterns and narrative trends
- **Legal Research**: Monitor court cases and judicial decisions
- **Advocacy Work**: Gather data for progressive campaigns
- **Academic Research**: Analyze political discourse and media framing
- **Fact-Checking**: Verify claims with structured data collection

## 🛠️ Advanced Features

### Configurable Court Searches

```bash
# Search civil cases from the last 7 days
python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed

# Search by case number
python -m opal.configurable_court_extractor --case-number "2024-CA-001"
```

### Custom Parsers

OPAL's extensible architecture makes it easy to add new content sources. See our [Creating Custom Parsers](https://alabama-forward.github.io/opal/developer/creating-custom-parsers/) guide.

## 📋 Output Format

OPAL produces structured JSON data:

### News Articles
```json
{
    "url": "https://example.com/article",
    "title": "Article Title",
    "author": "Author Name",
    "date": "2024-01-15",
    "line_count": 10,
    "line_content": {
        "line 1": "First paragraph...",
        "line 2": "Second paragraph..."
    }
}
```

### Court Cases
```json
{
    "court": "Court of Civil Appeals",
    "case_number": {
        "text": "2024-CA-001",
        "link": "https://..."
    },
    "case_title": "Smith v. Jones",
    "classification": "Civil",
    "filed_date": "01/10/2024",
    "status": "OPEN"
}
```

## 🤝 Contributing

To contribute to OPAL, please contact Gabriel at gabri@alforward.org. We welcome contributions that advance progressive causes in Alabama.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Build documentation locally
mkdocs serve
```

## 📜 License

This project uses a custom license focused on progressive use. Key points:
- ✅ Free for progressive organizations and research
- ✅ Open for educational purposes
- ❌ Not for commercial sale
- ❌ Not for use against progressive causes

See [LICENSE](LICENSE) for full details.

## 🙏 Acknowledgments

Created by **Gabriel Cabán Cubero**, Data Director at [Alabama Forward](https://alforward.org/).

Built by progressives in Alabama, for progressives in Alabama.

## 📞 Support

- **Documentation**: [OPAL Docs](https://alabama-forward.github.io/opal/)
- **Issues**: [GitHub Issues](https://github.com/alabama-forward/opal/issues)
- **Contact**: gabri@alforward.org

---

*Use it wisely. Use it for progressive purposes. Build a better Alabama.*