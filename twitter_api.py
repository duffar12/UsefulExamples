from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import time

API_KEY = 'ix6rKRbrpGtNcRlhjz5UZupov'
API_SECRET = 'CKRLlCh3JdTgYn2WEPXwKtgXPr2Wzz7H21fhzWWwLEB5kZXHAK'
ACCESS_KEY = '1961279430-a7XIIqZvNNDqcPQf2w1Exa2EKadXA9zqPnNOY5d'
ACCESS_SECRET = 'v6vNY8x2AKHv8MUSLQIYeepFBMhupLW02w8JB1ib29PJM'

class StdOutlistener(StreamListener):

    def __init__(self):
        self.tweets = 0
        self.start = time.time() * 1000

    def on_data(self, raw_data):
        self.tweets += 1
        now = time.time() * 1000
        if now - self.start > 1000:
            print('tweets per second = ', self.tweets)
            self.tweets = 0
            self.start = time.time() * 1000
        raw_data = json.loads(raw_data)
        #for k, v in raw_data.items():
        #    print(k,v)
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    listener = StdOutlistener()
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=["BTC", "ETH"])
