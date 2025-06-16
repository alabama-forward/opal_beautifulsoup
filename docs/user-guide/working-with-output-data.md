---
layout: default
title: "Working with Output Data"
---

# Working with Output Data

This tutorial shows you how to open, analyze, and work with the data OPAL produces. Whether you're new to data analysis or just getting started with JSON files, this guide will help you unlock the value in your scraped data.

## Opening and Viewing Data Files

### Opening JSON Files

**Method 1: Web Browser (Easiest)**
1. Find your OPAL output file (e.g., `2024-01-15_Parser1819.json`)
2. Drag and drop it into Chrome, Firefox, or Safari
3. The browser will format it nicely for reading

**Method 2: Text Editor**
- **Windows**: Right-click → Open with → Notepad
- **Mac**: Right-click → Open with → TextEdit
- **Better option**: Use VS Code, Notepad++, or Sublime Text for syntax highlighting

**Method 3: Online JSON Viewers**
- Go to jsonviewer.stack.hu or jsonformatter.org
- Copy and paste your JSON content
- Get a formatted, collapsible view

### Opening CSV Files (Court Data)

**Excel or Google Sheets**:
1. Double-click the CSV file
2. It opens automatically with columns properly separated
3. Perfect for sorting, filtering, and creating charts

**LibreOffice Calc** (Free alternative):
1. Open LibreOffice Calc
2. File → Open → Select your CSV file
3. Choose appropriate delimiter (usually comma)

## Understanding JSON Structure

### News Article Data Structure

```json
{
  "articles": [
    {
      "title": "Article headline here",
      "author": "Jane Smith", 
      "date": "January 15, 2024",
      "line_count": 42,
      "content": "Full article text..."
    }
  ],
  "metadata": {
    "source": "https://1819news.com/",
    "parser": "Parser1819",
    "total_articles": 25,
    "scrape_date": "2024-01-15T10:30:45"
  }
}
```

**Key Fields Explained**:
- `articles`: Array containing all scraped articles
- `title`: Article headline
- `author`: Writer's name (may be "Unknown" if not found)
- `date`: Publication date
- `line_count`: Number of lines in the article content
- `content`: Full article text with line breaks preserved
- `metadata`: Information about the scraping process

### Court Case Data Structure

```json
{
  "status": "success",
  "total_cases": 150,
  "cases": [
    {
      "court": "Court of Civil Appeals",
      "case_number": {
        "text": "CL-2024-0001",
        "link": "https://publicportal.alappeals.gov/portal/home/case/caseid/CL-2024-0001"
      },
      "case_title": "Smith v. Jones Construction Company",
      "classification": "Appeal",
      "filed_date": "01/10/2024",
      "status": "Pending"
    }
  ]
}
```

**Key Fields Explained**:
- `cases`: Array of all court cases found
- `court`: Which appeals court
- `case_number`: Case ID with clickable link to full details
- `case_title`: Full case name (parties involved)
- `classification`: Type of legal proceeding
- `filed_date`: When the case was submitted
- `status`: Current case status

## Basic Data Analysis with Python

### Installing Required Packages

```bash
# Install data analysis packages (in your virtual environment)
pip install pandas matplotlib jupyter
```

### Loading and Exploring Data

```python
import json
import pandas as pd
from datetime import datetime

# Load news data
with open('2024-01-15_Parser1819.json', 'r') as f:
    news_data = json.load(f)

# Convert to DataFrame for easier analysis
articles_df = pd.DataFrame(news_data['articles'])

# Basic exploration
print(f"Total articles: {len(articles_df)}")
print(f"Date range: {articles_df['date'].min()} to {articles_df['date'].max()}")
print(f"Authors: {articles_df['author'].nunique()} unique authors")

# Display first few articles
print("\nFirst 3 articles:")
for i, article in articles_df.head(3).iterrows():
    print(f"- {article['title']} by {article['author']}")
```

### Analyzing News Content

