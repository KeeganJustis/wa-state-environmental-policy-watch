import os
from datetime import datetime,date
import logging
import requests
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("google_api")
GOOGLE_CX = os.getenv("google_cx")

def get_news_sites(query,end_date):
    date_restict = date_restiction(end_date)
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}&dateRestrict={date_restict}&safe=active&lr=lang_en"
    response = requests.get(url)
    return response.json()


def validate_date(date_str):
    try:
        date_time = datetime.strptime(date_str, "%Y-%m-%d")
        date_time = date_time.date()
        today = date.today()
        if date_time > today:
            logging.error("End date cannot be in the future")
            return False
        else:
            print(date_time)
            print(type(date_time))
            return date_time
    except ValueError:
        return False

def date_restiction(start_date):
    try:
        start_date = validate_date(start_date)
        start_date
        today = date.today()
        delta = today - start_date
        return f"d[{delta.days}]"
    except ValueError as e:
        logging.error(e)
        exit(1)

