---
layout: default
title: "Court Case Scraper Extension Requirements"
---

# Court Case Scraper Extension Requirements

To help you build this court case scraper extension while maintaining OPAL's modularity, I'll need the following information:

## 1. Website Details
- **The URL of the court case website**
Example URL: https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~0~totalElements~0~totalPages~0%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29
- **Example URLs of pages containing the tables you want to scrape**
Example URL after pagination of next batch of table elements: https://publicportal.alappeals.gov/portal/search/case/results?criteria=~%28advanced~false~courtID~%2768f021c4-6a44-4735-9a76-5360b2e8af13~page~%28size~25~number~1~totalElements~317~totalPages~13%29~sort~%28sortBy~%27caseHeader.filedDate~sortDesc~true%29~case~%28caseCategoryID~1000000~caseNumberQueryTypeID~10463~caseTitleQueryTypeID~300054~filedDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025~excludeClosed~false%29%29
- **Screenshots or HTML snippets of the table structure**

## 2. Data Requirements
- **What specific data fields do you need from the tables?** (case number, parties, dates, status, etc.)
I will need to access the following html fields for data

Column 1 Title: <th role="columnheader" scope="col" aria-label="Court: Not sorted. Activate to sort ascending." aria-sort="none" class="text-start sortable"><span>Court</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th> 
<span>Court</span>

Column 1 Content Follows this pattern: <td class="text-start">Alabama Supreme Court</td>

Column 2 Title: <th role="columnheader" scope="col" aria-label="Case Number: Not sorted. Activate to sort ascending." aria-sort="none" class="text-start sortable"><span>Case Number</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th>
<span>Case Number</span>

Column 2 Content Follows this pattern:
<a href="/portal/court/68f021c4-6a44-4735-9a76-5360b2e8af13/case/d024d958-58a1-41c9-9fae-39c645c7977e" class=""> SC-2025-0424 </a>


Column 3 Title: <th role="columnheader" scope="col" aria-label="Case Title: Not sorted. Activate to sort ascending." aria-sort="none" class="text-start sortable"><span>Case Title</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th>
<span>Case Title</span>

Column 3 Content Follows this pattern: <td class="text-start">Frank Thomas Shumate, Jr. v. Berry Contracting L.P. d/b/a Bay Ltd.</td>

Column 4 Title: <th role="columnheader" scope="col" aria-label="Classification: Not sorted. Activate to sort ascending." aria-sort="none" class="text-start sortable"><span>Classification</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th>
<span>Classification</span>

Column 4 Content Follows this pattern: <td class="text-start">Appeal - Civil - Injunction Other</td>

Column 5 Title: <th role="columnheader" scope="col" aria-label="Filed Date: Sorted descending. Activate to sort ascending." aria-sort="descending" class="text-start sortable active desc"><span>Filed Date</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th>
<span>Filed Date</span>

Column 5 Content Follows this pattern: <td class="text-start"> 06/10/2025 </td>

Column 6 Title: <th role="columnheader" scope="col" aria-label="Open / Closed: Not sorted. Activate to sort ascending." aria-sort="none" class="text-start sortable"><span>Open / Closed</span><i aria-hidden="true" class="v-icon notranslate v-data-table-header__icon mdi mdi-arrow-up theme--dark" style="font-size: 18px;"></i></th>
<span>Open / Closed</span>

Column 6 Content Follows this pattern: <td class="text-start"> Open </td>

- **Do you need data from multiple tables per page or one main table?**

I only want one table with all of the results of all of the pages at that url. Even if pagination is used to reduce the number of table elements that appear at a time, I want all the results in a single table.

- **Any specific formatting requirements for the extracted data?**

## 3. Navigation Pattern
- **Does the site use pagination like the news sites?**
The pagination is not the same. The content is grouped into small chunks, but accessible at the same base url.

- **Are there search/filter parameters in the URL?**
There are multiple search parameters in the URL. For example, here are the search terms for this url
[case~%28caseCategoryID~1000000, caseNumberQueryTypeID~10463, aseTitleQueryTypeID~300054, iledDateChoice~%27-1y~filedDateStart~%2706%2a2f11%2a2f2024~filedDateEnd~%2706%2a2f11%2a2f2025, excludeClosed~false%29%29]
- **Do you need to follow links within tables to get additional details?**

I do not want to follow the links within the table, but I do want to store the text and the reference embedded in the link.

## 4. Technical Considerations
- **Does the site require authentication?**
No
- **Is the content loaded dynamically (JavaScript) or static HTML?**
Dynamically
- **Any rate limiting concerns we should be aware of?**
Please keep the rate limits low

## Proposed Extension Architecture

Based on OPAL's current architecture, here's how we'd extend it:

1. **Create a new parser class** (e.g., `CourtCaseParser`) extending `NewsParser` in `parser_module.py`
2. **Adapt or create a new URL discovery function** if the pagination pattern differs from the news sites
3. **Modify the CLI** in `main.py` to add the court parser option
4. **Ensure the output format** makes sense for tabular data (might need to adjust from the line-by-line article format)

## Next Steps

Please provide:
1. The court website URL
2. Description of the table structure you need to parse
3. Any specific requirements or constraints

This will help me design the extension to fit seamlessly with your existing OPAL architecture.