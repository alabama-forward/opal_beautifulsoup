---
layout: default
title: "Error Handling"
---

# Error Handling

OPAL includes comprehensive error handling mechanisms to ensure robust data extraction. This document covers error types, handling strategies, and troubleshooting guidance **for developers**.

**For users experiencing errors**: See [Understanding Errors](../user-guide/understanding-errors.md) for user-friendly explanations and solutions.

## Error Categories

### 1. Selenium WebDriver Errors

#### TimeoutException
Occurs when elements don't load within expected timeframes.

**Common Causes:**
- Slow network connection
- Page taking longer than usual to load
- Element selectors changed on the website

**Handling Strategy:**
```python
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "target-element"))
    )
except TimeoutException:
    logger.warning("Element not found within timeout, retrying...")
    # Implement retry logic or fallback
```

#### StaleElementReferenceException
Occurs when trying to interact with elements that are no longer attached to the DOM.

**Handling Strategy:**
```python
from selenium.common.exceptions import StaleElementReferenceException

def safe_element_interaction(driver, locator, action):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            element = driver.find_element(*locator)
            return action(element)
        except StaleElementReferenceException:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # Wait before retry
```

#### WebDriverException
General driver-related errors including crashes.

**Handling Strategy:**
```python
from selenium.common.exceptions import WebDriverException

def restart_driver_on_failure(parser_instance):
    try:
        # Perform driver operation
        return parser_instance.extract_data()
    except WebDriverException as e:
        logger.error(f"Driver failed: {e}")
        parser_instance._restart_driver()
        return parser_instance.extract_data()  # Retry once
```

### 2. Network Errors

#### Connection Timeouts
Network connectivity issues or server unresponsiveness.

**Handling Strategy:**
- Implement exponential backoff
- Retry with longer timeouts
- Check network connectivity

```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except (requests.ConnectionError, requests.Timeout) as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Network error, retrying in {wait_time:.2f}s")
            time.sleep(wait_time)
```

#### HTTP Status Errors
Server returning error status codes (404, 500, etc.)

```python
def handle_http_errors(response):
    if response.status_code == 404:
        logger.error("Page not found - URL may have changed")
        return None
    elif response.status_code >= 500:
        logger.error("Server error - may be temporary")
        raise ServerError("Server returned error status")
    elif response.status_code != 200:
        logger.warning(f"Unexpected status code: {response.status_code}")
```

### 3. Parsing Errors

#### ElementNotFound
Target HTML elements are missing or have changed.

**Handling Strategy:**
```python
def safe_find_element(driver, primary_selector, fallback_selectors=None):
    """Try multiple selectors for robustness"""
    selectors = [primary_selector] + (fallback_selectors or [])
    
    for selector in selectors:
        try:
            return driver.find_element(*selector)
        except NoSuchElementException:
            continue
    
    logger.error("No matching elements found with any selector")
    return None
```

#### DataValidation
Extracted data doesn't match expected format.

```python
def validate_case_data(case_data):
    """Validate extracted court case data"""
    required_fields = ['case_number', 'case_title', 'court', 'status']
    
    for field in required_fields:
        if field not in case_data or not case_data[field]:
            logger.warning(f"Missing required field: {field}")
            return False
    
    # Validate date format
    if case_data.get('filed_date'):
        try:
            datetime.strptime(case_data['filed_date'], '%m/%d/%Y')
        except ValueError:
            logger.warning(f"Invalid date format: {case_data['filed_date']}")
            case_data['filed_date'] = None
    
    return True
```

### 4. Session Management Errors

#### Session Expiration
Court system URLs contain session tokens that expire.

**Detection:**
```python
def is_session_expired(driver):
    """Check if current session has expired"""
    try:
        # Look for session expired indicators
        expired_indicators = [
            "Session has expired",
            "Please log in again",
            "Invalid session"
        ]
        
        page_text = driver.page_source.lower()
        return any(indicator.lower() in page_text for indicator in expired_indicators)
    except:
        return False
```

