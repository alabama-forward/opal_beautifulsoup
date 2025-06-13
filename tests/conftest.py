"""Shared pytest fixtures and configuration"""
import pytest
import os

# Path to fixture directory
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def sample_1819_html():
    """Load sample 1819 News HTML"""
    with open(os.path.join(FIXTURES_DIR, 'sample_1819_article.html'), 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture
def sample_daily_html():
    """Load sample Daily News HTML"""
    with open(os.path.join(FIXTURES_DIR, 'sample_daily_article.html'), 'r', encoding='utf-8') as f:
        return f.read()