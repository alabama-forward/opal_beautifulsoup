# Interactive Components Showcase

This page demonstrates all the interactive components available in the OPAL documentation.

## Quick Start Hero

<div class="quick-start-hero">
  <h2>Start Scraping Alabama Court Data in Minutes</h2>
  <p>OPAL makes it easy to extract structured data from Alabama court websites</p>
  <a href="/getting-started/quick-start/" class="md-button">Get Started →</a>
</div>

## Feature Cards

<div class="feature-grid">
  <div class="feature-card">
    <h4>Alabama Appeals Court</h4>
    <p>Extract appellate court decisions with structured metadata</p>
    <code>opal parse appeals-al</code>
  </div>
  <div class="feature-card">
    <h4>1819 News Parser</h4>
    <p>Scrape articles from Alabama's independent news source</p>
    <code>opal parse parser-1819</code>
  </div>
  <div class="feature-card">
    <h4>Daily News Parser</h4>
    <p>Extract content from daily news publications</p>
    <code>opal parse daily-news</code>
  </div>
</div>

## Interactive Command Builder

<div class="command-builder">
  <h3>Build Your Command</h3>
  
  <div class="command-option">
    <label for="parser-select">Select Parser:</label>
    <select id="parser-select">
      <option value="appeals-al">Alabama Appeals Court</option>
      <option value="parser-1819">1819 News</option>
      <option value="daily-news">Daily News</option>
    </select>
  </div>
  
  <div class="command-option">
    <label for="date-input">Date (optional):</label>
    <input type="date" id="date-input" />
  </div>
  
  <div class="command-option">
    <label for="output-format">Output Format:</label>
    <select id="output-format">
      <option value="json">JSON</option>
      <option value="csv">CSV</option>
      <option value="xml">XML</option>
    </select>
  </div>
  
  <div class="command-output">
    <span id="generated-command">opal parse appeals-al --output json</span>
    <button class="copy-button" onclick="copyCommand()">Copy</button>
  </div>
</div>

## Progress Tracker

<div class="progress-tracker">
  <div class="progress-step completed">
    <span>1</span>
    <span class="progress-step-label">Install</span>
  </div>
  <div class="progress-step completed">
    <span>2</span>
    <span class="progress-step-label">Configure</span>
  </div>
  <div class="progress-step active">
    <span>3</span>
    <span class="progress-step-label">First Scrape</span>
  </div>
  <div class="progress-step">
    <span>4</span>
    <span class="progress-step-label">Process Data</span>
  </div>
  <div class="progress-step">
    <span>5</span>
    <span class="progress-step-label">Automate</span>
  </div>
</div>

## Interactive Tabs

<div class="tab-container">
  <div class="tab-buttons">
    <button class="tab-button active" onclick="showTab('installation')">Installation</button>
    <button class="tab-button" onclick="showTab('configuration')">Configuration</button>
    <button class="tab-button" onclick="showTab('usage')">Usage</button>
    <button class="tab-button" onclick="showTab('examples')">Examples</button>
  </div>
  
  <div class="tab-content">
    <div id="installation" class="tab-panel active">
      <h3>Installation Guide</h3>
      <p>Install OPAL using pip:</p>
      <pre><code>pip install opal-scraper</code></pre>
    </div>
    
    <div id="configuration" class="tab-panel">
      <h3>Configuration Options</h3>
      <p>Configure OPAL with environment variables or config files.</p>
    </div>
    
    <div id="usage" class="tab-panel">
      <h3>Basic Usage</h3>
      <p>Run OPAL from the command line with various options.</p>
    </div>
    
    <div id="examples" class="tab-panel">
      <h3>Code Examples</h3>
      <p>See real-world examples of OPAL in action.</p>
    </div>
  </div>
</div>

## Code Example with Header

<div class="code-example">
  <div class="code-example-header">
    <span class="filename">scrape_appeals.py</span>
    <button class="copy-button">Copy</button>
  </div>
  <div class="code-example-content">
    <pre><code class="language-python">from opal import AppealsALParser

# Initialize the parser
parser = AppealsALParser()

# Scrape recent decisions
decisions = parser.scrape(date="2024-01-15")

# Process results
for decision in decisions:
    print(f"Case: {decision.case_number}")
    print(f"Title: {decision.title}")
    print(f"Date: {decision.date}")
</code></pre>
  </div>
</div>

## Parser Comparison Table

