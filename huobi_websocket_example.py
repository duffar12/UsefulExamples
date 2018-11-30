import websocket
import json
import gzip


def on_open(ws):
    subscriptions = [{"sub": "market.ethbtc.trade.detail", "id": "id1"}]
    for subscription in subscriptions:
        ws.send(json.dumps(subscription).encode())


def on_message(ws, message):
    result=gzip.decompress(message).decode('utf-8')
    print(result)
    if "ping" in result:
        hb ={"ping": 18212558000}
        ws.send(json.dumps(hb).encode())


def on_error(ws, error):
    print("hit error")
    print(error)


def on_close():
    print("#closed#")


if __name__ == '__main__':

    url = 'wss://api.huobi.pro/ws'
    ws = websocket.WebSocketApp(url
                                ,on_open=on_open
                                ,on_message=on_message
                                ,on_close=on_close
                                ,on_error=on_error )

    ws.run_forever()