```python
import re
from collections import Counter

def analyze_news_content(articles_df):
    """Analyze news articles for common topics and trends"""
    
    # Combine all article text
    all_text = ' '.join(articles_df['title'] + ' ' + articles_df['content'])
    
    # Extract keywords (words 4+ letters, excluding common words)
    stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'said', 'would', 'there', 'could', 'what', 'were', 'when'}
    words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
    keywords = [word for word in words if word not in stop_words]
    
    # Count most common topics
    word_counts = Counter(keywords)
    
    print("=== NEWS CONTENT ANALYSIS ===")
    print(f"Total words analyzed: {len(keywords)}")
    print(f"Unique topics: {len(word_counts)}")
    
    print("\nTop 15 topics mentioned:")
    for word, count in word_counts.most_common(15):
        print(f"  {word}: {count} times")
    
    # Analyze by author
    print(f"\nMost prolific authors:")
    author_counts = articles_df['author'].value_counts().head(5)
    for author, count in author_counts.items():
        print(f"  {author}: {count} articles")
    
    return word_counts, author_counts

# Run the analysis
keywords, authors = analyze_news_content(articles_df)
```

### Analyzing Court Data

```python
def analyze_court_data(json_file):
    """Analyze court case patterns"""
    
    # Load court data
    with open(json_file, 'r') as f:
        court_data = json.load(f)
    
    # Convert to DataFrame
    cases_df = pd.DataFrame(court_data['cases'])
    
    print("=== COURT CASE ANALYSIS ===")
    print(f"Total cases: {len(cases_df)}")
    
    # Analyze by court
    print("\nCases by court:")
    court_counts = cases_df['court'].value_counts()
    for court, count in court_counts.items():
        print(f"  {court}: {count} cases")
    
    # Analyze by case type
    print("\nCases by classification:")
    classification_counts = cases_df['classification'].value_counts()
    for classification, count in classification_counts.items():
        print(f"  {classification}: {count} cases")
    
    # Analyze by status
    print("\nCases by status:")
    status_counts = cases_df['status'].value_counts()
    for status, count in status_counts.items():
        print(f"  {status}: {count} cases")
    
    # Date analysis (convert dates to datetime)
    cases_df['filed_date'] = pd.to_datetime(cases_df['filed_date'], format='%m/%d/%Y', errors='coerce')
    
    print(f"\nDate range: {cases_df['filed_date'].min().strftime('%Y-%m-%d')} to {cases_df['filed_date'].max().strftime('%Y-%m-%d')}")
    
    return cases_df

# Analyze court data
cases_df = analyze_court_data('court_cases.json')
```

## Creating Visualizations

### News Article Trends

```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_news_charts(articles_df):
    """Create charts from news data"""
    
    # Convert dates to datetime
    articles_df['date'] = pd.to_datetime(articles_df['date'], errors='coerce')
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('News Article Analysis', fontsize=16)
    
    # 1. Articles per day
    daily_counts = articles_df['date'].dt.date.value_counts().sort_index()
    axes[0, 0].plot(daily_counts.index, daily_counts.values, marker='o')
    axes[0, 0].set_title('Articles per Day')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Number of Articles')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Article length distribution
    axes[0, 1].hist(articles_df['line_count'], bins=20, alpha=0.7)
    axes[0, 1].set_title('Article Length Distribution')
    axes[0, 1].set_xlabel('Lines in Article')
    axes[0, 1].set_ylabel('Frequency')
    
    # 3. Top authors
    top_authors = articles_df['author'].value_counts().head(8)
    axes[1, 0].bar(range(len(top_authors)), top_authors.values)
    axes[1, 0].set_title('Most Prolific Authors')
    axes[1, 0].set_xlabel('Author')
    axes[1, 0].set_ylabel('Number of Articles')
    axes[1, 0].set_xticks(range(len(top_authors)))
    axes[1, 0].set_xticklabels(top_authors.index, rotation=45, ha='right')
    
    # 4. Word cloud of common topics (if wordcloud is installed)
    try:
        from wordcloud import WordCloud
        all_text = ' '.join(articles_df['title'])
        wordcloud = WordCloud(width=400, height=300, background_color='white').generate(all_text)
        axes[1, 1].imshow(wordcloud, interpolation='bilinear')
        axes[1, 1].set_title('Common Topics in Headlines')
        axes[1, 1].axis('off')
    except ImportError:
        # If wordcloud not available, show article count by month
        monthly_counts = articles_df['date'].dt.to_period('M').value_counts().sort_index()
        axes[1, 1].bar(range(len(monthly_counts)), monthly_counts.values)
        axes[1, 1].set_title('Articles per Month')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Number of Articles')
    
    plt.tight_layout()
    plt.savefig('news_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Charts saved as 'news_analysis.png'")

# Create charts
create_news_charts(articles_df)
```

