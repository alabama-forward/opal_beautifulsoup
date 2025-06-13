"""Tests for the URL catcher module"""
import pytest
from unittest.mock import patch, MagicMock
from opal.url_catcher_module import get_all_news_urls

@patch('opal.url_catcher_module.requests.get')
@patch('opal.url_catcher_module.BeautifulSoup')
def test_get_all_news_urls(mock_bs, mock_get):
    """Test URL extraction with mocked requests"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><a href='/article1'>Link 1</a><a href='/article2'>Link 2</a></body></html>"
    mock_get.return_value = mock_response
    
    # Setup mock BeautifulSoup
    mock_soup = MagicMock()
    mock_bs.return_value = mock_soup
    
    # Setup mock links
    mock_link1 = MagicMock()
    mock_link1.get.return_value = "/article1"
    mock_link2 = MagicMock()
    mock_link2.get.return_value = "/article2"
    mock_soup.find_all.return_value = [mock_link1, mock_link2]
    
    # Test the function
    urls = get_all_news_urls("https://example.com", "article", 1)
    
    # Verify results
    assert len(urls) == 2
    assert "https://example.com/article1" in urls
    assert "https://example.com/article2" in urls