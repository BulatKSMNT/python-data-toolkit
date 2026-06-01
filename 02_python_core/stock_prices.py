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

    company = sys.argv[1].capitalize()
    ticker = COMPANIES.get(company)

    if ticker:
        price = STOCKS.get(ticker)
        print(price)
    else:
        print("Unknown company")


if __name__ == "__main__":
    core()