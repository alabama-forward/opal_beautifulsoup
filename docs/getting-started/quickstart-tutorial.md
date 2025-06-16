---
layout: default
title: "Quick Start Tutorial"
---

# Quick Start Tutorial

Welcome! This hands-on tutorial will walk you through your first OPAL scraping tasks. By the end, you'll have successfully scraped both news articles and court cases.

## Before You Begin

Make sure you've completed the [Complete Setup Guide](complete-setup-guide.md). You should have:
- ✅ Python installed
- ✅ Virtual environment activated (you see `(venv)` in your terminal)
- ✅ OPAL installed
- ✅ Google Chrome installed (for court scraping)

## Tutorial 1: Your First News Scrape

Let's start by scraping a few articles from 1819 News.

### Step 1: Understand the Command

Here's what we'll run:
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 2
```

Let's break this down:
- `python -m opal` - Runs OPAL as a module
- `--url https://1819news.com/` - The website to scrape
- `--parser Parser1819` - Which parser to use (specific to this news site)
- `--suffix /news/item` - Only scrape URLs containing this pattern (helps identify articles)
- `--max_pages 2` - Limit to 2 pages (keeps it quick for testing)

### Step 2: Run the Command

1. Make sure your virtual environment is activated
2. Copy and paste the command above
3. Press Enter

### Step 3: What You'll See

```
Starting OPAL web scraper...
Using Parser1819 for https://1819news.com/
Collecting article URLs...
Found 15 article URLs
Processing articles...
[1/15] Scraping: https://1819news.com/news/item/...
[2/15] Scraping: https://1819news.com/news/item/...
...
Scraping complete!
Output saved to: 2024-01-15_Parser1819.json
Total articles scraped: 15
```

### Step 4: Check Your Output

1. Look in your project folder for a file like `2024-01-15_Parser1819.json`
2. Open it with a text editor
3. You'll see structured data for each article

**Tip**: If the file looks messy, try opening it in a web browser for better formatting!

### Common Issues and Solutions

**"No articles found"**
- The website might have changed its structure
- Try without the `--suffix` parameter
- Check if the website is accessible in your browser

**"Connection error"**
- Check your internet connection
- The website might be temporarily down
- Try again in a few minutes

## Tutorial 2: Scraping Court Cases

Now let's scrape some court case data. This uses Selenium, so it might take a bit longer.

### Step 1: Basic Court Scrape

Run this command:
```bash
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL --max_pages 2
```

Parameters explained:
- `--parser ParserAppealsAL` - Uses the Alabama Appeals Court parser
- `--max_pages 2` - Limits to 2 pages of results

### Step 2: What Happens During Court Scraping

You'll see:
```
Starting OPAL web scraper...
Initializing Chrome browser (headless mode)...
Loading court portal...
Waiting for page to render...
Found 30 cases per page
Processing page 1 of 2...
Processing page 2 of 2...
Saving results...
Output saved to: 2024-01-15_court_cases.json
CSV output saved to: 2024-01-15_143022_court_cases_all.csv
Total cases scraped: 60
```

**Note**: Court scraping is slower because:
- It launches a real Chrome browser (in hidden mode)
- It waits for JavaScript to load
- The court website has rate limiting

### Step 3: Check Both Output Files

You now have two files:
1. **JSON file**: Complete data with all details
2. **CSV file**: Same data in spreadsheet format

Open the CSV file in Excel to see a nice table of court cases!

## Tutorial 3: Advanced Court Search

Let's search for specific types of cases using the configurable extractor.

### Step 1: Search Recent Civil Appeals

```bash
python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed
```

This searches for:
- Civil court cases only
- Filed in the last 7 days
- Excluding closed cases

### Step 2: Understanding Date Periods

You can use these date period options:
- `7d` - Last 7 days
- `1m` - Last month
- `3m` - Last 3 months
- `6m` - Last 6 months
- `1y` - Last year

### Step 3: Custom Date Range

For specific dates:
```bash
python -m opal.configurable_court_extractor --court criminal --start-date 2024-01-01 --end-date 2024-01-15
```

## Understanding Success

You know your scrape was successful when:
1. ✅ No error messages appear
2. ✅ Output files are created
3. ✅ The files contain data (not empty)
4. ✅ File sizes are reasonable (>1KB)

## Practice Exercises

Try these on your own:

### Exercise 1: Scrape More Articles
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 5
```
- How many articles did you get?
- How long did it take?

### Exercise 2: Different News Source
```bash
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 3
```
- Compare the output structure
- Are the fields the same?

### Exercise 3: Search Specific Court Cases
```bash
python -m opal.configurable_court_extractor --court supreme --date-period 1m --max-pages 3
```
- How many Supreme Court cases did you find?
- What classifications do you see?

## What's Next?

Congratulations! You've successfully:
- ✅ Scraped news articles from two sources
- ✅ Extracted court case data
- ✅ Used advanced search parameters
- ✅ Generated both JSON and CSV output

### Next Steps:
1. Review the [Output Examples](../user-guide/output-examples.md) to better understand your data
2. Learn about [Common Use Cases](../user-guide/common-use-cases.md)
3. Set up [Automated Daily Scraping](../user-guide/automation.md)

### Pro Tips:
- Start with small `--max_pages` values while learning
- Always check the first few results before scraping everything
- Save important command variations in a text file for reuse
- Court scraping is slower - be patient!

## Need Help?

If something isn't working:
1. Make sure your virtual environment is activated
2. Check your internet connection
3. Verify the website is accessible in your browser
4. Review error messages carefully - they often explain the issue
5. Try with `--max_pages 1` first to isolate problems

Remember: Every expert was once a beginner. Keep experimenting, and you'll be a pro in no time!