### Court Case Visualizations

```python
def create_court_charts(cases_df):
    """Create charts from court data"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Court Case Analysis', fontsize=16)
    
    # 1. Cases by court
    court_counts = cases_df['court'].value_counts()
    axes[0, 0].pie(court_counts.values, labels=court_counts.index, autopct='%1.1f%%')
    axes[0, 0].set_title('Cases by Court')
    
    # 2. Cases by classification
    classification_counts = cases_df['classification'].value_counts()
    axes[0, 1].bar(classification_counts.index, classification_counts.values)
    axes[0, 1].set_title('Cases by Type')
    axes[0, 1].set_xlabel('Classification')
    axes[0, 1].set_ylabel('Number of Cases')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Cases over time
    cases_df['filed_month'] = cases_df['filed_date'].dt.to_period('M')
    monthly_cases = cases_df['filed_month'].value_counts().sort_index()
    axes[1, 0].plot(range(len(monthly_cases)), monthly_cases.values, marker='o')
    axes[1, 0].set_title('Cases Filed Over Time')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Number of Cases')
    
    # 4. Case status
    status_counts = cases_df['status'].value_counts()
    axes[1, 1].bar(status_counts.index, status_counts.values)
    axes[1, 1].set_title('Cases by Status')
    axes[1, 1].set_xlabel('Status')
    axes[1, 1].set_ylabel('Number of Cases')
    
    plt.tight_layout()
    plt.savefig('court_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Charts saved as 'court_analysis.png'")

# Create court charts
create_court_charts(cases_df)
```

## Data Export and Conversion

### Convert JSON to CSV

```python
def json_to_csv(json_file, csv_file):
    """Convert news JSON to CSV format"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Convert articles to DataFrame
    df = pd.DataFrame(data['articles'])
    
    # Save to CSV
    df.to_csv(csv_file, index=False)
    print(f"Converted {len(df)} articles to {csv_file}")

# Convert your news data
json_to_csv('2024-01-15_Parser1819.json', 'news_articles.csv')
```

### Create Summary Reports

```python
def create_summary_report(articles_df, output_file):
    """Create a summary report of news data"""
    
    with open(output_file, 'w') as f:
        f.write("=== NEWS SCRAPING SUMMARY REPORT ===\n\n")
        
        f.write(f"Total articles collected: {len(articles_df)}\n")
        f.write(f"Date range: {articles_df['date'].min()} to {articles_df['date'].max()}\n")
        f.write(f"Unique authors: {articles_df['author'].nunique()}\n")
        f.write(f"Average article length: {articles_df['line_count'].mean():.1f} lines\n\n")
        
        f.write("TOP AUTHORS:\n")
        top_authors = articles_df['author'].value_counts().head(5)
        for author, count in top_authors.items():
            f.write(f"  {author}: {count} articles\n")
        
        f.write("\nLONGEST ARTICLES:\n")
        longest = articles_df.nlargest(3, 'line_count')
        for _, article in longest.iterrows():
            f.write(f"  {article['title'][:60]}... ({article['line_count']} lines)\n")
        
        f.write("\nMOST RECENT ARTICLES:\n")
        recent = articles_df.nlargest(5, 'date')
        for _, article in recent.iterrows():
            f.write(f"  {article['date']}: {article['title'][:60]}...\n")
    
    print(f"Summary report saved to {output_file}")

# Create summary
create_summary_report(articles_df, 'news_summary.txt')
```

## Advanced Data Analysis

### Text Analysis and Sentiment

