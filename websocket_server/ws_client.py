import websocket
import time

count = 0
def on_open(ws):
    print("opened")
    ws.send("new")
def on_message(ws, message):
    global count
    count += 1
    if count % 10000 == 0:
        print(message, "{} received at {}".format(count, time.time() *1000))
def on_error(ws, error):
    pass
def on_close(ws):
    print("closed")


if __name__ == '__main__':
    ws = websocket.WebSocketApp('ws://localhost:8765'
                                ,on_message = on_message
                                ,on_error = on_error
                                ,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()