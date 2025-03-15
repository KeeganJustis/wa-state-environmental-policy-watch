import os
from datetime import datetime,date
import logging
import requests
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

GOOGLE_API_KEY = os.getenv("google_api")
GOOGLE_CX = os.getenv("google_cx")

def get_news_sites(query,end_date):
    try:
        today = get_today()
        date_restict = date_restiction(end_date,today)
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}&dateRestrict={date_restict}&safe=active&lr=lang_en"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logging.error(e)
        exit(1)

def save_news_sites(news_sites):
    current_dir = Path("./")
    file_path = current_dir / "tmp"
    os.makedirs(file_path, exist_ok=True)
    with open("./tmp/news_sites.json", "w") as f:
        json.dump(news_sites, f)

def get_today():
    try:
        today = date.today()
        return today
    except Exception as e:
        logging.error(e)
        exit(1)


def validate_date(date_str,today):
    try:
        date_time = datetime.strptime(date_str, "%Y-%m-%d")
        date_time = date_time.date()
        if date_time > today:
            logging.error("End date cannot be in the future")
            return False
        else:
            return date_time
    except ValueError:
        return False

def date_restiction(start_date,today):
    try:
        start_date = validate_date(start_date,today)
        if start_date == False or start_date > today :
            return False
        else:
            delta = today - start_date
            if delta.days > 365:
                logging.error("Date range is too long")
                return False
            else:
                return f"d[{delta.days}]"
    except ValueError as e:
        logging.error(e)
        exit(1)

