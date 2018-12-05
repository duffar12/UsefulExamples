import websocket
import json
import time
import hmac
import hashlib
import threading

# Base class for all BfxAlgoProcesses
class WSClient(object):

    def __init__(self):
        self.url = "wss://api2.poloniex.com"
        self.msg_c = 0
        self.last_message_time = int(time.time())
        self.thread_started = False
        self.thread = None

    def maintain_connection(self, ws):
        # Poloniex specify that a heartbeat should be received every second. If heartbeats are not received they
        # reccommend reconnecting to the websocket.
        # This method will reconnect the websocket if a heartbeat or any other message has not been received in the
        # last 10 seconds
        # Note that closing the websocket, will force a reconnect in the _on_close method
        while True:
            #print("checking messages")
            if int(time.time()) - self.last_message_time > 10:
                print("No messages received in the last 10 seconds. Restarting websocket connection")
                ws.close()
            time.sleep(2)

    def on_open(self, ws):
        s =  {"command": "subscribe"
            ,"channel": "BTC_ETH"}
        ws.send(json.dumps(s))
        print("#open")

    def on_message(self, ws, message):
        self.last_message_time = int(time.time())
        self.msg_c += 1
        message = json.loads(message)
        print(message)

    def on_error(self, ws, error):
        print("#error")
        print(error)

    def on_close(self, ws):
        print("#closed")
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

