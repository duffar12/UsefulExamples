import websocket
import json
import time
import hmac
import hashlib

# Base class for all BfxAlgoProcesses
class WSClient(object):

    def __init__(self):
        self.url = "wss://api.bitfinex.com/ws/2"
        keys = self._get_keys()
        self.api = keys[0]
        self.secret = keys[1]
        self.count = 0

    # read api keys from a keys file
    def _get_keys(self):
        with open('keys/bitfinex.key') as f:
            keys = f.readlines()
            keys = [key.rstrip('\n') for key in keys]
        return keys

    # Internal method to add authentication to API requests
    def get_auth_subscription(self):
        auth_nonce = str(time.time() * 1000000)
        auth_payload = 'AUTH' + auth_nonce
        auth_sig = hmac.new(self.secret.encode(), auth_payload.encode(), hashlib.sha384).hexdigest()

        auth_subscription = {'event': 'auth'
                            ,'apiKey': self.api
                            ,'authPayload': auth_payload
                            ,'authSig': auth_sig
                            ,'authNonce': auth_nonce
                            ,'filter': ['wallet']}

        return auth_subscription

    def on_open(self, ws):
        s =  {"event": "subscribe"
            ,"channel": "book"
            ,"prec": 'R0'
            ,"len": "100"
            ,"symbol": 'tBTCUSD'} 

        ws.send(json.dumps(s))
        s = { "event": "conf","flags": 98304 }
        ws.send(json.dumps(s))
        #ws.send(json.dumps(self.get_auth_subscription()))

    def on_message(self, ws, message):
        print(message)
        self.count += 1
        if self.count > 4:
            pass
            #ws.close()
        #message = json.loads(message)
        #if type(message) == list and  message[1] == 'hb':
        #    ws.close()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("#closed")



if __name__ == '__main__':

    # While True - means that websocket will reconnect every time we try to close it 
    while True:
        ws_client = WSClient()
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(ws_client.url
                                    ,on_message = ws_client.on_message
                                    ,on_error = ws_client.on_error
                                    ,on_close = ws_client.on_close
                                    ,on_open = ws_client.on_open)
        ws.run_forever()
        time.sleep(1)
