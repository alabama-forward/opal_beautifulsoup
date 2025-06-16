# Output Formats

For detailed output examples with real data, see [Output Examples](output-examples.md).

## Overview

OPAL produces structured data in two main formats:
- **JSON**: Complete data with all fields and metadata
- **CSV**: Court data in spreadsheet format (court scraping only)

## Data Processing

### Python Analysis
```python
import json
import pandas as pd

# Load and analyze news data
with open('output.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame for analysis
df = pd.DataFrame(data['articles'])
print(f"Found {len(df)} articles")
print(df['date'].value_counts())
```

### Excel Integration
- JSON files can be imported into Excel using Power Query
- CSV files open directly in Excel
- Use pivot tables for data analysis

### Database Storage
The structured JSON format works well with:
- MongoDB (document storage)
- PostgreSQL (JSON columns)
- SQLite (for small datasets)

## Advanced Processing

### Filtering Results
```python
# Filter articles by date
recent_articles = [
    article for article in data['articles'] 
    if article['date'] >= '2024-01-01'
]
```

### Data Validation
```python
# Check for missing data
for article in data['articles']:
    if not article.get('title'):
        print(f"Missing title: {article}")
```

For complete output structure and real examples, see [Output Examples](output-examples.md).