**Handling:**
```python
def handle_session_expiration(custom_url):
    """Provide guidance for expired sessions"""
    logger.error("Session appears to have expired")
    logger.info("Custom URLs are session-based and expire after ~30 minutes")
    logger.info("Please create a new search and provide the fresh URL")
    
    # Suggest alternative
    logger.info("Or use the configurable extractor to build a new search:")
    logger.info("python -m opal.configurable_court_extractor --court civil --date-period 7d")
```

### 5. Configuration Errors

#### Invalid Parameters
User-provided parameters don't match expected values.

```python
def validate_court_type(court_type):
    """Validate court type parameter"""
    valid_courts = ['civil', 'criminal', 'supreme']
    if court_type not in valid_courts:
        raise ValueError(f"Invalid court type: {court_type}. Must be one of {valid_courts}")

def validate_date_period(date_period):
    """Validate date period parameter"""
    valid_periods = ['7d', '1m', '3m', '6m', '1y', 'custom']
    if date_period not in valid_periods:
        raise ValueError(f"Invalid date period: {date_period}. Must be one of {valid_periods}")
```

## Error Recovery Strategies

### 1. Graceful Degradation

When non-critical operations fail, continue with reduced functionality:

```python
def extract_with_fallbacks(driver):
    """Extract data with fallback strategies"""
    results = []
    
    try:
        # Primary extraction method
        results = extract_full_data(driver)
    except Exception as e:
        logger.warning(f"Primary extraction failed: {e}")
        
        try:
            # Fallback to basic extraction
            results = extract_basic_data(driver)
            logger.info("Using fallback extraction method")
        except Exception as e2:
            logger.error(f"Fallback extraction also failed: {e2}")
            # Return partial results if any
            results = extract_minimal_data(driver)
    
    return results
```

### 2. Partial Success Handling

Continue processing even when some operations fail:

```python
def process_all_pages(page_urls):
    """Process all pages, continuing on individual failures"""
    successful_pages = 0
    failed_pages = 0
    all_results = []
    
    for i, url in enumerate(page_urls):
        try:
            logger.info(f"Processing page {i+1}/{len(page_urls)}")
            page_results = extract_page_data(url)
            all_results.extend(page_results)
            successful_pages += 1
        except Exception as e:
            logger.error(f"Failed to process page {i+1}: {e}")
            failed_pages += 1
            continue  # Continue with next page
    
    logger.info(f"Completed: {successful_pages} successful, {failed_pages} failed")
    return all_results
```

### 3. State Recovery

Save progress to recover from failures:

```python
import json
import os

class StatefulExtractor:
    def __init__(self, state_file="extraction_state.json"):
        self.state_file = state_file
        self.state = self.load_state()
    
    def load_state(self):
        """Load previous state if exists"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"completed_pages": [], "results": []}
    
    def save_state(self):
        """Save current state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def extract_with_recovery(self, page_urls):
        """Extract data with state recovery"""
        for url in page_urls:
            if url in self.state["completed_pages"]:
                logger.info(f"Skipping already processed page: {url}")
                continue
            
            try:
                results = extract_page_data(url)
                self.state["results"].extend(results)
                self.state["completed_pages"].append(url)
                self.save_state()  # Save after each page
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                continue
        
        # Clean up state file on completion
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        
        return self.state["results"]
```

## Logging and Monitoring

