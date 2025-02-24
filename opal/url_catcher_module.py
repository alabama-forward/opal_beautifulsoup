"""
Module to create an array of urls using a base URL and additional suffix
"""
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def get_all_news_urls(base_url: str, suffix: str, max_pages: int = None):
    """Gets urls from a website.
    
    Args:
        base_url (string): the base url you want to use for search
        suffix (string): Any url suffix elements you want to join to the base url
        max_pages (integer): The maximum number of pages you want to pull
        
    Returns:
        list: An array of urls that meet the criteria
    """
    news_urls = []
    page = 1

    # Add a strict counter to enforce max_pages
    pages_processed = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    while True:
        try:
            # Increment pages processed counter
            pages_processed += 1

            # Check max_pages before making request
            if max_pages is not None and pages_processed > max_pages:
                print(f"Reached maximum pages limit: {max_pages}")
                break

            # Construct current URL
            current_url = base_url if page == 1 else f"{base_url}/page/{page}"

            # Make request
            response = requests.get(current_url, headers=headers, timeout=5)
            if response.status_code != 200:
                print(f"Reached end at page {page-1}")
                break

            # Parse page
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            found_on_page = 0

            # Process links
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(current_url, href)
                    if ((suffix is None) or (suffix in full_url)) \
                            and full_url.startswith(base_url) and full_url not in news_urls:
                        news_urls.append(str(full_url))
                        found_on_page += 1

            print(f"Page {page}: Found {found_on_page} new URLs")

            # Check exit conditions
            if max_pages is not None and page >= max_pages:
                print(f"Reached maximum pages limit: {max_pages}")
                break
            if found_on_page == 0:
                print("No new URLs found on this page")
                break

            page += 1
            time.sleep(1)

        except requests.RequestException as e:
            print(f"Error making request: {e}")
            break

    return news_urls
