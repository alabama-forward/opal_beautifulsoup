# Common Use Cases

This guide shows you how to use OPAL for specific real-world scenarios. Each use case includes the exact commands, expected outputs, and practical tips.

## News Monitoring Use Cases

### Use Case 1: Track Weekly Political News

**Scenario**: You want to monitor Alabama political news from both major news sources for the past week.

**Commands**:
```bash
# Scrape 1819 News for political articles
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 10 --output weekly_1819_politics.json

# Scrape Alabama Daily News for political articles  
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --suffix /news/item --max_pages 10 --output weekly_daily_politics.json
```

**Expected Output**:
- Two JSON files with 50-100 articles each
- Articles from the past week (news sites typically show recent content first)
- Processing time: 5-10 minutes per source

**Pro Tips**:
- Run these commands on the same day each week for consistency
- Use `--max_pages 5` for faster results if you just want recent highlights
- Save files with dates: `weekly_1819_2024-01-15.json`

### Use Case 2: Research Specific Topics

**Scenario**: You're researching coverage of education policy in Alabama news.

**Commands**:
```bash
# Collect all recent articles from both sources
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 20 --output education_research_1819.json

python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 20 --output education_research_daily.json
```

**Post-Processing** (filter for education topics):
```python
import json

# Load the data
with open('education_research_1819.json', 'r') as f:
    data = json.load(f)

# Filter for education-related articles
education_keywords = ['education', 'school', 'teacher', 'student', 'classroom', 'university', 'college']
education_articles = []

for article in data['articles']:
    title_lower = article['title'].lower()
    content_lower = article['content'].lower()
    
    if any(keyword in title_lower or keyword in content_lower for keyword in education_keywords):
        education_articles.append(article)

print(f"Found {len(education_articles)} education-related articles out of {len(data['articles'])} total")

# Save filtered results
filtered_data = {
    'articles': education_articles,
    'metadata': data['metadata'],
    'filter_applied': 'education keywords',
    'original_count': len(data['articles']),
    'filtered_count': len(education_articles)
}

with open('education_articles_filtered.json', 'w') as f:
    json.dump(filtered_data, f, indent=2)
```

**Expected Output**:
- 200-500 total articles collected
- 20-50 education-related articles after filtering
- Research-ready dataset for analysis

### Use Case 3: Daily News Digest

**Scenario**: You want a daily digest of top stories from Alabama news sources.

**Commands**:
```bash
# Get just the latest articles (first 2-3 pages usually contain today's news)
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 3 --output daily_digest_1819.json

python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --suffix /news/item --max_pages 3 --output daily_digest_daily.json
```

**Automation Setup** (Linux/Mac):
```bash
# Create a daily script
cat << 'EOF' > daily_digest.sh
#!/bin/bash
DATE=$(date +%Y-%m-%d)
cd /path/to/opal_project

# Activate virtual environment
source venv/bin/activate

# Run daily scrapes
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 3 --output "daily_${DATE}_1819.json"
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --suffix /news/item --max_pages 3 --output "daily_${DATE}_daily.json"

echo "Daily digest complete for $DATE"
EOF

# Make executable and add to cron
chmod +x daily_digest.sh

# Add to crontab (runs every day at 8 AM)
echo "0 8 * * * /path/to/daily_digest.sh" | crontab -
```

**Expected Output**:
- 20-40 articles per source
- Processing time: 2-3 minutes total
- Consistent daily data collection

## Court Monitoring Use Cases

### Use Case 4: Weekly Court Case Review

**Scenario**: You want to track new court cases filed each week.

**Commands**:
```bash
# Basic weekly court scraping
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court --max_pages 5 --output weekly_court_cases.json

# Or use the configurable extractor for more control
python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed --max-pages 10 --output-prefix weekly_civil
```

**Expected Output**:
- 100-300 court cases
- Both JSON and CSV formats
- Cases from the past week
- Processing time: 10-15 minutes (court scraping is slower due to JavaScript)

### Use Case 5: Research Specific Case Types

**Scenario**: You're researching civil appeals related to business disputes.

**Commands**:
```bash
# Search civil court for appeals
python -m opal.configurable_court_extractor \
    --court civil \
    --date-period 6m \
    --case-category Appeal \
    --exclude-closed \
    --max-pages 15 \
    --output-prefix business_appeals_research
```

**Post-Processing** (filter for business cases):
```python
import json

# Load court case data
with open('business_appeals_research_civil.json', 'r') as f:
    data = json.load(f)

# Filter for business-related cases
business_keywords = ['llc', 'corp', 'company', 'business', 'contract', 'commercial', 'partnership']
business_cases = []

for case in data['cases']:
    title_lower = case['case_title'].lower()
    
    if any(keyword in title_lower for keyword in business_keywords):
        business_cases.append(case)

print(f"Found {len(business_cases)} business-related cases out of {len(data['cases'])} total")

# Save filtered results
filtered_data = {
    'cases': business_cases,
    'metadata': data.get('metadata', {}),
    'filter_applied': 'business keywords',
    'search_parameters': data.get('search_parameters', {}),
    'original_count': len(data['cases']),
    'filtered_count': len(business_cases)
}

with open('business_cases_filtered.json', 'w') as f:
    json.dump(filtered_data, f, indent=2)
```

**Expected Output**:
- 500-1000 total civil appeals
- 50-150 business-related cases after filtering
- Detailed case information for legal research