<div class="parser-comparison">
  <table>
    <thead>
      <tr>
        <th>Feature</th>
        <th>Appeals AL</th>
        <th>1819 News</th>
        <th>Daily News</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Date Filtering</td>
        <td class="check">✓</td>
        <td class="check">✓</td>
        <td class="cross">✗</td>
      </tr>
      <tr>
        <td>Pagination Support</td>
        <td class="check">✓</td>
        <td class="check">✓</td>
        <td class="check">✓</td>
      </tr>
      <tr>
        <td>Metadata Extraction</td>
        <td class="check">✓</td>
        <td class="cross">✗</td>
        <td class="check">✓</td>
      </tr>
      <tr>
        <td>PDF Download</td>
        <td class="check">✓</td>
        <td class="cross">✗</td>
        <td class="cross">✗</td>
      </tr>
    </tbody>
  </table>
</div>

## Statistics Grid

<div class="stats-grid">
  <div class="stat-card">
    <p class="stat-number">3</p>
    <p class="stat-label">Available Parsers</p>
  </div>
  <div class="stat-card">
    <p class="stat-number">10k+</p>
    <p class="stat-label">Documents Scraped</p>
  </div>
  <div class="stat-card">
    <p class="stat-number">5min</p>
    <p class="stat-label">Setup Time</p>
  </div>
  <div class="stat-card">
    <p class="stat-number">100%</p>
    <p class="stat-label">Open Source</p>
  </div>
</div>

## Interactive Terminal

<div class="terminal-window">
  <div class="terminal-header">
    <div class="terminal-dot red"></div>
    <div class="terminal-dot yellow"></div>
    <div class="terminal-dot green"></div>
  </div>
  <div class="terminal-body">
    <div>
      <span class="terminal-prompt">$</span>
      <span class="terminal-command">opal parse appeals-al --date 2024-01-15</span>
    </div>
    <div class="terminal-output">
      Initializing Alabama Appeals Court parser...<br>
      Fetching cases from 2024-01-15...<br>
      Found 12 cases<br>
      Processing: [████████████████████] 100%<br>
      Successfully scraped 12 cases to appeals_al_2024-01-15.json
    </div>
  </div>
</div>

## Flowchart Example

<div class="flowchart-container">
  <div class="mermaid">
    graph LR
      A[Start] --> B[Select Parser]
      B --> C{Date Filter?}
      C -->|Yes| D[Set Date Range]
      C -->|No| E[Use Default]
      D --> F[Run Scraper]
      E --> F
      F --> G[Process Data]
      G --> H[Export Results]
      H --> I[End]
  </div>
</div>

<script>
// Command Builder Logic
document.getElementById('parser-select').addEventListener('change', updateCommand);
document.getElementById('date-input').addEventListener('change', updateCommand);
document.getElementById('output-format').addEventListener('change', updateCommand);

function updateCommand() {
  const parser = document.getElementById('parser-select').value;
  const date = document.getElementById('date-input').value;
  const format = document.getElementById('output-format').value;
  
  let command = `opal parse ${parser}`;
  if (date) command += ` --date ${date}`;
  command += ` --output ${format}`;
  
  document.getElementById('generated-command').textContent = command;
}

function copyCommand() {
  const command = document.getElementById('generated-command').textContent;
  navigator.clipboard.writeText(command);
  
  const button = event.target;
  button.textContent = 'Copied!';
  button.classList.add('copied');
  
  setTimeout(() => {
    button.textContent = 'Copy';
    button.classList.remove('copied');
  }, 2000);
}

// Tab Logic
function showTab(tabName) {
  // Hide all panels
  document.querySelectorAll('.tab-panel').forEach(panel => {
    panel.classList.remove('active');
  });
  
  // Remove active from all buttons
  document.querySelectorAll('.tab-button').forEach(button => {
    button.classList.remove('active');
  });
  
  // Show selected panel
  document.getElementById(tabName).classList.add('active');
  
  // Mark button as active
  event.target.classList.add('active');
}

// Copy button for code examples
document.querySelectorAll('.code-example .copy-button').forEach(button => {
  button.addEventListener('click', function() {
    const codeBlock = this.closest('.code-example').querySelector('code');
    navigator.clipboard.writeText(codeBlock.textContent);
    
    this.textContent = 'Copied!';
    this.classList.add('copied');
    
    setTimeout(() => {
      this.textContent = 'Copy';
      this.classList.remove('copied');
    }, 2000);
  });
});
</script>