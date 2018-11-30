# WS server example

import asyncio
import websockets
import json
import time

# Send orderbook snapshot
# 3 updates
# 1 insert
# 1 delete


loop = asyncio.get_event_loop()
best_bid =  []
best_ask =  []
count = 0

async def send_snapshot(websocket):
    # Send an  initial snapshot of an orderbook. the exammple used was captured from bitfinex and is stored in data.json
    with open('data.json') as fi:
        data =  fi.readlines()[0].split('\n')
        data = json.loads(data[0])

    global best_bid
    global best_ask
    chan_id = data[0]
    best_bid = [chan_id,data[1][0]]
    best_ask = [chan_id, data[1][100]]
    await websocket.send(json.dumps(data))

async def send_message(websocket, message):
    global count
    for i in range(100):
        count +=1
        c = count *1
        message[1][1] = time.time() * 1000000
        await websocket.send(json.dumps(message))
        if count % 5000 == 0:
            print(message, " number {} sent at {}".format(c, time.time() *1000000))

async def send_new_best_bid(websocket):
    global best_bid
    global loop
    for i in range(10000):
        loop.create_task(send_message(websocket, best_bid))

async def send_new_best_ask(websocket):
    global best_ask
    global loop
    for i in range(10000):
        loop.create_task(send_message(websocket, best_ask))

async def hello(websocket, path):
    global loop
    name = await websocket.recv()
    await websocket.send(json.dumps({"event":"info","version":2,"serverId":"9704b94c-9d8f-451c-ae37-73ed80bdf851","platform":{"status":1}}))
    await websocket.send(json.dumps({"event":"subscribed","channel":"book","chanId":312671,"symbol":"tBTCUSD","prec":"R0","freq":"F0","len":"100","pair":"BTCUSD"}))
    await send_snapshot(websocket)
    loop.create_task(send_new_best_ask(websocket))
    loop.create_task(send_new_best_bid(websocket))
    await asyncio.sleep(100000)
    #loop.create_task(send_new_best_bid(websocket))


start_server = websockets.serve(hello, 'localhost', 8765)

loop.run_until_complete(start_server)
print("gathering pending tasks")
pending = asyncio.Task.all_tasks()
loop.run_until_complete(asyncio.gather(*pending))
loop.run_forever()
