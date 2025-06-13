"""Tests for the integrated parser"""
import json
import pytest
from unittest.mock import patch, MagicMock
from opal.integrated_parser import IntegratedParser
from opal.parser_module import Parser1819

@patch('opal.url_catcher_module.get_all_news_urls')
@patch('opal.parser_module.Parser1819.make_request')
def test_process_site(mock_make_request, mock_get_urls):
    """Test processing a site with mocked dependencies"""
    # Setup mocks
    mock_get_urls.return_value = ["https://example.com/article1", "https://example.com/article2"]
    mock_make_request.return_value = ["<html>content1</html>", "<html>content2</html>"], ["https://example.com/article1", "https://example.com/article2"]
    
    # Create a mock Parser1819 that returns predefined results
    with patch.object(Parser1819, 'parse_article') as mock_parse:
        mock_parse.side_effect = [
            {"title": "Article 1", "author": "Author 1", "date": "2023-01-01", "line_count": 5, "line_content": {}},
            {"title": "Article 2", "author": "Author 2", "date": "2023-01-02", "line_count": 7, "line_content": {}}
        ]
        
        # Test the integrated parser
        parser = IntegratedParser(Parser1819)
        result = parser.process_site("https://example.com", "/article", 10)
        
        # Parse result and verify
        result_dict = json.loads(result)
        assert result_dict["success"] is True
        assert result_dict["total_articles"] == 2
        assert len(result_dict["articles"]) == 2