### Use Case 6: Monitor Specific Courts

**Scenario**: You need to track all activity in the Criminal Appeals Court.

**Commands**:
```bash
# Criminal court cases from the last month
python -m opal.configurable_court_extractor \
    --court criminal \
    --date-period 1m \
    --max-pages 20 \
    --output-prefix monthly_criminal
```

**Expected Output**:
- 200-600 criminal cases
- All case types (appeals, petitions, etc.)
- Complete case information
- Processing time: 15-25 minutes

## Analysis and Research Use Cases

### Use Case 7: Comparative News Analysis

**Scenario**: Compare how different news sources cover the same topics.

**Commands**:
```bash
# Collect comprehensive data from both sources
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 25 --output analysis_1819_full.json
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 25 --output analysis_daily_full.json
```

**Analysis Script**:
```python
import json
from collections import Counter
import re

def analyze_news_coverage(file1, file2, source1_name, source2_name):
    # Load both datasets
    with open(file1, 'r') as f:
        data1 = json.load(f)
    with open(file2, 'r') as f:
        data2 = json.load(f)
    
    # Extract common keywords
    def extract_keywords(articles):
        all_text = ' '.join([article['title'] + ' ' + article['content'] for article in articles])
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        return Counter(words)
    
    keywords1 = extract_keywords(data1['articles'])
    keywords2 = extract_keywords(data2['articles'])
    
    # Find common topics
    common_keywords = set(keywords1.keys()) & set(keywords2.keys())
    
    print(f"\n=== NEWS COVERAGE COMPARISON ===")
    print(f"{source1_name}: {len(data1['articles'])} articles")
    print(f"{source2_name}: {len(data2['articles'])} articles")
    print(f"Common topics: {len(common_keywords)}")
    
    # Top topics by source
    print(f"\nTop topics in {source1_name}:")
    for word, count in keywords1.most_common(10):
        print(f"  {word}: {count}")
    
    print(f"\nTop topics in {source2_name}:")
    for word, count in keywords2.most_common(10):
        print(f"  {word}: {count}")

# Run the analysis
analyze_news_coverage('analysis_1819_full.json', 'analysis_daily_full.json', '1819 News', 'Alabama Daily News')
```

**Expected Output**:
- 500-1000 articles per source
- Keyword frequency analysis
- Topic comparison between sources
- Research insights

### Use Case 8: Long-term Trend Monitoring

**Scenario**: Track political discourse trends over time.

**Setup**: Run this monthly for trend analysis:

```bash
# Monthly data collection script
#!/bin/bash
MONTH=$(date +%Y-%m)

# Create monthly folder
mkdir -p "monthly_data/$MONTH"
cd "monthly_data/$MONTH"

# Collect comprehensive data
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 50 --output "1819_${MONTH}.json"
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 50 --output "daily_${MONTH}.json"

# Court data
python -m opal.configurable_court_extractor --court civil --date-period 1m --max-pages 20 --output-prefix "court_${MONTH}"

echo "Monthly data collection complete for $MONTH"
```

**Trend Analysis**:
```python
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

def analyze_monthly_trends(data_folder):
    monthly_data = {}
    
    # Load all monthly files
    for month_folder in os.listdir(data_folder):
        month_path = os.path.join(data_folder, month_folder)
        if os.path.isdir(month_path):
            # Load 1819 News data
            file_path = os.path.join(month_path, f"1819_{month_folder}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    monthly_data[month_folder] = len(data['articles'])
    
    # Create trend chart
    months = sorted(monthly_data.keys())
    article_counts = [monthly_data[month] for month in months]
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, article_counts, marker='o')
    plt.title('Monthly Article Count Trends')
    plt.xlabel('Month')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_trends.png')
    plt.show()
    
    print(f"Trend analysis complete. Chart saved as 'monthly_trends.png'")

# Run trend analysis
analyze_monthly_trends('monthly_data')
```

## Performance and Efficiency Tips

### Optimization Strategies

1. **Start Small**: Always test with `--max_pages 2-3` first
2. **Peak Hours**: Avoid scraping during business hours (9 AM - 5 PM CST) for better performance
3. **Batch Processing**: Run multiple scrapers in sequence, not parallel
4. **Storage**: Use dated folders to organize output files

### Resource Management

```bash
# Good practice: organized data collection
DATE=$(date +%Y-%m-%d)
mkdir -p "data/$DATE"
cd "data/$DATE"

# Run scrapers with reasonable limits
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 10 --output "1819_${DATE}.json"
# Wait between scrapers to be respectful
sleep 30
python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 10 --output "daily_${DATE}.json"
```

### Error Recovery

```bash
# Robust scraping with retry logic
#!/bin/bash
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 5 --output "test_output.json"; then
        echo "Scraping successful!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "Attempt $RETRY_COUNT failed. Retrying in 60 seconds..."
        sleep 60
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "Scraping failed after $MAX_RETRIES attempts"
    exit 1
fi
```

## Next Steps

After implementing these use cases:

1. **Automate Regular Collection**: Set up cron jobs or scheduled tasks
2. **Data Analysis**: Use Python libraries like pandas for deeper analysis
3. **Visualization**: Create charts and graphs from your collected data
4. **Integration**: Connect OPAL data to databases or other analysis tools

For troubleshooting specific issues, see [Understanding Errors](understanding-errors.md).

For working with the collected data, see [Working with Output Data](working-with-output-data.md).