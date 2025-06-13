"""OPAL - Opposing Positions and Lingo Parser"""

from opal.parser_module import BaseParser, Parser1819, ParserDailyNews
from opal.integrated_parser import IntegratedNewsParser
from opal.url_catcher_module import get_all_news_urls
from opal.court_case_parser import ParserAppealsAL
from opal.court_url_paginator import paginate_court_urls, is_court_url

__version__ = "0.1.0"