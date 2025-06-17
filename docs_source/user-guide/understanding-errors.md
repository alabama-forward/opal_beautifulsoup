---
layout: default
title: "Understanding Errors"
---

# Understanding Errors

This guide helps you understand common error messages when using OPAL and provides solutions to fix them. Don't worry - most errors have simple solutions!

**For developers**: See [Error Handling](../developer/error_handling.md) for technical implementation details and error handling strategies.

## Common Installation and Setup Errors

### Error: "python is not recognized" (Windows)

**What it means**: Windows can't find Python because it's not in your system PATH.

**Example**:
```
'python' is not recognized as an internal or external command,
operable program or batch file.
```

**Solutions**:
1. **Reinstall Python with PATH**:
   - Download Python again from python.org
   - ✅ Check "Add Python to PATH" during installation
   - Complete the installation

2. **Add Python to PATH manually**:
   - Find your Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\`)
   - Add it to your system PATH in Environment Variables

3. **Use Python Launcher** (Windows):
   ```cmd
   py -m opal --help
   ```

### Error: "No module named 'opal'"

**What it means**: OPAL isn't installed in your current Python environment.

**Example**:
```
ModuleNotFoundError: No module named 'opal'
```

**Solutions**:
1. **Make sure virtual environment is activated**:
   ```bash
   # You should see (venv) in your prompt
   # If not, activate it:
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Install OPAL**:
   ```bash
   pip install -e .
   ```

3. **Check you're in the right directory**:
   ```bash
   # Make sure you're in the opal folder
   ls -la  # Should see setup.py or pyproject.toml
   ```

### Error: "pip: command not found"

**What it means**: pip (Python package installer) isn't available.

**Solutions**:
1. **Install pip**:
   ```bash
   python -m ensurepip --upgrade
   ```

2. **Use alternative installation**:
   ```bash
   python -m pip install -e .
   ```

3. **Check Python installation**:
   ```bash
   python --version
   python -m pip --version
   ```

## Network and Connection Errors

### Error: "Connection timeout" or "Failed to establish connection"

**What it means**: OPAL can't reach the website you're trying to scrape.

**Example**:
```
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='1819news.com', port=443): 
Read timed out. (read timeout=30)
```

**Solutions**:
1. **Check your internet connection**:
   - Open the website in your browser
   - Try a different website to confirm internet works

2. **Wait and retry**:
   ```bash
   # Wait 5 minutes and try again
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2
   ```

3. **Try a different time**:
   - Websites may be slower during peak hours
   - Try early morning or late evening

4. **Reduce concurrent requests**:
   - OPAL includes built-in rate limiting
   - The delay between requests helps prevent timeouts

### Error: "SSL Certificate verification failed"

**What it means**: Your system can't verify the website's security certificate.

**Example**:
```
requests.exceptions.SSLError: HTTPSConnectionPool(host='example.com', port=443): 
Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError))
```

**Solutions**:
1. **Update your system**:
   - Update Python: `pip install --upgrade pip`
   - Update certificates on Mac: Run "Install Certificates.command" in Python folder

2. **Check system date/time**:
   - Incorrect system time can cause SSL errors
   - Sync your system clock

### Error: "Too Many Requests" or "Rate Limited"

**What it means**: The website is blocking you for making too many requests too quickly.

**Example**:
```
HTTP Error 429: Too Many Requests
```

**Solutions**:
1. **Wait before retrying**:
   ```bash
   # Wait 10-15 minutes, then try again
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 3
   ```

2. **Reduce the scope**:
   ```bash
   # Use fewer pages
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2
   ```

3. **Spread out your scraping**:
   - Don't run multiple scrapers simultaneously
   - Wait between different scraping sessions

## Browser and Selenium Errors (Court Scraping)

### Error: "Chrome driver not found" or "WebDriver errors"

**What it means**: OPAL can't find or start the Chrome browser for court scraping.

**Example**:
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solutions**:
1. **Install Google Chrome**:
   - Download from google.com/chrome
   - Make sure it's the latest version

2. **Let webdriver-manager handle it**:
   ```bash
   # OPAL should automatically download the right ChromeDriver
   # If it doesn't work, try updating:
   pip install --upgrade webdriver-manager
   ```

3. **Check Chrome version compatibility**:
   ```bash
   # Check your Chrome version
   google-chrome --version  # Linux
   # Or check in Chrome browser: Menu > Help > About Google Chrome
   ```

### Error: "Element not found" or "No such element"

**What it means**: The court website's structure changed, and OPAL can't find expected elements.

**Example**:
```
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
```

**Solutions**:
1. **Check if the court website is working**:
   - Visit https://publicportal.alappeals.gov/ in your browser
   - Make sure the search results page loads correctly

