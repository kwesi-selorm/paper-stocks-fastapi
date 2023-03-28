import requests
from bs4 import BeautifulSoup

url = "https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

stocks_table = soup.find_all(".nasdaq-screener_table")[0]
rows = stocks_table.find_all(".nasdaq-screener_row")

stocks = []
for row in rows:
    symbol_data = row.find("th")
    name_data = row.find(".nasdaq-screener__cell nasdaq-screener__cell--name")
    stock = {
        "symbol": symbol_data.text.strip(),
        "name": name_data.text.strip()
    }
    stocks.append(stock)

print(stocks[0])
