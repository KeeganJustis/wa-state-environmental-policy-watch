import pytest
import sys
sys.path.insert(0, '/Users/keeganjustis/Documents/open-source/wa-state-environmental-policy-watch')
from src import get_news
import datetime

def test_validate_date():
    assert get_news.validate_date("2024-01-01") == True
    assert get_news.validate_date("2023-04-02") == True
    assert get_news.validate_date("2024-05-08") == True
    assert get_news.validate_date("2024-09-10") == True
    assert get_news.validate_date("2024-10-31") == True
    assert get_news.validate_date("2024-11-30") == True
    assert get_news.validate_date("2024-12-32") == False
    assert get_news.validate_date("2024-12-00") == False
    assert get_news.validate_date("2025-14-01") == False
    assert get_news.validate_date("2025-02-30") == False
    assert get_news.validate_date("2024-06-31") == False
    assert get_news.validate_date("2024-17-01") == False
    assert get_news.validate_date("2050-01-01") == False
    assert get_news.validate_date("invalid-date") == False