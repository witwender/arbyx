import requests, json, time

# Exchange to check e.g. binance, hitbtc, kucoin
exchange = "binance"
# Arbitrage gap size. 01 = 1%.
margin = 1.01
# BTC volume minimum for trading pair
volume = 0.1
url = "https://api.coingecko.com/api/v3/exchanges/" + exchange + "/tickers"
u = requests.get(url) # call first page and 100 coins
total = int(u.headers['Total']) # total headers
page = int(u.headers['Per-Page']) # tickers per page
scrolls = (total % page) - 1 # number of pages to scroll

p1 = u.json() # Save first page as dictionary
data = p1['tickers'] # Save ticker data

for i in range(scrolls): # for each of the page in total
    payload = {'page': i + 2} # calculate page number
    time.sleep(1) # sleep for a second
    p = requests.get(url, params=payload) # query each page
    pa = p.json()
    data.extend(pa['tickers'])

items = {} # Set empty dictionary

for ticker in data: # Loop through the tickers in data imported
    if ticker['converted_volume']['btc'] < volume: # Skip below this volume
        continue
    elif ticker['base'] not in items: # Check if base exists
        items[ticker['base']] = {ticker['target']: ticker['converted_last']['usd']} # Creates a new dict
    elif ticker['base'] in items: # Base exists
        items[ticker['base']][ticker['target']] = ticker['converted_last']['usd'] # Create & add dict to list

for item in items: # Loop through each base currency
    for key, value in items[item].items():
        for k, v in items[item].items():
            m = value / v
            if m > margin: # Check for price differences and print
                print(item + ' - ' + k + '/' + key + ' - ' + '{:.4f}'.format(m))