```python
# Install required packages first: pip install textblob
from textblob import TextBlob

def analyze_sentiment(articles_df):
    """Analyze sentiment of news articles"""
    
    sentiments = []
    
    for _, article in articles_df.iterrows():
        # Analyze title sentiment
        blob = TextBlob(article['title'])
        sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        sentiments.append({
            'title': article['title'][:50] + '...',
            'sentiment': sentiment,
            'sentiment_label': 'Positive' if sentiment > 0.1 else 'Negative' if sentiment < -0.1 else 'Neutral'
        })
    
    sentiment_df = pd.DataFrame(sentiments)
    
    print("=== SENTIMENT ANALYSIS ===")
    sentiment_counts = sentiment_df['sentiment_label'].value_counts()
    for label, count in sentiment_counts.items():
        print(f"{label}: {count} articles ({count/len(sentiment_df)*100:.1f}%)")
    
    # Show most positive and negative headlines
    print("\nMost positive headlines:")
    positive = sentiment_df.nlargest(3, 'sentiment')
    for _, row in positive.iterrows():
        print(f"  {row['title']} (score: {row['sentiment']:.2f})")
    
    print("\nMost negative headlines:")
    negative = sentiment_df.nsmallest(3, 'sentiment')
    for _, row in negative.iterrows():
        print(f"  {row['title']} (score: {row['sentiment']:.2f})")
    
    return sentiment_df

# Analyze sentiment
sentiment_results = analyze_sentiment(articles_df)
```

### Topic Modeling

```python
# Install required packages: pip install scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def find_topics(articles_df, n_topics=5):
    """Find common topics in articles using clustering"""
    
    # Combine title and content for analysis
    texts = [f"{row['title']} {row['content'][:200]}" for _, row in articles_df.iterrows()]
    
    # Convert text to numerical features
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    text_vectors = vectorizer.fit_transform(texts)
    
    # Find topics using clustering
    kmeans = KMeans(n_clusters=n_topics, random_state=42)
    clusters = kmeans.fit_predict(text_vectors)
    
    # Get top words for each topic
    feature_names = vectorizer.get_feature_names_out()
    
    print("=== TOPIC ANALYSIS ===")
    for i in range(n_topics):
        top_words_idx = kmeans.cluster_centers_[i].argsort()[-10:][::-1]
        top_words = [feature_names[idx] for idx in top_words_idx]
        print(f"Topic {i+1}: {', '.join(top_words)}")
        
        # Show example articles from this topic
        topic_articles = articles_df[clusters == i]
        print(f"  Example articles ({len(topic_articles)} total):")
        for _, article in topic_articles.head(2).iterrows():
            print(f"    - {article['title'][:60]}...")
        print()

# Find topics
find_topics(articles_df)
```

## Working with Multiple Data Sources

### Combining News Sources

```python
def combine_news_sources(file1, file2, output_file):
    """Combine data from multiple news sources"""
    
    # Load both files
    with open(file1, 'r') as f:
        data1 = json.load(f)
    with open(file2, 'r') as f:
        data2 = json.load(f)
    
    # Combine articles
    all_articles = data1['articles'] + data2['articles']
    
    # Create combined dataset
    combined_data = {
        'articles': all_articles,
        'metadata': {
            'combined_from': [file1, file2],
            'total_articles': len(all_articles),
            'source1_count': len(data1['articles']),
            'source2_count': len(data2['articles']),
            'combined_date': datetime.now().isoformat()
        }
    }
    
    # Save combined data
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"Combined {len(all_articles)} articles from 2 sources")
    print(f"Source 1: {len(data1['articles'])} articles")
    print(f"Source 2: {len(data2['articles'])} articles")
    print(f"Saved to: {output_file}")

# Combine multiple sources
combine_news_sources('1819_news.json', 'daily_news.json', 'combined_news.json')
```

### Cross-Source Analysis

