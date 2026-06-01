import pstats
import os
import sys
import time
import re
from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import cProfile


def request_processing(ticker, table_field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials/"
    try:
        headers = { 'User-Agent' : 'Mozilla/5.0 '}
        response = requests.get(url, headers=headers)
        response.raise_for_status() #

    except requests.exceptions.RequestException as e:
        raise HTTPError(f"Failed to fetch data: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    #time.sleep(5)
    rows = soup.find_all('div', class_='row lv-0 yf-t22klz')

    for row in rows:
        good = (re.sub(r'<[^>]+>', '', row.text).strip())
        if good.startswith(table_field):
            return tuple([table_field] + good[len(table_field):].split())

    raise ValueError(f"Field '{table_field}' not found in financial data")

def main():
    if len(sys.argv) != 3:
        print("Invalid command: python financial.py <ticker> <table_field>")
        sys.exit(1)
    ticker = sys.argv[1]
    table_field = sys.argv[2]

    try:
        res = request_processing(ticker,table_field)
        print(res)
    except HTTPError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.dump_stats("profiling-sleep.prof")
    stats.sort_stats('tottime')
    with open("profiling-tottime.txt", "w", encoding="utf-8") as file:
        stats.stream = file
        stats.print_stats()
        os.remove("profiling-sleep.prof")
