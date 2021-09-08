import requests
import json
import binance_websocket
import track_stock 

# Convert Dollar to INR 
def dlr_inr():
    response = requests.get('https://live-rates.com/rates')
    response = response.json()
    print(response)

# Print Json Object
def print_data(obj):
    text = json.dumps(obj, indent=4)
    print(text)

# Check a the variable key passed in the function is present in that dictionary
def checkKey(dict, key): 
    if key in dict.keys():
        return 1
    else:
        return 0

def formatted_print(wazir, b_price, w_price, diff, percentage, direction):
    if direction == 0:
        print(
            'Coin Name: ', wazir[0],
            '\nArbitrage: ', 'WazirX ----> Binance',
            '\nBinance USD Price: ', b_price,
            '\nWazirX USD Price: ', w_price,
            '\nVolume: ', wazir[4],
            '\nDiff/Coin: ', diff,
            '\nPercentage: ', percentage
        )
    else:
        print(
            'Coin Name: ', wazir[0],
            '\nArbitrage: ', 'Binance ----> WazirX',
            '\nBinance USD Price: ', b_price,
            '\nWazirX USD Price: ', w_price,
            '\nVolume: ', wazir[4],
            '\nDiff/Coin: ', diff,
            '\nPercentage: ', percentage
        )
    print('\n')


# Print the stock usdt value if arbitrage possible
def print_arbitrage(wazir, binance, wazir_price, binance_price):
    w_price = wazir[1]
    b_price = binance[1]

    if float(w_price) != 0.0 and float(b_price) != 0.0:
        if w_price < b_price:
            diff = float(b_price) - float(w_price)
            percentage = diff / float(w_price)
            # variable to get the direction of flow
            direction = 0
        else:
            diff = float(w_price) - float(b_price)
            percentage = diff / float(b_price)    
            # variable to get the direction of flow
            direction = 1 
        percentage *= 100

        if percentage >= 5.0:
            flag = get_arbitrage_new(wazir_price, binance_price, wazir[0].lower())
            print(wazir)
            if flag == 1:
                formatted_print(wazir, b_price, w_price, diff, percentage, direction)
                temp = input('Do you want to track this coin (Y/N): ')
                if temp == 'Y' or temp == 'y' or temp == '':
                    trade_coin(wazir[0].lower()) 
                else:
                    return
        else:
            return

# Convectional method without the websocket
def get_arbitrage(wazir_price, binance_price):
    for i in range(len(wazir_price)):
        # print(wazir_price)
        w_symbol = wazir_price[i][0]
        for j in range(len(binance_price)):
            b_symbol = binance_price[j][0]
            if w_symbol == b_symbol:
                print_arbitrage(wazir_price[i], binance_price[j], wazir_price, binance_price)

# Websocket impelementation of getting the stock prices
def get_arbitrage_new(wazir_price, binance_price, symbol):
    if(symbol in ['stratusdt', 'npxsusdt', 'stormusdt', 'klayusdt']):
        return 0 
    binance_websocket.cc = symbol
    print(symbol.upper())
    binance_websocket.run_socket()
    return 1


def trade_coin(symbol):
    try:
        while(1):
            # print the binance coin price
            binance_websocket.cc = symbol
            # binance_websocket.run_socket() 

            # print the wazirx coin price
            wazir = get_wazir_data(symbol)
            print(wazir)
    except KeyboardInterrupt:
        return


# WazirX API reponse
'''
# Using Market Status api 

response = requests.get('https://api.wazirx.com/api/v2/market-status')
response = response.json()

wazir_response = response["markets"]
# wazir_response = parse_data(wazir_response)
# print_data(wazir_response)

wazir_price = []
for i in wazir_response:
    if(checkKey(i, "last") == 1 and checkKey(i, "volume") == 1):
        symbol = i["baseMarket"] + i["quoteMarket"]
        symbol = symbol.upper()
        last_price = i["last"]
        volume = i["volume"]
        if(i["quoteMarket"] == "usdt"):
            wazir_price.append([symbol, last_price, volume])
            # print("Symbol: ", symbol, " Last Price: ", last_price)
        # print("Symbol: ", symbol, " Last Price: ", last_price)

print(wazir_price)
'''
# Using tickers api

# response = requests.get('https://api.wazirx.com/api/v2/tickers')
# response = response.json()
# print(response)

# wazir_price = []
# for i in response:
#     if(checkKey(response[i], 'last') == 1 and checkKey(response[i], 'volume') == 1):
#         symbol = i.upper()
#         sell = response[i]['sell']
#         buy = response[i]['buy']
#         last = response[i]['last']
#         volume = response[i]['volume']
#         if response[i]['quote_unit'] == 'usdt':
#             wazir_price.append([symbol, last, sell, buy, volume])

# print(wazir_price)
wazir_price = []
def get_wazir_data(symbol=''):
    trade_wazir_price = []
    check_symbol = symbol
    # print(symbol)
    # Using tickers api 
    response = requests.get('https://api.wazirx.com/api/v2/tickers')
    response = response.json()
    # print(response)
    for i in response:
        if(checkKey(response[i], 'last') == 1 and checkKey(response[i], 'volume') == 1):
            symbol = i.upper()
            sell = response[i]['sell']
            buy = response[i]['buy']
            last = response[i]['last']
            volume = response[i]['volume']
            if response[i]['quote_unit'] == 'usdt':
                wazir_price.append([symbol, last, sell, buy, volume])
    # print(wazir_price)	
    trade_wazir_price = wazir_price
    wazir = []
    for i in range(len(trade_wazir_price)):
        if check_symbol.upper() == trade_wazir_price[i][0]:
            wazir = trade_wazir_price[i]

    return wazir

# Binance API response
response = requests.get('https://api.binance.com/api/v3/ticker/price')
response = response.json()
# print(response)

binance_price = []
for i in response:
    if(checkKey(i, "price") == 1):
        b_symbol = i["symbol"]
        b_last_price = i["price"]
        binance_price.append([b_symbol, b_last_price])

get_wazir_data()
get_arbitrage(wazir_price, binance_price)
# get_arbitrage_new(wazir_price, binance_price, symbol)
