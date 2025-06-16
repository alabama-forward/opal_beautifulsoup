**OPAL (Oppositional Positions in Alabama)**

This is a web scraping tool that extracts content from Alabama news sites and court records, returning structured data as JSON objects for use in language analysis and research projects. OPAL supports multiple content sources including news articles and court case records.

**SETUP:** 
```bash
# Check your system first
python check_prerequisites.py

# Install OPAL
pip install -e .
```

For detailed setup instructions, see the [Complete Setup Guide](docs/getting-started/complete-setup-guide.md). 

**USAGE:** This project is a specific application of the beautifulsoup package to support the extract and analysis of conservative news sites in Alabama. This is built by progressives in Alabama for progressives in Alabama. The BaseParser object can be updated to include additional news sources if desired.

**FEATURES:** This project is based on beautifulsoup4 and Selenium for JavaScript-rendered content. It is built using OOP with the primary object being the BaseParser. The site-specific parsers are extensions of the parent BaseParser class.

Currently available parsers:
- **Parser1819**: Extracts articles from 1819news.com
- **ParserDailyNews**: Extracts articles from Alabama Daily News
- **ParserAppealsAL**: Extracts court case data from Alabama Appeals Court Public Portal (uses Selenium for JavaScript rendering)

You can run this program from your terminal using the following command:
```bash
python -m opal --url <base_url> --parser <parser_name> [--suffix <suffix>] [--max_pages <number>]
```

**Required arguments:**
- `--url`: Base URL of the site to scrape
- `--parser`: Parser to use (choices: Parser1819, ParserDailyNews, court)

**Optional arguments:**
- `--suffix`: URL suffix to identify article pages (e.g., '/news/item/') - only used for news parsers
- `--max_pages`: Maximum number of pages to process (default: no limit)

**Examples:**
```bash
# Scrape news articles from 1819news
python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5

# Scrape court cases from Alabama Appeals Court
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser court
```

The url_catcher module handles URL discovery for news sites, while court parsers use specialized pagination logic for handling complex query parameters.

The program returns structured JSON data that includes:
- **News articles**: title, author, date, line count, and full text content
- **Court cases**: court name, case number (with link), case title, classification, filed date, and status

Output files are saved with timestamps in the format: `YYYY-MM-DD_ParserName.json`

**CONFIGURATION:** No special configuration outside of set up is necessary. This program doesn't use nor require private details to work.

**CONTRIBUTING GUIDELINES:** To contribute to this project, please reach out to Gabri at gabri@alforward.org.

**LICENSE:** Use it wisely. Use it for progressive purposes. Don't sell it! (It wouldn't be work much anyway)

**ACKNOWLEDGEMENT:** This project was created by Gabriel Cabán Cubero, Data Director at Alabama Forward.
