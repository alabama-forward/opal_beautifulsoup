"""Tests for the parser module"""
import pytest
from opal.parser_module import Parser1819, ParserDailyNews

def test_parser_1819(sample_1819_html):
    """Test Parser1819 can extract article details"""
    parser = Parser1819()
    result = parser.parse_article(sample_1819_html, "https://example.com/article")
    
    # Test specific fields
    assert isinstance(result, dict)
    assert 'title' in result
    assert 'author' in result
    assert 'date' in result
    assert 'line_count' in result
    assert isinstance(result['line_content'], dict)

def test_parser_daily_news(sample_daily_html):
    """Test ParserDailyNews can extract article details"""
    parser = ParserDailyNews()
    result = parser.parse_article(sample_daily_html, "https://example.com/article")
    
    # Test specific fields
    assert isinstance(result, dict)
    assert 'title' in result
    assert 'author' in result
    assert 'date' in result
    assert 'line_count' in result
    assert isinstance(result['line_content'], dict)