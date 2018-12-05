import websocket
import json
import gzip
import logging
import requests
import pandas as pd

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger()

def get_pairs():
    r = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols']
    response = json.dumps(r)
    symbols = pd.read_json(response).rename(columns={0:"symbol"})
    symbols_list = symbols['symbol'].tolist()
    return symbols_list
    #symbols = [x['symbol'] for x in r]
    #return symbols


def on_message(ws, message):
    result = json.loads(message)
    print(type(result['data']['q']))
    print(float(result['data']['q']))
    print(result)


def on_open(ws):
    print("opendlsjaflsdja")

def on_error(ws, error):
    print("hit error " + error)


def on_close():
    print("#closed#")


if __name__ == '__main__':

    url = 'wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade/'
    ws = websocket.WebSocketApp(url
                                ,on_open=on_open
                                ,on_message=on_message
                                ,on_close=on_close
                                ,on_error=on_error )

    ws.run_forever(ping_interval=1)
