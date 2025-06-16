---
layout: default
title: "User-Agent Headers Guide"
---

# User-Agent Headers Guide

## What is a User-Agent?

**User-Agent headers** are strings that identify the client (browser, bot, or application) making an HTTP request to a web server.

It's an HTTP header that tells the server:
- What software is making the request
- What version it is
- What operating system it's running on

## Examples of User-Agent Strings

### Chrome Browser
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

### Python Requests (default)
```
python-requests/2.28.0
```

### Googlebot
```
Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
```

### Firefox Browser
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
```

### Safari Browser
```
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15
```

## Why User-Agents Matter

1. **Server Behavior**: Websites may serve different content based on User-Agent
2. **Access Control**: Some sites block requests with suspicious or missing User-Agents
3. **Analytics**: Helps websites understand their traffic
4. **Bot Detection**: Sites use it to identify and potentially block scrapers
5. **Content Optimization**: Sites may serve mobile vs desktop versions

## Setting User-Agent in Python

### Basic Example
```python
import requests

# Without User-Agent (might be blocked)
response = requests.get('https://example.com')

# With User-Agent (appears as a browser)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://example.com', headers=headers)
```

### Advanced Example with Multiple Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get('https://example.com', headers=headers)
```

## Common User-Agent Patterns

### Desktop Browsers
```python
# Windows Chrome
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# macOS Safari
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'

# Linux Firefox
'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
```

### Mobile Browsers
```python
# iPhone Safari
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'

# Android Chrome
'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
```

### Custom Bot (Honest Approach)
```python
'OPAL-Bot/1.0 (+https://github.com/yourusername/opal)'
'MyCompany-Scraper/2.1 (contact@mycompany.com)'
```

## Implementing User-Agents in OPAL

### Enhanced BaseParser
```python
def make_request(self, urls: List[str]) -> Tuple[List[str], List[str]]:
    """Shared request functionality for all parsers with proper headers"""
    
    # Realistic browser headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    responses = []
    successful_urls = []

    for url in urls:
        try:
            print(f"Requesting: {url}")
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            responses.append(response.text)
            successful_urls.append(url)
        except requests.exceptions.RequestException:
            print(f"Skipping URL due to error: {url}")
            continue

    return responses, successful_urls
```

### User-Agent Rotation
```python
import random

class RotatingUserAgentParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
    
    def get_random_user_agent(self):
        return random.choice(self.user_agents)
    
    def make_request(self, urls):
        # Use different User-Agent for each request
        headers = {'User-Agent': self.get_random_user_agent()}
        # ... rest of request logic
```

## Best Practices

### 1. Be Strategic
- **Use real User-Agents**: Copy from actual browsers
- **Stay current**: Browser versions change frequently
- **Match behavior**: If you claim to be Chrome, act like Chrome

### 2. Be Respectful
- **Respect robots.txt**: Even with a browser User-Agent
- **Rate limit**: Don't overwhelm servers
- **Be honest when possible**: Some sites appreciate transparent bots

### 3. Be Consistent
- **Use complete headers**: Include Accept, Accept-Language, etc.
- **Maintain session**: Use the same User-Agent throughout a session
- **Handle responses**: Check if the site is behaving differently

### 4. Be Prepared
- **Rotate User-Agents**: Avoid detection patterns
- **Handle blocks**: Have fallback strategies
- **Monitor changes**: Sites may update their detection methods

## User-Agent Detection Techniques

Websites can detect fake User-Agents by:

1. **Header Analysis**: Checking if browser behavior matches the User-Agent
2. **Missing Headers**: Looking for headers real browsers always send
3. **JavaScript Testing**: Testing browser capabilities that match the claimed version
4. **Request Patterns**: Analyzing timing and request sequences
5. **Feature Detection**: Checking for browser-specific features

## Common Mistakes

### 1. Outdated User-Agents
```python
# Bad - very old browser version
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 Chrome/45.0.2454.85'

# Good - recent browser version
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124'
```

### 2. Inconsistent Headers
```python
# Bad - claims to be Chrome but uses Firefox Accept header
headers = {
    'User-Agent': 'Chrome/91.0.4472.124',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'  # Firefox style
}
```

### 3. Missing Common Headers
```python
# Bad - only User-Agent
headers = {'User-Agent': 'Mozilla/5.0...'}

# Good - realistic browser headers
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Accept': 'text/html,application/xhtml+xml...',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}
```

## Testing User-Agents

### Check What You're Sending
```python
import requests

# Test your headers
response = requests.get('https://httpbin.org/headers', headers=your_headers)
print(response.json())
```

### Verify Server Response
```python
# Check if the site is treating you differently
response_bot = requests.get(url)  # Default requests User-Agent
response_browser = requests.get(url, headers=browser_headers)

if response_bot.content != response_browser.content:
    print("Site serves different content based on User-Agent")
```

## Tools and Resources

- **Browser DevTools**: Copy real User-Agent strings from Network tab
- **User-Agent Databases**: Sites like whatismybrowser.com
- **Header Checkers**: Use httpbin.org to test your headers
- **Browser Testing**: Use Selenium to see what real browsers send

## Conclusion

User-Agent headers are a crucial part of web scraping that can mean the difference between successful data extraction and being blocked. Use them thoughtfully and responsibly to build robust scrapers that respect both the technical and ethical aspects of web crawling.