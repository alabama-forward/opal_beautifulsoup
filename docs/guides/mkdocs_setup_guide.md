# Setting Up MkDocs for OPAL

This guide will help you set up MkDocs to create a beautiful documentation website for your OPAL project.

## 1. Install MkDocs and Theme

```bash
# Install MkDocs and the popular Material theme
pip install mkdocs mkdocs-material mkdocs-material-extensions

# Or add to your requirements.txt:
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocs-material-extensions>=1.3.0
```

## 2. Create MkDocs Configuration

Create a `mkdocs.yml` file in your project root:

```yaml
site_name: OPAL - Oppositional Positions in Alabama
site_description: Web scraper for Alabama news sites and court records
site_author: Gabriel Cabán Cubero
site_url: https://yourusername.github.io/opal

repo_name: opal
repo_url: https://github.com/yourusername/opal
edit_uri: edit/main/docs/

theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: blue
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: blue
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

plugins:
  - search
  - autorefs

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - admonition
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
      - Configuration: getting-started/configuration.md
  - User Guide:
      - CLI Usage: user-guide/cli-usage.md
      - Available Parsers: user-guide/parsers.md
      - Output Formats: user-guide/output-formats.md
  - Developer Guide:
      - Architecture: developer/architecture.md
      - BaseParser Guide: developer/BaseParser_web_scraping_guide.md
      - Creating New Parsers: developer/creating-parsers.md
      - ParserAppealsAL Documentation: developer/ParserAppealsAL_documentation.md
  - API Reference:
      - BaseParser: api/base-parser.md
      - Parser1819: api/parser-1819.md
      - ParserDailyNews: api/parser-daily-news.md
      - ParserAppealsAL: api/parser-appeals-al.md
  - About:
      - Contributing: about/contributing.md
      - License: about/license.md
```

## 3. Create Documentation Structure

```bash
# Create the docs directory structure
mkdir -p docs/getting-started
mkdir -p docs/user-guide
mkdir -p docs/developer
mkdir -p docs/api
mkdir -p docs/about

# Move existing documentation (don't delete originals yet)
cp docs/BaseParser_web_scraping_guide.md docs/developer/
cp docs/ParserAppealsAL_documentation.md docs/developer/
```

## 4. Create the Homepage

Create `docs/index.md`:

```markdown
# OPAL - Oppositional Positions in Alabama

Welcome to OPAL's documentation! OPAL is a web scraping tool that extracts content from Alabama news sites and court records.

## Features

- 📰 **Multiple News Sources** - Parse articles from 1819news.com and Alabama Daily News
- ⚖️ **Court Records** - Extract data from Alabama Appeals Court Public Portal
- 🔧 **Extensible Architecture** - Easy to add new parsers
- 📊 **Structured Output** - Clean JSON format for analysis
- 🚀 **CLI Tool** - Simple command-line interface

## Quick Start

```bash
# Install OPAL
pip install -e .

# Scrape news articles
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5

# Scrape court cases
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court
```

## Documentation Overview

- **[Getting Started](getting-started/installation.md)** - Installation and setup
- **[User Guide](user-guide/cli-usage.md)** - How to use OPAL
- **[Developer Guide](developer/architecture.md)** - Extend OPAL with new parsers
- **[API Reference](api/base-parser.md)** - Detailed API documentation

## Built by Alabama Forward

This project was created by Gabriel Cabán Cubero, Data Director at Alabama Forward.
```

## 5. Create Basic Documentation Files

Create `docs/getting-started/installation.md`:

```markdown
# Installation

## Requirements

- Python 3.6 or higher
- Chrome browser (for court parser)

## Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/opal.git
cd opal

# Install dependencies
pip install -r requirements.txt

# Install OPAL
pip install -e .
```

## Verify Installation

```bash
# Check OPAL is installed
python -m opal --help
```
```

## 6. Build and Serve Documentation

```bash
# Serve locally for development (hot reload)
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 7. GitHub Pages Setup

1. Go to your repository settings on GitHub
2. Navigate to "Pages"
3. Set source to "Deploy from a branch"
4. Select `gh-pages` branch and `/ (root)` folder
5. Your site will be available at `https://yourusername.github.io/opal`

## 8. Add to .gitignore

```bash
echo "site/" >> .gitignore  # MkDocs build output
```

## 9. Useful Commands

```bash
# Local development server (http://127.0.0.1:8000)
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy

# Get help
mkdocs --help
```

## 10. Advanced Features

You can add:
- **Code syntax highlighting** with language-specific formatting
- **Mermaid diagrams** for architecture visualization
- **API documentation** auto-generated from docstrings
- **Search functionality** (included by default)
- **PDF export** with additional plugins
- **Multiple languages** support

## Next Steps

1. **Install MkDocs**: Run `pip install mkdocs mkdocs-material`
2. **Create mkdocs.yml**: Copy the configuration from step 2
3. **Organize docs**: Move your existing markdown files to the appropriate folders
4. **Run locally**: Use `mkdocs serve` to preview your documentation
5. **Deploy**: Use `mkdocs gh-deploy` to publish to GitHub Pages

## Tips

- Keep documentation close to code - update docs when you change features
- Use meaningful file names that match your navigation structure
- Include code examples and real-world usage scenarios
- Add screenshots for complex features
- Keep a changelog to track documentation updates

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [MkDocs Plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins)