# Interactive Command Builder

Build your OPAL commands with this interactive tool. Select your options and get the exact command to run.

<style>
.command-builder {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
    color: #333;
}

.form-group input, .form-group select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.command-output {
    background: #2d3748;
    color: #e2e8f0;
    padding: 15px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    margin: 20px 0;
    position: relative;
}

.copy-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #4299e1;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
}

.copy-btn:hover {
    background: #3182ce;
}

.example-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.example-card {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.2s;
}

.example-card:hover {
    border-color: #4299e1;
    box-shadow: 0 2px 8px rgba(66, 153, 225, 0.15);
}

.example-card h4 {
    margin: 0 0 8px 0;
    color: #2d3748;
    font-size: 16px;
}

.example-card p {
    margin: 0 0 10px 0;
    color: #4a5568;
    font-size: 14px;
}

.example-card code {
    background: #2d3748;
    color: #e2e8f0;
    padding: 8px;
    border-radius: 3px;
    font-size: 12px;
    display: block;
    word-break: break-all;
}

.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
    border-bottom: 1px dotted #999;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

.warning {
    background: #fed7d7;
    border-left: 4px solid #f56565;
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
}

.info {
    background: #bee3f8;
    border-left: 4px solid #4299e1;
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
}
</style>

## Quick Examples Gallery

Click any example to load it into the builder:

<div class="example-gallery">
    <div class="example-card" onclick="loadExample('news-basic')">
        <h4>📰 Basic News Scraping</h4>
        <p>Scrape recent articles from 1819 News</p>
        <code>python -m opal --url https://1819news.com/ --parser Parser1819 --suffix /news/item --max_pages 5</code>
    </div>
    
    <div class="example-card" onclick="loadExample('court-basic')">
        <h4>⚖️ Basic Court Cases</h4>
        <p>Extract court cases from Alabama Appeals</p>
        <code>python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL --max_pages 3</code>
    </div>
    
    <div class="example-card" onclick="loadExample('news-daily')">
        <h4>📅 Daily News Digest</h4>
        <p>Quick daily update from Alabama Daily News</p>
        <code>python -m opal --url https://www.aldailynews.com/ --parser ParserDailyNews --max_pages 2</code>
    </div>
    
    <div class="example-card" onclick="loadExample('court-civil')">
        <h4>🏛️ Civil Court Search</h4>
        <p>Search civil court cases from last week</p>
        <code>python -m opal.configurable_court_extractor --court civil --date-period 7d --exclude-closed</code>
    </div>
    
    <div class="example-card" onclick="loadExample('court-custom')">
        <h4>🔍 Custom Court Search</h4>
        <p>Advanced court search with filters</p>
        <code>python -m opal.configurable_court_extractor --court civil --date-period 1m --case-category Appeal --max-pages 10</code>
    </div>
    
    <div class="example-card" onclick="loadExample('research-mode')">
        <h4>🔬 Research Mode</h4>
        <p>Comprehensive data collection for analysis</p>
        <code>python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 20</code>
    </div>
</div>

## Interactive Command Builder