```python
def compare_news_sources(file1, file2, source1_name, source2_name):
    """Compare coverage between two news sources"""
    
    # Load and prepare data
    with open(file1, 'r') as f:
        data1 = json.load(f)
    with open(file2, 'r') as f:
        data2 = json.load(f)
    
    df1 = pd.DataFrame(data1['articles'])
    df2 = pd.DataFrame(data2['articles'])
    
    print(f"=== COMPARING {source1_name.upper()} vs {source2_name.upper()} ===")
    
    # Basic stats
    print(f"{source1_name}: {len(df1)} articles")
    print(f"{source2_name}: {len(df2)} articles")
    
    # Average article length
    print(f"\nAverage article length:")
    print(f"  {source1_name}: {df1['line_count'].mean():.1f} lines")
    print(f"  {source2_name}: {df2['line_count'].mean():.1f} lines")
    
    # Most active authors
    print(f"\nMost active authors:")
    print(f"  {source1_name}: {df1['author'].value_counts().index[0]} ({df1['author'].value_counts().iloc[0]} articles)")
    print(f"  {source2_name}: {df2['author'].value_counts().index[0]} ({df2['author'].value_counts().iloc[0]} articles)")
    
    # Find common topics
    def get_top_words(df, n=10):
        all_text = ' '.join(df['title'] + ' ' + df['content'])
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        return Counter(words).most_common(n)
    
    words1 = dict(get_top_words(df1))
    words2 = dict(get_top_words(df2))
    
    common_topics = set(words1.keys()) & set(words2.keys())
    print(f"\nCommon topics covered: {len(common_topics)}")
    for topic in sorted(common_topics)[:5]:
        print(f"  {topic}: {source1_name}({words1[topic]}) vs {source2_name}({words2[topic]})")

# Compare sources
compare_news_sources('1819_news.json', 'daily_news.json', '1819 News', 'Alabama Daily News')
```

## Data Integration with Other Tools

### Export to Database

```python
import sqlite3

def save_to_database(json_file, db_file):
    """Save news data to SQLite database"""
    
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Create database connection
    conn = sqlite3.connect(db_file)
    
    # Create table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            date TEXT,
            line_count INTEGER,
            content TEXT,
            source TEXT
        )
    ''')
    
    # Insert articles
    for article in data['articles']:
        conn.execute('''
            INSERT INTO articles (title, author, date, line_count, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            article['title'],
            article['author'],
            article['date'],
            article['line_count'],
            article['content'],
            data['metadata']['parser']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"Saved {len(data['articles'])} articles to database: {db_file}")

# Save to database
save_to_database('news_data.json', 'news.db')
```

### Export for Excel Analysis

```python
def create_excel_report(articles_df, filename):
    """Create an Excel file with multiple sheets for analysis"""
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main data
        articles_df.to_excel(writer, sheet_name='Articles', index=False)
        
        # Summary statistics
        summary_stats = pd.DataFrame({
            'Metric': ['Total Articles', 'Unique Authors', 'Avg Length', 'Date Range'],
            'Value': [
                len(articles_df),
                articles_df['author'].nunique(),
                f"{articles_df['line_count'].mean():.1f} lines",
                f"{articles_df['date'].min()} to {articles_df['date'].max()}"
            ]
        })
        summary_stats.to_excel(writer, sheet_name='Summary', index=False)
        
        # Top authors
        top_authors = articles_df['author'].value_counts().head(10).reset_index()
        top_authors.columns = ['Author', 'Article Count']
        top_authors.to_excel(writer, sheet_name='Top Authors', index=False)
        
        # Articles by date
        daily_counts = articles_df['date'].value_counts().sort_index().reset_index()
        daily_counts.columns = ['Date', 'Article Count']
        daily_counts.to_excel(writer, sheet_name='Daily Counts', index=False)
    
    print(f"Excel report saved as: {filename}")

# Create Excel report
create_excel_report(articles_df, 'news_analysis.xlsx')
```

## Next Steps

Now that you know how to work with OPAL's output data:

1. **Automate Analysis**: Create scripts that automatically analyze new data as you collect it
2. **Build Dashboards**: Use tools like Streamlit or Dash to create interactive data dashboards
3. **Set Up Monitoring**: Track trends over time by regularly collecting and analyzing data
4. **Share Insights**: Export charts and summaries to share your findings

For collecting more data, see [Common Use Cases](common-use-cases.md).

For troubleshooting data issues, see [Understanding Errors](understanding-errors.md).