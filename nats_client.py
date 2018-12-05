import socket
import json
from nats.aio.client import Client as NATS
import asyncio
import time

nats = NATS()

async def nats_connect(loop):
    global nats
    try:
        await nats.connect(servers=["nats://0.0.0.0:4222"],
                                connect_timeout=10, dont_randomize=True,
                                allow_reconnect=True, loop=loop,
                                error_cb=error_cb, max_reconnect_attempts=8640,
                                reconnect_time_wait=10
                                )
    except Exception as ermsg:
        print(str(ermsg))
        if str(ermsg) == 'nats: No servers available for connection':
            sys.exit(1)

async def error_cb(error):
    """ Write error to the log file"""
    print("error_callback:" + str(error))

def nwrite():
    with open('websocket_server/data.json') as fi:
        data = fi.readlines()[0]
        data = data.split('/n')[0]
    orderbook = data 
    print(orderbook)
    global nats
    now = time.time() * 1000
    for i in range(1000000):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(nats.publish("orderbook." + "bitfinex" + "." + "ethusd", json.dumps(orderbook).encode()))
        #tasks = [asyncio.ensure_future(nats.publish("orderbook." + "bitfinex" + "." + "ethusd", json.dumps(orderbook).encode()))]
        #loop.run_until_complete(nats.publish("orderbook." + "bitfinex" + "." + "ethusd", json.dumps(orderbook).encode()))
        #print("printed ",i)
    end = time.time() * 1000
    print("time taken = {}".format(int(end - now)))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(nats_connect(loop))]
    loop.run_until_complete(asyncio.wait(tasks))
    #time.sleep(1)
    #loop.run_until_complete(nwrite())
    nwrite()