<div class="command-builder">
    <h3>Build Your Command</h3>
    
    <div class="form-group">
        <label for="command-type">Command Type:</label>
        <select id="command-type" onchange="updateCommandType()">
            <option value="basic">Basic OPAL (python -m opal)</option>
            <option value="court-extractor">Court Extractor (python -m opal.configurable_court_extractor)</option>
        </select>
    </div>

    <!-- Basic OPAL Options -->
    <div id="basic-options">
        <div class="form-group">
            <label for="url">
                <span class="tooltip">URL (required)
                    <span class="tooltiptext">The website URL to scrape. Must be a supported site.</span>
                </span>
            </label>
            <select id="url" onchange="updateParser()">
                <option value="">Select a website...</option>
                <option value="https://1819news.com/">1819 News</option>
                <option value="https://www.aldailynews.com/">Alabama Daily News</option>
                <option value="https://publicportal.alappeals.gov/portal/search/case/results">Alabama Appeals Court</option>
                <option value="custom">Custom URL...</option>
            </select>
            <input type="text" id="custom-url" placeholder="Enter custom URL..." style="display:none; margin-top:5px;" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label for="parser">
                <span class="tooltip">Parser (required)
                    <span class="tooltiptext">The parser that matches your chosen website.</span>
                </span>
            </label>
            <select id="parser" onchange="updateCommand()">
                <option value="">Auto-detect from URL</option>
                <option value="Parser1819">Parser1819 (for 1819news.com)</option>
                <option value="ParserDailyNews">ParserDailyNews (for aldailynews.com)</option>
                <option value="ParserAppealsAL">ParserAppealsAL (for court portal)</option>
            </select>
        </div>

        <div class="form-group" id="suffix-group">
            <label for="suffix">
                <span class="tooltip">URL Suffix (optional)
                    <span class="tooltiptext">Filter URLs containing this pattern. Helps identify article pages.</span>
                </span>
            </label>
            <input type="text" id="suffix" placeholder="e.g., /news/item" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label for="max-pages">
                <span class="tooltip">Max Pages (optional)
                    <span class="tooltiptext">Maximum number of pages to process. Default is 5 for basic, unlimited for court extractor.</span>
                </span>
            </label>
            <input type="number" id="max-pages" placeholder="e.g., 5" min="1" max="100" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label for="output">
                <span class="tooltip">Output File (optional)
                    <span class="tooltiptext">Where to save results. Default generates timestamped filename.</span>
                </span>
            </label>
            <input type="text" id="output" placeholder="e.g., my_results.json" onchange="updateCommand()">
        </div>
    </div>

    <!-- Court Extractor Options -->
    <div id="court-options" style="display:none;">
        <div class="form-group">
            <label for="court-type">
                <span class="tooltip">Court Type (required)
                    <span class="tooltiptext">Which Alabama court to search: civil, criminal, or supreme.</span>
                </span>
            </label>
            <select id="court-type" onchange="updateCommand()">
                <option value="">Select court...</option>
                <option value="civil">Civil Appeals Court</option>
                <option value="criminal">Criminal Appeals Court</option>
                <option value="supreme">Supreme Court</option>
            </select>
        </div>

        <div class="form-group">
            <label for="date-period">
                <span class="tooltip">Date Period
                    <span class="tooltiptext">How far back to search for cases. Recent periods are faster.</span>
                </span>
            </label>
            <select id="date-period" onchange="updateCommand()">
                <option value="">No date filter</option>
                <option value="7d">Last 7 days</option>
                <option value="1m" selected>Last month</option>
                <option value="3m">Last 3 months</option>
                <option value="6m">Last 6 months</option>
                <option value="1y">Last year</option>
                <option value="custom">Custom date range...</option>
            </select>
        </div>

        <div id="custom-dates" style="display:none;">
            <div class="form-group">
                <label for="start-date">Start Date (YYYY-MM-DD):</label>
                <input type="date" id="start-date" onchange="updateCommand()">
            </div>
            <div class="form-group">
                <label for="end-date">End Date (YYYY-MM-DD):</label>
                <input type="date" id="end-date" onchange="updateCommand()">
            </div>
        </div>

        <div class="form-group">
            <label for="case-category">
                <span class="tooltip">Case Category (optional)
                    <span class="tooltiptext">Filter by type of legal proceeding.</span>
                </span>
            </label>
            <select id="case-category" onchange="updateCommand()">
                <option value="">All categories</option>
                <option value="Appeal">Appeal</option>
                <option value="Certiorari">Certiorari</option>
                <option value="Original Proceeding">Original Proceeding</option>
                <option value="Petition">Petition</option>
                <option value="Certified Question">Certified Question</option>
            </select>
        </div>

        <div class="form-group">
            <label for="case-number">
                <span class="tooltip">Case Number Filter (optional)
                    <span class="tooltiptext">Filter by case number pattern. Use * for wildcards.</span>
                </span>
            </label>
            <input type="text" id="case-number" placeholder="e.g., CL-2024-* or specific number" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label for="case-title">
                <span class="tooltip">Case Title Filter (optional)
                    <span class="tooltiptext">Filter by words in case title.</span>
                </span>
            </label>
            <input type="text" id="case-title" placeholder="e.g., Smith, contract, appeal" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" id="exclude-closed" onchange="updateCommand()">
                <span class="tooltip">Exclude Closed Cases
                    <span class="tooltiptext">Only show active/pending cases, skip completed ones.</span>
                </span>
            </label>
        </div>

        <div class="form-group">
            <label for="court-max-pages">
                <span class="tooltip">Max Pages (optional)
                    <span class="tooltiptext">Limit pages processed. Useful for large result sets.</span>
                </span>
            </label>
            <input type="number" id="court-max-pages" placeholder="e.g., 10" min="1" max="100" onchange="updateCommand()">
        </div>

        <div class="form-group">
            <label for="output-prefix">
                <span class="tooltip">Output Prefix (optional)
                    <span class="tooltiptext">Prefix for output filenames. Will generate both JSON and CSV.</span>
                </span>
            </label>
            <input type="text" id="output-prefix" placeholder="e.g., civil_cases_2024" onchange="updateCommand()">
        </div>
    </div>
