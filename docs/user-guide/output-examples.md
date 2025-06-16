---
layout: default
title: "Output Examples"
---

# Output Examples

This page shows you exactly what data OPAL produces when scraping different sources. Understanding the output format helps you plan how to use the data.

## Output File Naming

OPAL automatically names output files with timestamps:
- Format: `YYYY-MM-DD_ParserName.json`
- Example: `2024-01-15_Parser1819.json`
- CSV files (court data): `YYYY-MM-DD_HH-MM-SS_court_cases_[court_type].csv`

## News Article Output

### 1819 News Example

When you run:
```bash
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 2
```

You get a JSON file like this:

```json
{
  "articles": [
    {
      "title": "Alabama lawmakers consider education reform bill",
      "author": "Jane Smith",
      "date": "January 15, 2024",
      "line_count": 45,
      "content": "Full article text appears here...\n\nThe article continues with multiple paragraphs...\n\nAll the content from the webpage is captured."
    },
    {
      "title": "Local community rallies to support food bank",
      "author": "John Doe", 
      "date": "January 14, 2024",
      "line_count": 32,
      "content": "The complete article text...\n\nEvery paragraph is preserved..."
    }
  ],
  "metadata": {
    "source": "https://1819news.com/",
    "parser": "Parser1819",
    "total_articles": 2,
    "scrape_date": "2024-01-15T10:30:45"
  }
}
```

### Alabama Daily News Example

When you run:
```bash
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --suffix /articles --max_pages 1
```

Output structure is identical, but content comes from Alabama Daily News:

```json
{
  "articles": [
    {
      "title": "Birmingham announces new business development initiative",
      "author": "Sarah Johnson",
      "date": "January 15, 2024", 
      "line_count": 38,
      "content": "Birmingham city officials announced today...\n\nThe full article text appears here..."
    }
  ],
  "metadata": {
    "source": "https://www.aldailynews.com/",
    "parser": "ParserDailyNews",
    "total_articles": 1,
    "scrape_date": "2024-01-15T11:15:22"
  }
}
```

### Understanding News Output Fields

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Article headline | "Alabama lawmakers consider..." |
| `author` | Article author | "Jane Smith" |
| `date` | Publication date | "January 15, 2024" |
| `line_count` | Number of lines in content | 45 |
| `content` | Full article text with line breaks | "Full article text..." |

## Court Case Output

### JSON Format

When you run:
```bash
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL
```

You get both JSON and CSV files. Here's the JSON structure:

```json
{
  "status": "success",
  "court": "civil",
  "extraction_time": "2024-01-15 14:30:22",
  "total_cases": 150,
  "pages_processed": 5,
  "cases": [
    {
      "court": "Court of Civil Appeals",
      "case_number": {
        "text": "CL-2024-0001",
        "link": "https://publicportal.alappeals.gov/portal/home/case/caseid/CL-2024-0001"
      },
      "case_title": "Smith v. Jones Construction Company, LLC",
      "classification": "Appeal",
      "filed_date": "01/10/2024",
      "status": "Pending"
    },
    {
      "court": "Court of Civil Appeals",
      "case_number": {
        "text": "CL-2024-0002", 
        "link": "https://publicportal.alappeals.gov/portal/home/case/caseid/CL-2024-0002"
      },
      "case_title": "Johnson Family Trust v. State of Alabama Department of Revenue",
      "classification": "Petition",
      "filed_date": "01/11/2024",
      "status": "Active"
    }
  ],
  "search_parameters": {
    "court_type": "civil",
    "date_range": "last_30_days",
    "exclude_closed": true
  }
}
```

### CSV Format

The same data in CSV format (easier for Excel):

```csv
Court,Case Number,Case Title,Classification,Filed Date,Status,Case Link
Court of Civil Appeals,CL-2024-0001,"Smith v. Jones Construction Company, LLC",Appeal,01/10/2024,Pending,https://publicportal.alappeals.gov/portal/home/case/caseid/CL-2024-0001
Court of Civil Appeals,CL-2024-0002,"Johnson Family Trust v. State of Alabama Department of Revenue",Petition,01/11/2024,Active,https://publicportal.alappeals.gov/portal/home/case/caseid/CL-2024-0002
```

### Understanding Court Output Fields

| Field | Description | Example |
|-------|-------------|---------|
| `court` | Which court | "Court of Civil Appeals" |
| `case_number` | Case identifier with link | {"text": "CL-2024-0001", "link": "..."} |
| `case_title` | Full case name | "Smith v. Jones Construction..." |
| `classification` | Type of case | "Appeal", "Petition", "Writ" |
| `filed_date` | Date case was filed | "01/10/2024" |
| `status` | Current case status | "Active", "Pending", "Closed" |

## Working with Output Files

### Opening JSON Files

**In a Text Editor:**
- Right-click the file → Open with → Notepad (Windows) or TextEdit (Mac)
- For better formatting, use Notepad++ or VS Code

**In a Web Browser:**
- Drag the JSON file into Chrome or Firefox
- Many browsers will format it nicely

**In Python:**
```python
import json

# Read the file
with open('2024-01-15_Parser1819.json', 'r') as file:
    data = json.load(file)

# Access the data
for article in data['articles']:
    print(f"Title: {article['title']}")
    print(f"Author: {article['author']}")
    print(f"Date: {article['date']}")
    print("---")
```

### Opening CSV Files

**In Excel:**
1. Double-click the CSV file
2. Excel will open it automatically
3. Columns will be properly separated

**In Google Sheets:**
1. Go to sheets.google.com
2. File → Import → Upload
3. Select your CSV file

### Common Output Scenarios

**Scenario 1: No Articles Found**
```json
{
  "articles": [],
  "metadata": {
    "source": "https://example.com/",
    "parser": "Parser1819",
    "total_articles": 0,
    "scrape_date": "2024-01-15T10:30:45",
    "note": "No articles found matching the criteria"
  }
}
```

**Scenario 2: Partial Data (Missing Author)**
```json
{
  "articles": [
    {
      "title": "Breaking News Article",
      "author": "Unknown",
      "date": "January 15, 2024",
      "line_count": 25,
      "content": "Article content here..."
    }
  ]
}
```

**Scenario 3: Error During Scraping**
```json
{
  "status": "partial_success",
  "message": "Completed 3 of 5 pages before encountering error",
  "cases": [...],
  "error_details": "Connection timeout on page 4"
}
```

## File Size Expectations

- **News Articles**: 
  - ~1-3 KB per article
  - 100 articles ≈ 200-300 KB
  
- **Court Cases**:
  - ~500 bytes per case
  - 1000 cases ≈ 500 KB

## Next Steps

Now that you understand the output format:
1. Try the [Quick Start Tutorial](quickstart-tutorial.md) to generate your own output
2. Learn about [Working with Output Data](working-with-output.md)
3. Explore [Common Use Cases](common-use-cases.md) for practical applications