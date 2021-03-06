import websocket
import json
import gzip
import logging
import requests

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger()

def get_pairs():
    url = 'https://api.huobi.pro/v1/common/symbols'
    response = requests.get(url).json()['data']
    symbols = [r['symbol'] for r in response]
    return symbols


def on_message(ws, message):
    result = json.loads(gzip.decompress(message).decode('utf-8'))
    print(result)


def on_open(ws):
    for pair in ['ltcbtc', 'ethbtc']:
        print("subscribing to pair {}".format(pair))
        ws.send(json.dumps({"sub": "market.{}.trade.detail".format(pair), "id": pair}).encode())

def on_error(ws, error):
    print("hit error " + error)


def on_close():
    print("#closed#")


if __name__ == '__main__':

    url = 'wss://api.huobi.pro/ws'
    ws = websocket.WebSocketApp(url
                                ,on_open=on_open
                                ,on_message=on_message
                                ,on_close=on_close
                                ,on_error=on_error )

    ws.run_forever(ping_interval=1)
