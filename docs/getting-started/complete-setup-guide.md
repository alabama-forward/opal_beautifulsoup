# Complete Setup Guide

This guide will walk you through setting up OPAL from scratch, even if you're new to Python development. We'll cover everything you need to get started.

## Prerequisites Overview

Before installing OPAL, you'll need:
- Python 3.8 or higher
- A terminal/command prompt
- Internet connection
- About 15 minutes

## Step 1: Install Python

### Windows

1. **Download Python**:
   - Go to [python.org/downloads](https://python.org/downloads)
   - Click "Download Python" (get version 3.8 or higher)
   - Run the installer

2. **Important Installation Settings**:
   - ✅ Check "Add Python to PATH" at the bottom of the installer
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (search for "cmd" in Start menu)
   - Type: `python --version`
   - You should see: `Python 3.x.x`

### macOS

1. **Check if Python is Installed**:
   - Open Terminal (found in Applications > Utilities)
   - Type: `python3 --version`
   - If you see a version number, skip to Step 2

2. **Install Python** (if needed):
   - Install Homebrew first (if not installed):
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python:
     ```bash
     brew install python3
     ```

3. **Verify Installation**:
   ```bash
   python3 --version
   ```

### Linux (Ubuntu/Debian)

1. **Update Package List**:
   ```bash
   sudo apt update
   ```

2. **Install Python and pip**:
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Verify Installation**:
   ```bash
   python3 --version
   ```

## Step 2: Set Up Your Project Directory

1. **Create a folder for OPAL**:
   
   Windows (Command Prompt):
   ```cmd
   mkdir C:\opal-project
   cd C:\opal-project
   ```
   
   macOS/Linux (Terminal):
   ```bash
   mkdir ~/opal-project
   cd ~/opal-project
   ```

2. **Download OPAL**:
   - Option A: Download ZIP from GitHub
     - Go to the OPAL repository
     - Click "Code" → "Download ZIP"
     - Extract to your opal-project folder
   
   - Option B: Use git (if installed):
     ```bash
     git clone [repository-url] .
     ```

## Step 3: Create a Virtual Environment

A virtual environment keeps OPAL's dependencies separate from other Python projects.

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` appear in your command prompt when activated.

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal when activated.

### Troubleshooting Virtual Environment

If you get an error about execution policies on Windows:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

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