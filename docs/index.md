# OPAL - Oppositional Positions in ALabama

Welcome to OPAL's documentation! OPAL is a web scraping tool that extracts content from websites like Alabama news sites and court records.

## Features

- 📰 **Multiple News Sources** - Parse articles from 1819news.com and Alabama Daily News
- ⚖️ **Court Records** - Extract data from Alabama Appeals Court Public Portal
- 🔧 **Extensible Architecture** - Easy to add new parsers
- 📊 **Structured Output** - Clean JSON format for analysis
- 🚀 **CLI Tool** - Simple command-line interface

## Quick Start

#Install OPAL
pip install -e .

#Scrape news articles
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5

# Scrape court cases
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court

## Documentation Overview

- **[Complete Setup Guide](getting-started/complete-setup-guide.md)** - Step-by-step installation for beginners
- **[Quick Start Tutorial](getting-started/quickstart-tutorial.md)** - Hands-on tutorial with real examples
- **[Output Examples](user-guide/output-examples.md)** - See exactly what OPAL produces
- **[User Guide](user-guide/cli-usage.md)** - Detailed usage instructions
- **[Developer Guide](developer/architecture.md)** - Extend OPAL with new parsers

## Built by Alabama Forward

This project was created by Gabriel Cabán Cubero, Data Director at Alabama Forward.
