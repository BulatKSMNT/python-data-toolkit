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
        print("No argument")
        return

    ticker = sys.argv[1].upper()

    ticker_to_company = {v: k for k, v in COMPANIES.items()}
    #print(ticker_to_company)
    company = ticker_to_company.get(ticker)
    price = STOCKS.get(ticker)

    if company and price:
        print(f"{company} {price}")
    else:
        print("Unknown ticker")

if __name__ == "__main__":
    core()