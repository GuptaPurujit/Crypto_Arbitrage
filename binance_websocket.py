from websocket import create_connection
import websocket, json


cc = ''
interval = '1m'
closes, highs, lows = [], [], []

'''
# Long Lived Connection

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    high = candle['h']
    low = candle['l']
    vol = candle['v']

    print(close, high, low, vol, is_candle_closed)
    # if is_candle_closed == True:
    #     closes.append(float(close))
    #     highs.append(float(high))
    #     lows.append(float(low))

    #     print(closes)
    #     print(highs)
    #     print(lows)
    # ws.close()


def on_close(ws, close_status_code, close_msg):
    # print(close_status_code, close_msg)
    print("Connection Closed")


def on_error(ws, error):
    print(error)


def run_socket():
    socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
    ws = websocket.WebSocketApp(socket, 
                                on_message=on_message, 
                                on_close=on_close,
                                on_error=on_error)
    ws.run_forever()
'''

# Short Lived Connection (Faster) 

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    high = candle['h']
    low = candle['l']
    vol = candle['v']

    print(close, high, low, vol, is_candle_closed)
    # if is_candle_closed == True:
    #     closes.append(float(close))
    #     highs.append(float(high))
    #     lows.append(float(low))

    #     print(closes)
    #     print(highs)
    #     print(lows)


def run_socket():
    ws = create_connection(f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}')
    result = ws.recv()
    on_message(ws, result)

# run_socket()