2. **Try a different URL**:
   ```bash
   # Use the basic court URL
   python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL --max_pages 2
   ```

3. **Website may have changed**:
   - The court website occasionally updates its structure
   - This may require updates to OPAL's parser
   - Report the issue if the website works fine in your browser

### Error: "Chrome crashed" or "Browser process ended"

**What it means**: The Chrome browser used for court scraping stopped working.

**Solutions**:
1. **Restart and try again**:
   ```bash
   # Simply run the command again
   python -m opal --url https://publicportal.alacourt.gov --parser ParserAppealsAL
   ```

2. **Check available memory**:
   - Close other applications to free up RAM
   - Court scraping uses more memory than news scraping

3. **Reduce page count**:
   ```bash
   # Process fewer pages at once
   python -m opal --url https://publicportal.alacourt.gov --parser ParserAppealsAL --max_pages 3
   ```

## Data and Parsing Errors

### Error: "No articles found" or "Empty results"

**What it means**: OPAL ran successfully but didn't find any content to scrape.

**Example Output**:
```json
{
  "articles": [],
  "metadata": {
    "total_articles": 0,
    "note": "No articles found matching the criteria"
  }
}
```

**Solutions**:
1. **Check the website manually**:
   - Visit the URL in your browser
   - Confirm there are actually articles/cases to scrape

2. **Adjust the suffix parameter**:
   ```bash
   # Try without suffix
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 3
   
   # Or try a different suffix
   python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /article --max_pages 3
   ```

3. **Website structure changed**:
   - News websites sometimes change their URL patterns
   - The parser may need updates for new website structures

### Error: "Permission denied" when saving files

**What it means**: OPAL can't save the output file to your chosen location.

**Example**:
```
PermissionError: [Errno 13] Permission denied: 'output.json'
```

**Solutions**:
1. **Check file permissions**:
   ```bash
   # Make sure you have write permissions in the current directory
   ls -la
   ```

2. **Choose a different output location**:
   ```bash
   # Save to your home directory
   python -m opal --url https://1819news.com/ --parser Parser1819 --output ~/my_output.json
   ```

3. **Close the file if it's open**:
   - Make sure the output file isn't open in Excel or another program

## Virtual Environment Errors

### Error: "Virtual environment not activated"

**What it means**: You're not using your virtual environment, so packages aren't available.

**Signs**:
- You don't see `(venv)` in your command prompt
- Getting "module not found" errors
- Commands that worked before now fail

**Solutions**:
1. **Activate virtual environment**:
   ```bash
   # Mac/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   
   # You should see (venv) appear in your prompt
   ```

2. **Recreate virtual environment if needed**:
   ```bash
   # If activation fails, recreate it
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## JSON and Output Errors

### Error: "Invalid JSON" when opening output files

**What it means**: The output file is corrupted or incomplete.

**Solutions**:
1. **Check if scraping completed successfully**:
   - Look for "Scraping complete!" message
   - Check file size (should be > 1KB if successful)

2. **Re-run the scraping**:
   ```bash
   # Try a smaller scope first
   python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2
   ```

3. **Validate JSON**:
   ```python
   import json
   
   try:
       with open('your_output.json', 'r') as f:
           data = json.load(f)
       print("JSON is valid!")
   except json.JSONDecodeError as e:
       print(f"JSON error: {e}")
   ```

## How to Report Issues

If you encounter an error that isn't covered here:

### 1. Gather Information
- Full error message
- Command you ran
- Your operating system
- Python version (`python --version`)
- Website you were trying to scrape

### 2. Try Basic Troubleshooting
- Update OPAL: `pip install --upgrade -e .`
- Try with `--max_pages 1` to isolate the issue
- Test your internet connection
- Check if the target website is accessible

### 3. Create a Bug Report
Include this information:
```
**Command that failed:**
python -m opal --url https://example.com --parser Parser1819

**Error message:**
[Paste the full error here]

**Environment:**
- OS: Windows 10 / macOS / Linux
- Python version: 3.9.7
- OPAL version: [run `pip show opal` if installed]

**Additional context:**
- Website accessible in browser: Yes/No
- First time using OPAL: Yes/No
- Worked before: Yes/No
```

## Error Prevention Tips

### 1. Start Small
```bash
# Always test with small runs first
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2
```

### 2. Check Your Setup
```bash
# Verify your environment before big runs
python --version
python -m opal --help
```

### 3. Monitor Progress
- Watch the console output for warnings
- Check file sizes to ensure data is being collected
- Test with different websites to isolate issues

### 4. Keep Backups
```bash
# Save successful outputs with dates
cp output.json "backup_$(date +%Y%m%d).json"
```

Remember: Every developer encounters errors. The key is systematic troubleshooting and learning from each issue. Most OPAL errors have straightforward solutions once you understand what they mean!