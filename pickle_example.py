import json
import time
from timeit import timeit
import pickle
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


def nats_write_pickle(arr, loop):
    global nats
    now = time.time() * 1000
    loop.run_until_complete(nats.publish("pickle", pickle.dumps(arr)))
    end = time.time() * 1000
    print("nats_write_pickle time taken = {}".format(int(end - now)))

def nats_write_json(arr, loop):
    global nats
    now = time.time() * 1000
    loop.run_until_complete(nats.publish("pickle", json.dumps(arr).encode()))
    end = time.time() * 1000
    print("nats_write_json time taken = {}".format(int(end - now)))


def time_json_dumps(arr):
    start  = time.time() *1000
    json.dumps(arr).encode()
    end  = time.time() *1000
    print("json dumps time = ", end - start)


def time_pickle_dumps(arr):
    start  = time.time() *1000
    pickle.dumps(arr)
    end  = time.time() *1000
    print("pickle dumps time = ", end - start)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_connect(loop))
    arr = [i for i in range(100000)]
    time_pickle_dumps(arr)
    time_json_dumps(arr)
    nats_write_pickle(arr, loop)
    nats_write_json(arr, loop)