### Structured Logging

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        
    def log_extraction_start(self, court_type, parameters):
        """Log extraction start with context"""
        self.logger.info("Extraction started", extra={
            "event": "extraction_start",
            "court_type": court_type,
            "parameters": parameters,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_error(self, error_type, error_message, context=None):
        """Log errors with structured data"""
        self.logger.error("Error occurred", extra={
            "event": "error",
            "error_type": error_type,
            "error_message": str(error_message),
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        })
```

### Error Metrics

Track error rates and types:

```python
from collections import defaultdict
import time

class ErrorMetrics:
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.start_time = time.time()
        
    def record_error(self, error_type):
        """Record an error occurrence"""
        self.error_counts[error_type] += 1
    
    def get_error_summary(self):
        """Get summary of all errors"""
        total_errors = sum(self.error_counts.values())
        runtime = time.time() - self.start_time
        
        return {
            "total_errors": total_errors,
            "error_rate": total_errors / (runtime / 60),  # errors per minute
            "error_breakdown": dict(self.error_counts),
            "runtime_minutes": runtime / 60
        }
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. "Element not found" errors

**Symptoms:** NoSuchElementException, TimeoutException
**Causes:** Website changes, slow loading, wrong selectors
**Solutions:**
- Check if website structure changed
- Increase timeout values
- Use more robust selectors
- Add wait conditions

#### 2. Empty results returned

**Symptoms:** No data extracted, empty result sets
**Causes:** Page not loading, changed selectors, session issues
**Solutions:**
- Run in non-headless mode to see browser
- Check page source for expected elements
- Verify URL is correct and accessible
- Check for session expiration

#### 3. Driver crashes or hangs

**Symptoms:** WebDriverException, processes not terminating
**Causes:** Memory issues, driver version problems, resource limits
**Solutions:**
- Update ChromeDriver
- Increase system resources
- Add proper cleanup in finally blocks
- Use context managers for driver lifecycle

#### 4. Slow extraction performance

**Symptoms:** Very slow processing, timeouts
**Causes:** Network issues, server rate limiting, inefficient code
**Solutions:**
- Adjust rate limiting parameters
- Optimize element selection
- Use headless mode
- Check network connectivity

### Debug Mode Usage

Enable comprehensive debugging:

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run extraction with debugging
from opal.configurable_court_extractor import extract_court_cases_with_params

results = extract_court_cases_with_params(
    court='civil',
    date_period='7d',
    max_pages=3
    # The function internally uses ParserAppealsAL with headless=True by default
    # To debug, modify the function to set headless=False
)

# Add breakpoints for inspection
import pdb; pdb.set_trace()
```

### Health Checks

Implement health checks for long-running extractions:

```python
def health_check(driver):
    """Check if extraction environment is healthy"""
    checks = {
        "driver_responsive": False,
        "page_loaded": False,
        "elements_present": False
    }
    
    try:
        # Check driver responsiveness
        driver.current_url
        checks["driver_responsive"] = True
        
        # Check page loaded
        driver.execute_script("return document.readyState") == "complete"
        checks["page_loaded"] = True
        
        # Check for expected elements
        driver.find_element(By.TAG_NAME, "body")
        checks["elements_present"] = True
        
    except Exception as e:
        logger.warning(f"Health check failed: {e}")
    
    return all(checks.values()), checks
```

## Best Practices

1. **Always use timeouts** - Never wait indefinitely
2. **Implement retry logic** - Network issues are common
3. **Log comprehensively** - Errors and successful operations
4. **Validate data** - Check extracted data makes sense
5. **Handle partial failures** - Don't let one failure stop everything
6. **Clean up resources** - Always close drivers and files
7. **Provide user feedback** - Show progress and error context
8. **Plan for recovery** - Save state for long operations

## Error Response Formats

Standardized error responses for consistency:

```python
def create_error_response(error_type, message, context=None):
    """Create standardized error response"""
    return {
        "status": "error",
        "error_type": error_type,
        "error_message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "context": context or {}
    }

# Usage examples
timeout_error = create_error_response(
    "TimeoutError",
    "Page failed to load within 30 seconds",
    {"url": "https://example.com", "timeout": 30}
)

session_error = create_error_response(
    "SessionExpired",
    "Court session has expired",
    {"suggestion": "Create a new search"}
)
```