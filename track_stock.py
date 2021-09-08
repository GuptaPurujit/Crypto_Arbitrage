import binance_websocket
import requests


def checkKey(dict, key): 
    if key in dict.keys():
        return 1
    else:
        return 0


# Call the binance websocket and get real time data and wazirx api
def trade_coin(symbol, wazir):
    try:
        while(1):
            # print the binance coin price
            binance_websocket.cc = symbol
            binance_websocket.run_socket            
            # print the wazirx coin price
            wazir = get_wazir_data(symbol)
            print(wazir)
    except KeyboardInterrupt:
        return


def get_wazir_data(symbol):
    check_symbol = symbol
    # Using tickers api 
    response = requests.get('https://api.wazirx.com/api/v2/tickers')
    response = response.json()
    # print(response)   
    wazir_price = []
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
    wazir = []
    for i in range(len(wazir_price)):
        if check_symbol.upper() == wazir_price[i][0]:
            wazir = wazir_price[i]

    return wazir
