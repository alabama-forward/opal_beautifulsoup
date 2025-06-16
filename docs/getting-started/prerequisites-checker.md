# Prerequisites Checker

Before installing OPAL, run our prerequisites checker to verify your system is ready. This tool will identify potential issues and provide specific solutions.

## Quick Check

Run this single command to check your system:

```bash
python check_prerequisites.py
```

The checker will automatically verify all requirements and give you a detailed report.

## What It Checks

### ✅ Python Environment
- **Python Version**: Ensures you have Python 3.8+ (required for OPAL)
- **Package Installer (pip)**: Verifies pip is available for installing packages
- **Virtual Environment**: Checks if you're using a virtual environment (recommended)

### ✅ Required Packages
- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML parsing library
- **selenium**: Web browser automation for court scraping
- **webdriver-manager**: Automatic ChromeDriver management

### ✅ Browser Requirements
- **Google Chrome**: Required for court scraping functionality
- **ChromeDriver Management**: Verifies automatic driver setup will work

### ✅ Network Connectivity
Tests connections to:
- 1819news.com
- Alabama Daily News
- Alabama Appeals Court portal
- Python Package Index (PyPI)

### ✅ System Resources
- **File Permissions**: Can write output files
- **Memory (RAM)**: Sufficient for scraping operations
- **Disk Space**: Available for storing scraped data

## Understanding the Results

### 🟢 Passed Checks
```
✅ Python Version: Python 3.9.7 (compatible)
✅ Package Installer (pip): pip 21.3.1 available
✅ Google Chrome: Found at /Applications/Google Chrome.app
```

These items are working correctly and ready for OPAL.

### 🟡 Warnings
```
⚠️  Virtual Environment: Not running in virtual environment
   💡 Fix: Create virtual environment: python -m venv venv && source venv/bin/activate

⚠️  requests: Not installed (HTTP library for web requests)
   💡 Fix: Install with: pip install requests
```

Warnings indicate items that should be addressed but won't prevent OPAL from working.

### 🔴 Failed Checks
```
❌ Python Version: Python 2.7.18 (incompatible)
   💡 Fix: Install Python 3.8 or higher from https://python.org

❌ Google Chrome: Google Chrome not found
   💡 Fix: Install Chrome from https://google.com/chrome for court scraping functionality
```

Failed checks must be fixed before OPAL will work properly.

## Sample Output

Here's what a typical check looks like:

```
============================================================
OPAL Prerequisites Checker
============================================================

📋 Python Environment
------------------
✅ Python Version: Python 3.9.7 (compatible)

✅ Package Installer (pip): pip 21.3.1 available

⚠️  Virtual Environment: Not running in virtual environment
   💡 Fix: Create virtual environment: python -m venv venv && source venv/bin/activate

📋 Required Packages
-----------------
⚠️  requests: Not installed (HTTP library for web requests)
   💡 Fix: Install with: pip install requests

⚠️  beautifulsoup4: Not installed (HTML parsing library)
   💡 Fix: Install with: pip install beautifulsoup4

⚠️  selenium: Not installed (Web browser automation)
   💡 Fix: Install with: pip install selenium

⚠️  webdriver-manager: Not installed (Automatic ChromeDriver management)
   💡 Fix: Install with: pip install webdriver-manager

📋 Browser Requirements
--------------------
✅ Google Chrome: Found at /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

✅ ChromeDriver Management: webdriver-manager will handle ChromeDriver automatically

📋 Network Connectivity
---------------------
✅ Connection to 1819news.com: Successfully connected (200)

✅ Connection to Alabama Daily News: Successfully connected (200)

✅ Connection to Alabama Appeals Court: Successfully connected (200)

✅ Connection to Python Package Index: Successfully connected (200)

📋 File System Permissions
------------------------
✅ Write Permissions: Can write files in current directory

✅ Home Directory Access: Can write to home directory

📋 System Resources
-----------------
✅ Memory (RAM): 16.0 GB available

✅ Disk Space: 45.2 GB free space available

📊 Summary
============================================================
Total checks: 14
✅ Passed: 8
⚠️  Warnings: 6
❌ Failed: 0

✅ Good to go with minor warnings!

Your system should work with OPAL, but consider addressing the warnings above.

Next steps:
1. Install OPAL: pip install -e .
2. Try the quick start tutorial

📚 For help with setup:
- Complete Setup Guide: docs/getting-started/complete-setup-guide.md
- Environment-specific guides: docs/getting-started/environment-guides.md
- Troubleshooting: docs/user-guide/understanding-errors.md

Happy scraping! 🚀
```

## Common Issues and Fixes

### Python Version Issues

**Problem**: "Python 2.7.18 (incompatible)"
**Solution**: Install Python 3.8+ from [python.org](https://python.org)

**Problem**: "Python 3.6.9 (minimum supported, but 3.8+ recommended)"
**Solution**: Consider upgrading to Python 3.8+ for best compatibility

### Package Installation Issues

**Problem**: "pip not found"
**Solution**: Install pip with `python -m ensurepip --upgrade`

**Problem**: Multiple package warnings
**Solution**: These will be automatically installed when you run `pip install -e .`

### Browser Issues

**Problem**: "Google Chrome not found"
**Solution**: Install Chrome from [google.com/chrome](https://google.com/chrome)

**Problem**: ChromeDriver issues
**Solution**: The webdriver-manager package handles this automatically

### Network Issues

**Problem**: Connection failures to websites
**Solution**: 
- Check your internet connection
- Try again later (websites may be temporarily down)
- Use a VPN if you're in a restricted network

### Permission Issues

**Problem**: "Cannot write to current directory"
**Solution**: 
- Run from a directory where you have write permissions
- On Linux/Mac: `chmod 755 .` to fix permissions
- On Windows: Run as administrator if needed

## When to Run the Checker

### Before First Installation
Run the checker before installing OPAL to catch issues early:

```bash
# Download OPAL
git clone https://github.com/your-repo/opal_beautifulsoup
cd opal_beautifulsoup

# Check prerequisites first
python check_prerequisites.py

# Then install if checks pass
pip install -e .
```

### After System Changes
Re-run the checker if you:
- Update Python
- Change virtual environments  
- Update your operating system
- Move OPAL to a different computer

### Troubleshooting Issues
If OPAL isn't working properly, run the checker to identify potential causes:

```bash
python check_prerequisites.py
```

## Advanced Usage

### Verbose Output
For more detailed information during checks:

```bash
python check_prerequisites.py --verbose
```

### Save Results to File
To save the check results for troubleshooting:

```bash
python check_prerequisites.py > system_check.txt 2>&1
```

### CI/CD Integration
Use in automated testing:

```bash
# Exit code 0 = all critical checks passed
# Exit code 1 = critical issues found
python check_prerequisites.py
if [ $? -eq 0 ]; then
    echo "System ready for OPAL"
    pip install -e .
else
    echo "Prerequisites not met"
    exit 1
fi
```

## Getting Help

If the prerequisites checker shows issues you can't resolve:

1. **Check the suggested fixes** - Each failed check includes specific solutions
2. **Review the setup guide** - [Complete Setup Guide](complete-setup-guide.md) has detailed instructions
3. **Check environment-specific guides** - [Environment Guides](environment-guides.md) for your OS
4. **Look for error solutions** - [Understanding Errors](../user-guide/understanding-errors.md) for common problems

The prerequisites checker is designed to catch 95% of setup issues before they cause problems. Running it first will save you time and frustration during installation!