</div>

## Generated Command

<div class="command-output" id="command-output">
<button class="copy-btn" onclick="copyCommand()">Copy</button>
<span id="command-text">Select options above to generate your command...</span>
</div>

<div class="info">
<strong>💡 Pro Tip:</strong> After copying your command, open your terminal, activate your virtual environment with <code>source venv/bin/activate</code> (or <code>venv\Scripts\activate</code> on Windows), then paste and run the command.
</div>

## Command Validation

<div id="validation-messages"></div>

## What Happens Next?

After running your command:

1. **For News Scraping**: You'll get a JSON file with articles including title, author, date, and full content
2. **For Court Scraping**: You'll get both JSON and CSV files with case details, plus progress updates in the terminal
3. **Files are named with timestamps** for easy organization
4. **Check the terminal output** for any warnings or helpful information

## Advanced Options

### Environment Variables

You can set these environment variables to customize behavior:

```bash
# Set default output directory
export OPAL_OUTPUT_DIR="/path/to/outputs"

# Set default rate limiting (seconds between requests)
export OPAL_RATE_LIMIT=2.0

# Enable debug mode
export OPAL_DEBUG=1
```

### Combining with Other Tools

**Process results with jq (JSON processor):**
```bash
# Extract just article titles
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2 \
  && cat *Parser1819*.json | jq '.articles[].title'

# Count court cases by status
python -m opal.configurable_court_extractor --court civil --date-period 7d \
  && cat *civil*.json | jq '.cases | group_by(.status) | map({status: .[0].status, count: length})'
```

**Save to specific directory:**
```bash
mkdir -p ~/opal-results/$(date +%Y-%m)
cd ~/opal-results/$(date +%Y-%m)
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 5
```

## Need Help?

- **Command not working?** Check the [Understanding Errors](understanding-errors.md) guide
- **Want to see examples?** Visit [Common Use Cases](common-use-cases.md) 
- **Need setup help?** Try the [Prerequisites Checker](../getting-started/prerequisites-checker.md)

