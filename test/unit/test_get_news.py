import pytest
import sys
sys.path.insert(0, '/Users/keeganjustis/Documents/open-source/wa-state-environmental-policy-watch')
from src import get_news
from datetime import datetime,date


def test_get_today():
    assert get_news.get_today() == date.today()

def MOCK_TODAY():
    date_str = "2025-01-01"
    date_time = datetime.strptime(date_str, "%Y-%m-%d")
    return date_time.date()


def test_validate_date():
    TODAY = MOCK_TODAY()
    assert get_news.validate_date("2024-01-01",TODAY) == date(2024, 1, 1)
    assert get_news.validate_date("2023-04-02",TODAY) == date(2023, 4, 2)
    assert get_news.validate_date("2024-05-08",TODAY) == date(2024, 5, 8)
    assert get_news.validate_date("2024-09-10",TODAY) == date(2024, 9, 10)
    assert get_news.validate_date("2024-10-31",TODAY) == date(2024, 10, 31)
    assert get_news.validate_date("2024-11-30",TODAY) == date(2024, 11, 30)
    assert get_news.validate_date("2024-12-32",TODAY) == False
    assert get_news.validate_date("2024-12-00",TODAY) == False
    assert get_news.validate_date("2025-14-01",TODAY) == False
    assert get_news.validate_date("2025-02-30",TODAY) == False
    assert get_news.validate_date("2024-06-31",TODAY) == False
    assert get_news.validate_date("2024-17-01",TODAY) == False
    assert get_news.validate_date("2050-01-01",TODAY) == False
    assert get_news.validate_date("invalid-date",TODAY) == False
    
def test_date_restiction():
    TODAY = MOCK_TODAY()
    assert get_news.date_restiction("2024-01-01",TODAY) == False
    assert get_news.date_restiction("2023-04-02",TODAY) == False
    assert get_news.date_restiction("2024-05-08",TODAY) == "d[238]"
    assert get_news.date_restiction("2024-09-10",TODAY) == "d[113]"
    assert get_news.date_restiction("2024-10-31",TODAY) == "d[62]"
    assert get_news.date_restiction("2024-11-30",TODAY) == "d[32]"
    assert get_news.date_restiction("2026-11-30",TODAY) == False