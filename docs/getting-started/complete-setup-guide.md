---
layout: default
title: "Complete Setup Guide"
---

# Complete Setup Guide

This guide will walk you through setting up OPAL from scratch, even if you're new to Python development. We'll cover everything you need to get started.

## Quick Install (For Experienced Users)

If you're already familiar with Python development:

```bash
# Clone and install
git clone https://github.com/alabama-forward/opal
cd opal
pip install -e .
```

**Requirements**: Python 3.8+, Google Chrome (for court scraping), Internet connection

## Before You Start

🔍 **Check Your System First**: Run our [Prerequisites Checker](prerequisites-checker.md) to verify your system is ready and identify any issues early.

```bash
python check_prerequisites.py
```

## Prerequisites Overview

Before installing OPAL, you'll need:
- Python 3.8 or higher
- A terminal/command prompt
- Internet connection
- About 15 minutes

## Step 1: Install Python

**For detailed platform-specific installation instructions, see [Environment-Specific Guides](environment-guides.md).**

### Quick Installation Summary

**Windows**: Download from python.org (✅ check "Add Python to PATH")  
**macOS**: Use Homebrew (`brew install python3`) or download from python.org  
**Linux**: Use package manager (`sudo apt install python3 python3-pip python3-venv`)

### Verify Installation
```bash
# Check Python version (should be 3.8+)
python --version      # Windows
python3 --version     # macOS/Linux

# Check pip is available
pip --version         # Windows  
pip3 --version        # macOS/Linux
```

## Step 2: Set Up Your Project Directory

1. **Create a folder for OPAL**:
   ```bash
   # Create project directory
   mkdir opal-project
   cd opal-project
   ```

2. **Download OPAL**:
   ```bash
   # Clone repository (recommended)
   git clone https://github.com/alabama-forward/opal .
   
   # OR download ZIP from GitHub and extract here
   ```

**Platform-specific commands**: See [Environment-Specific Guides](environment-guides.md) for detailed OS-specific instructions.

## Step 3: Create a Virtual Environment

A virtual environment keeps OPAL's dependencies separate from other Python projects.

```bash
# Create virtual environment
python -m venv venv          # Windows
python3 -m venv venv         # macOS/Linux

# Activate virtual environment  
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

You'll see `(venv)` appear in your prompt when activated.

**Troubleshooting**: See [Environment-Specific Guides](environment-guides.md) for platform-specific activation issues.

## Step 4: Install OPAL and Dependencies

With your virtual environment activated:

1. **Install OPAL**:
   ```bash
   pip install -e .
   ```
   
   Or if that doesn't work:
   ```bash
   pip install -r requirements.txt
   ```

2. **Wait for Installation**:
   - This will download and install all necessary packages
   - It may take 2-5 minutes depending on your internet speed

## Step 5: Set Up Chrome Driver (for Court Scraping)

OPAL uses Selenium for scraping JavaScript-heavy sites like the Alabama Appeals Court.

1. **Good News**: OPAL automatically manages ChromeDriver!
   - The `webdriver-manager` package handles this for you
   - It will download the correct version when first needed

2. **Requirements**:
   - You need Google Chrome installed on your computer
   - Download from: [google.com/chrome](https://google.com/chrome)

## Step 6: Verify Your Installation

Let's make sure everything is working:

1. **Test OPAL is installed**:
   ```bash
   python -m opal --help
   ```
   
   You should see the help menu with available options.

2. **Test with a simple scrape**:
   ```bash
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 1
   ```
   
   This will scrape just one page to verify everything works.

## Step 7: Understanding the Output

After running OPAL, you'll find:
- A JSON file in your project directory
- Named with timestamp: `YYYY-MM-DD_ParserName.json`
- Contains structured data from the scraped content

## Common Installation Issues

### Issue: "python is not recognized" (Windows)
**Solution**: Python wasn't added to PATH during installation
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to your system PATH

### Issue: "pip is not recognized"
**Solution**: 
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

### Issue: "No module named 'opal'"
**Solution**: Make sure you're in the correct directory and virtual environment is activated

### Issue: Chrome driver errors
**Solution**: 
1. Ensure Google Chrome is installed
2. Try updating Chrome to the latest version
3. The webdriver-manager should handle version matching automatically

## Next Steps

Now that OPAL is installed:
1. Read the [Quick Start Tutorial](quickstart-tutorial.md) for your first real scraping task
2. Check out [Output Examples](../output-examples.md) to understand the data format
3. Explore [Common Use Cases](../user-guide/common-use-cases.md)

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review the [Troubleshooting Guide](../troubleshooting.md)
3. Ensure your virtual environment is activated (you see `(venv)`)
4. Try reinstalling in a fresh virtual environment

Remember: Every developer started as a beginner. Take it step by step, and you'll be scraping Alabama news and court data in no time!