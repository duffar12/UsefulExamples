import websocket
import json
import logging
import requests

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger()

def get_pairs():
    url = 'https://www.okex.com/api/v1/tickers.do'
    response = requests.get(url).json()['tickers']
    symbols = [r['symbol'] for r in response]
    return symbols

def on_open(ws):
    subscriptions = [{'event':'addChannel','channel':'ok_sub_spot_bch_btc_deals'}
                    ,{'event':'addChannel','channel':'ok_sub_spot_eth_btc_deals'}]
    for subscription in subscriptions:
        print("subscribing to subscritpion {}".format(subscription['channel']))
        ws.send(json.dumps(subscription).encode())


def on_message(ws, message):
    result = json.loads(message)
    print(result)


def on_error(ws, error):
    print("hit error " + error)


def on_close():
    print("#closed#")


if __name__ == '__main__':

    print(get_pairs())

    url = 'wss://real.okex.com:10441/websocket'
    ws = websocket.WebSocketApp(url
                                ,on_open=on_open
                                ,on_message=on_message
                                ,on_close=on_close
                                ,on_error=on_error )

    ws.run_forever()
