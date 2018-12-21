import websocket
import json
import time
import hmac
import hashlib
import threading

# Base class for all BfxAlgoProcesses
class WSClient(object):

    def __init__(self):
        self.url = "wss://api.lbkex.com/ws/V2/"
        self.msg_c = 0
        self.last_message_time = int(time.time())
        self.thread_started = False
        self.thread = None
        self.is_connected = False

    def maintain_connection(self, ws):
        # Poloniex specify that a heartbeat should be received every second. If heartbeats are not received they
        # reccommend reconnecting to the websocket.
        # This method will reconnect the websocket if a heartbeat or any other message has not been received in the
        # last 10 seconds
        # Note that closing the websocket, will force a reconnect in the _on_close method
        while True:
            print("checking messages now = {} last_time = {}".format(int(time.time()), self.last_message_time))
            if int(time.time()) - self.last_message_time > 10:
                print("No messages received in the last 10 seconds. Restarting websocket connection")
                ws.close()
            time.sleep(2)
            try:
                ws.send(json.dumps({"action":"ping", "ping":"myserv"}))
            except:
                pass

    def on_open(self, ws):

        print("#open")
        self.is_connected = True
        s =  {"action": "subscribe"
             ,"subscribe": "trade"
             ,"pair": "eth_btc"}
             #,"size": 100}

        ws.send(json.dumps(s))

    def on_message(self, ws, message):
        print("on message")
        self.last_message_time = int(time.time())
        self.msg_c += 1
        message = json.loads(message)
        print(message)

    def on_error(self, ws, error):
        print("#error")
        print(error)

    def on_close(self, ws):
        print("#closed")
        self.is_connected = False
        self.run()

    def run(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.url
                                    ,on_message = self.on_message
                                    ,on_error = self.on_error
                                    ,on_close = self.on_close
                                    ,on_open = self.on_open)

        if self.thread == None or self.thread.is_alive() == False:
            print("starting thread")
            self.thread = threading.Thread(target=self.maintain_connection, args=(ws,))
            self.thread.start()
        ws.run_forever()


if __name__ == '__main__':
    ws_client = WSClient()
    ws_client.run()
    websocket.enableTrace(True)

