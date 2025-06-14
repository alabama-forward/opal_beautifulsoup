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

- **[Getting Started](getting-started/installation.md)** - Installation and setup
- **[User Guide](user-guide/cli-usage.md)** - How to use OPAL
- **[Developer Guide](developer/architecture.md)** - Extend Opal with new parsers

## Built by Alabama Forward

This project was created by Gabriel Cabán Cubero, Data Director at Alabama Forward.
