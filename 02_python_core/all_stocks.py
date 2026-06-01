import sys


def core():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }

    if len(sys.argv) != 2:
        return

    query_string = sys.argv[1].strip()
    if not query_string or ',,' in query_string:
        return

    queries = [q.strip() for q in query_string.split(',')]
    if any(not q for q in queries):
        return

    for query in queries:
        query_lower = query.lower()
        found = False

        for company, ticker in COMPANIES.items():
            if query_lower == company.lower():
                print(f"{company} stock price is {STOCKS[ticker]}")
                found = True
                break
            if query_lower == ticker.lower():
                print(f"{ticker} is a ticker symbol for {company}")
                found = True
                break

        if not found:
            print(f"{query} is an unknown company or an unknown ticker symbol")


if __name__ == '__main__':
    core()