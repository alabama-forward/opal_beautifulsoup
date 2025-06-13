"""
Court Case Parser for Alabama Appeals Court Public Portal
"""
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .parser_module import NewsParser


class ParserAppealsAL(NewsParser):
    """Parser for Alabama Appeals Court Public Portal using Selenium for JavaScript rendering"""
    
    def __init__(self, headless: bool = True, rate_limit_seconds: int = 3):
        """
        Initialize the Court Case Parser
        
        Args:
            headless: Run browser in headless mode (no GUI)
            rate_limit_seconds: Seconds to wait between requests
        """
        super().__init__()
        self.headless = headless
        self.rate_limit_seconds = rate_limit_seconds
        self.driver = None
        
    def _setup_driver(self):
        """Set up Chrome driver with appropriate options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def _close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            
    def make_request(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Override make_request to use Selenium instead of requests
        
        Args:
            url: URL to load
            timeout: Maximum time to wait for page load
            
        Returns:
            Page source HTML or None if error
        """
        try:
            if not self.driver:
                self._setup_driver()
                
            self.driver.get(url)
            
            # Wait for table to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Additional wait for dynamic content to load
            time.sleep(2)
            
            # Rate limiting
            time.sleep(self.rate_limit_seconds)
            
            return self.driver.page_source
            
        except Exception as e:
            print(f"Error loading page {url}: {str(e)}")
            return None
            
    def parse_table_row(self, row) -> Optional[Dict]:
        """
        Parse a single table row to extract case information
        
        Args:
            row: BeautifulSoup row element
            
        Returns:
            Dictionary with case data or None if parsing fails
        """
        try:
            cells = row.find_all('td')
            if len(cells) < 6:
                return None
                
            # Extract court name (column 1)
            court = cells[0].get_text(strip=True)
            
            # Extract case number and link (column 2)
            case_number_elem = cells[1].find('a')
            if case_number_elem:
                case_number = {
                    "text": case_number_elem.get_text(strip=True),
                    "link": case_number_elem.get('href', '')
                }
            else:
                case_number = {
                    "text": cells[1].get_text(strip=True),
                    "link": ""
                }
                
            # Extract remaining fields
            case_title = cells[2].get_text(strip=True)
            classification = cells[3].get_text(strip=True)
            filed_date = cells[4].get_text(strip=True)
            status = cells[5].get_text(strip=True)
            
            return {
                "court": court,
                "case_number": case_number,
                "case_title": case_title,
                "classification": classification,
                "filed_date": filed_date,
                "status": status
            }
            
        except Exception as e:
            print(f"Error parsing table row: {str(e)}")
            return None
            
    def parse_article(self, url: str) -> Dict:
        """
        Override parse_article to parse court case table data
        This method will be called for each page of results
        
        Args:
            url: URL of the page to parse
            
        Returns:
            Dictionary with parsed cases from this page
        """
        try:
            html_content = self.make_request(url)
            if not html_content:
                return {"error": "Failed to load page", "cases": []}
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the table
            table = soup.find('table')
            if not table:
                return {"error": "No table found", "cases": []}
                
            # Find all data rows (skip header)
            rows = table.find_all('tr')[1:]  # Skip header row
            
            cases = []
            for row in rows:
                case_data = self.parse_table_row(row)
                if case_data:
                    cases.append(case_data)
                    
            return {"cases": cases}
            
        except Exception as e:
            return {"error": str(e), "cases": []}
            
    def parse_all_cases(self, base_url: str, page_urls: List[str]) -> Dict:
        """
        Parse all court cases from multiple pages
        
        Args:
            base_url: Base URL of the court portal
            page_urls: List of URLs for each page of results
            
        Returns:
            Combined results from all pages
        """
        try:
            all_cases = []
            total_pages = len(page_urls)
            
            for i, url in enumerate(page_urls):
                print(f"Processing page {i + 1} of {total_pages}...")
                result = self.parse_article(url)
                
                if "cases" in result:
                    all_cases.extend(result["cases"])
                    
            return {
                "status": "success",
                "total_cases": len(all_cases),
                "extraction_date": datetime.now().strftime("%Y-%m-%d"),
                "cases": all_cases
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "total_cases": 0,
                "cases": []
            }
        finally:
            self._close_driver()