<script>
const examples = {
    'news-basic': {
        commandType: 'basic',
        url: 'https://1819news.com/',
        parser: 'Parser1819',
        suffix: '/news/item',
        maxPages: '5'
    },
    'court-basic': {
        commandType: 'basic',
        url: 'https://publicportal.alappeals.gov/portal/search/case/results',
        parser: 'ParserAppealsAL',
        maxPages: '3'
    },
    'news-daily': {
        commandType: 'basic',
        url: 'https://www.aldailynews.com/',
        parser: 'ParserDailyNews',
        maxPages: '2'
    },
    'court-civil': {
        commandType: 'court-extractor',
        courtType: 'civil',
        datePeriod: '7d',
        excludeClosed: true
    },
    'court-custom': {
        commandType: 'court-extractor',
        courtType: 'civil',
        datePeriod: '1m',
        caseCategory: 'Appeal',
        maxPages: '10'
    },
    'research-mode': {
        commandType: 'basic',
        url: 'https://1819news.com/',
        parser: 'Parser1819',
        maxPages: '20'
    }
};

function loadExample(exampleId) {
    const example = examples[exampleId];
    if (!example) return;
    
    // Set command type
    document.getElementById('command-type').value = example.commandType;
    updateCommandType();
    
    if (example.commandType === 'basic') {
        if (example.url) document.getElementById('url').value = example.url;
        if (example.parser) document.getElementById('parser').value = example.parser;
        if (example.suffix) document.getElementById('suffix').value = example.suffix;
        if (example.maxPages) document.getElementById('max-pages').value = example.maxPages;
        if (example.output) document.getElementById('output').value = example.output;
    } else {
        if (example.courtType) document.getElementById('court-type').value = example.courtType;
        if (example.datePeriod) document.getElementById('date-period').value = example.datePeriod;
        if (example.caseCategory) document.getElementById('case-category').value = example.caseCategory;
        if (example.caseNumber) document.getElementById('case-number').value = example.caseNumber;
        if (example.caseTitle) document.getElementById('case-title').value = example.caseTitle;
        if (example.excludeClosed) document.getElementById('exclude-closed').checked = example.excludeClosed;
        if (example.maxPages) document.getElementById('court-max-pages').value = example.maxPages;
        if (example.outputPrefix) document.getElementById('output-prefix').value = example.outputPrefix;
    }
    
    updateCommand();
}

function updateCommandType() {
    const commandType = document.getElementById('command-type').value;
    const basicOptions = document.getElementById('basic-options');
    const courtOptions = document.getElementById('court-options');
    
    if (commandType === 'basic') {
        basicOptions.style.display = 'block';
        courtOptions.style.display = 'none';
    } else {
        basicOptions.style.display = 'none';
        courtOptions.style.display = 'block';
    }
    
    updateCommand();
}

function updateParser() {
    const url = document.getElementById('url').value;
    const parser = document.getElementById('parser');
    const customUrl = document.getElementById('custom-url');
    const suffixGroup = document.getElementById('suffix-group');
    const suffix = document.getElementById('suffix');
    
    if (url === 'custom') {
        customUrl.style.display = 'block';
        parser.value = '';
        suffix.value = '';
    } else {
        customUrl.style.display = 'none';
        
        // Auto-select parser based on URL
        if (url.includes('1819news.com')) {
            parser.value = 'Parser1819';
            suffix.value = '/news/item';
        } else if (url.includes('aldailynews.com')) {
            parser.value = 'ParserDailyNews';
            suffix.value = '';
        } else if (url.includes('publicportal.alappeals.gov')) {
            parser.value = 'ParserAppealsAL';
            suffix.value = '';
        } else {
            parser.value = '';
            suffix.value = '';
        }
    }
    
    // Show/hide suffix based on parser
    if (parser.value === 'ParserAppealsAL') {
        suffixGroup.style.display = 'none';
    } else {
        suffixGroup.style.display = 'block';
    }
    
    updateCommand();
}

