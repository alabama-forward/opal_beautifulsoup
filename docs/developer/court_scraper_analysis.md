# Court Scraper Analysis

The ParserAppealsAL scraper is different from the news scrapers. This is because of the courts' use of JavaScript, which renders content dynamically. 

## 1. Dynamic JavaScript-Rendered Content
- The site loads content dynamically, which means BeautifulSoup alone won't work
- You'll need Selenium or Playwright to render JavaScript before parsing

## 2. Complex URL-Based Pagination
- Pagination uses URL parameters (`page~(number~0)` becomes `page~(number~1)`)
- Total pages/elements are embedded in the URL (`totalElements~317~totalPages~13`)
- This is very different from the simple `/page/2` pattern in the news scrapers

## 3. Structured Table Data
- We needed 6 specific columns: Court, Case Number, Case Title, Classification, Filed Date, Open/Closed
- Case Numbers contained links we wanted to preserve (both text and href)
- We wanted all paginated results combined into one table

## 4. Custom URL Encoding
- The URLs use a unique encoding scheme with `~` and `%2a2f` (for slashes)
- Search parameters are complex with date ranges and multiple filters

## Key Challenges:
- Need to handle JavaScript rendering
- Must parse and manipulate the encoded URL format for pagination
- Need to extract both text and href attributes from case number links
- Different data structure (tabular vs. article paragraphs)