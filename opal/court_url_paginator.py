"""
URL Pagination handler for Alabama Appeals Court Public Portal
"""
import re
from typing import List, Tuple, Optional
from urllib.parse import unquote


def parse_court_url(url: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse court URL to extract current page number and total pages
    
    Args:
        url: Court portal URL with encoded parameters
        
    Returns:
        Tuple of (current_page, total_pages) or (None, None) if not found
    """
    try:
        # Decode URL to make parsing easier
        decoded_url = unquote(url)
        
        # Extract page number using regex
        page_match = re.search(r'page~\(.*?number~(\d+)', decoded_url)
        current_page = int(page_match.group(1)) if page_match else None
        
        # Extract total pages
        total_match = re.search(r'totalPages~(\d+)', decoded_url)
        total_pages = int(total_match.group(1)) if total_match else None
        
        return current_page, total_pages
        
    except Exception as e:
        print(f"Error parsing URL: {str(e)}")
        return None, None


def build_court_url(base_url: str, page_number: int) -> str:
    """
    Build court URL with updated page number
    
    Args:
        base_url: Original URL with page 0
        page_number: Target page number
        
    Returns:
        Updated URL with new page number
    """
    try:
        # First, decode the URL to work with it
        decoded_url = unquote(base_url)
        
        # Replace the page number
        # Pattern: page~(size~25~number~X~totalElements~Y~totalPages~Z)
        new_url = re.sub(
            r'(page~\(.*?number~)\d+',
            f'\\g<1>{page_number}',
            decoded_url
        )
        
        # Re-encode special characters to match original format
        # The URL uses ~ instead of URL encoding for structure
        # and %2a2f for forward slashes in dates
        new_url = new_url.replace('/', '%2a2f')
        
        return new_url
        
    except Exception as e:
        print(f"Error building URL: {str(e)}")
        return base_url


def extract_total_pages_from_first_load(url: str, parser) -> int:
    """
    Load the first page to extract total pages from the actual response
    
    Args:
        url: Initial URL (page 0)
        parser: CourtCaseParser instance to make the request
        
    Returns:
        Total number of pages
    """
    try:
        # Load the first page
        html_content = parser.make_request(url)
        if not html_content:
            return 1
            
        # Try to extract total pages from the page content or URL updates
        # After JavaScript execution, the URL might be updated with totalPages
        if hasattr(parser, 'driver') and parser.driver:
            current_url = parser.driver.current_url
            _, total_pages = parse_court_url(current_url)
            if total_pages and total_pages > 0:
                return total_pages
                
        # Default to 1 if we can't determine
        return 1
        
    except Exception as e:
        print(f"Error extracting total pages: {str(e)}")
        return 1


def paginate_court_urls(base_url: str, parser=None) -> List[str]:
    """
    Generate list of URLs for all pages of court results
    
    Args:
        base_url: Initial court search URL (page 0)
        parser: Optional CourtCaseParser instance to determine total pages dynamically
        
    Returns:
        List of URLs for all pages
    """
    urls = []
    
    # Check if the URL already has pagination info
    current_page, total_pages = parse_court_url(base_url)
    
    # If we can't determine total pages from URL and have a parser, load first page
    if (total_pages is None or total_pages == 0) and parser:
        total_pages = extract_total_pages_from_first_load(base_url, parser)
    
    # If still no total pages, default to a reasonable number or return just base URL
    if total_pages is None or total_pages == 0:
        # Return just the base URL if we can't determine pagination
        return [base_url]
    
    # Generate URLs for all pages (0-indexed)
    for page_num in range(total_pages):
        page_url = build_court_url(base_url, page_num)
        urls.append(page_url)
        
    return urls


def is_court_url(url: str) -> bool:
    """
    Check if a URL is for the Alabama Appeals Court portal
    
    Args:
        url: URL to check
        
    Returns:
        True if this is a court portal URL
    """
    return "publicportal.alappeals.gov" in url and "/portal/search/case/results" in url