function updateCommand() {
    const commandType = document.getElementById('command-type').value;
    let command = '';
    let validation = [];
    
    if (commandType === 'basic') {
        command = buildBasicCommand(validation);
    } else {
        command = buildCourtCommand(validation);
    }
    
    document.getElementById('command-text').textContent = command || 'Configure options above to generate command...';
    
    // Show validation messages
    const validationDiv = document.getElementById('validation-messages');
    if (validation.length > 0) {
        validationDiv.innerHTML = '<div class="warning"><strong>⚠️ Issues:</strong><ul>' + 
            validation.map(msg => '<li>' + msg + '</li>').join('') + '</ul></div>';
    } else if (command) {
        validationDiv.innerHTML = '<div class="info"><strong>✅ Command looks good!</strong> Ready to copy and run.</div>';
    } else {
        validationDiv.innerHTML = '';
    }
    
    // Handle custom dates
    const datePeriod = document.getElementById('date-period');
    const customDates = document.getElementById('custom-dates');
    if (datePeriod && datePeriod.value === 'custom') {
        customDates.style.display = 'block';
    } else if (customDates) {
        customDates.style.display = 'none';
    }
}

function buildBasicCommand(validation) {
    let command = 'python -m opal';
    
    // URL (required)
    const urlSelect = document.getElementById('url').value;
    const customUrl = document.getElementById('custom-url').value;
    const url = urlSelect === 'custom' ? customUrl : urlSelect;
    
    if (!url) {
        validation.push('URL is required');
        return '';
    }
    command += ` --url ${url}`;
    
    // Parser (required)
    const parser = document.getElementById('parser').value;
    if (!parser) {
        validation.push('Parser is required');
        return '';
    }
    command += ` --parser ${parser}`;
    
    // Optional parameters
    const suffix = document.getElementById('suffix').value;
    if (suffix && parser !== 'ParserAppealsAL') {
        command += ` --suffix ${suffix}`;
    }
    
    const maxPages = document.getElementById('max-pages').value;
    if (maxPages) {
        command += ` --max_pages ${maxPages}`;
    }
    
    const output = document.getElementById('output').value;
    if (output) {
        command += ` --output ${output}`;
    }
    
    return command;
}

function buildCourtCommand(validation) {
    let command = 'python -m opal.configurable_court_extractor';
    
    // Court type (required)
    const courtType = document.getElementById('court-type').value;
    if (!courtType) {
        validation.push('Court type is required');
        return '';
    }
    command += ` --court ${courtType}`;
    
    // Date period
    const datePeriod = document.getElementById('date-period').value;
    if (datePeriod && datePeriod !== 'custom') {
        command += ` --date-period ${datePeriod}`;
    } else if (datePeriod === 'custom') {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        if (startDate && endDate) {
            command += ` --start-date ${startDate} --end-date ${endDate}`;
        } else {
            validation.push('Both start and end dates required for custom range');
        }
    }
    
    // Optional filters
    const caseCategory = document.getElementById('case-category').value;
    if (caseCategory) {
        command += ` --case-category "${caseCategory}"`;
    }
    
    const caseNumber = document.getElementById('case-number').value;
    if (caseNumber) {
        command += ` --case-number "${caseNumber}"`;
    }
    
    const caseTitle = document.getElementById('case-title').value;
    if (caseTitle) {
        command += ` --case-title "${caseTitle}"`;
    }
    
    const excludeClosed = document.getElementById('exclude-closed').checked;
    if (excludeClosed) {
        command += ` --exclude-closed`;
    }
    
    const maxPages = document.getElementById('court-max-pages').value;
    if (maxPages) {
        command += ` --max-pages ${maxPages}`;
    }
    
    const outputPrefix = document.getElementById('output-prefix').value;
    if (outputPrefix) {
        command += ` --output-prefix ${outputPrefix}`;
    }
    
    return command;
}

function copyCommand() {
    const commandText = document.getElementById('command-text').textContent;
    if (commandText && commandText !== 'Select options above to generate your command...' && commandText !== 'Configure options above to generate command...') {
        navigator.clipboard.writeText(commandText).then(() => {
            const btn = document.querySelector('.copy-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            btn.style.background = '#48bb78';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '#4299e1';
            }, 2000);
        });
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updateCommandType();
    updateCommand();
});
</script>