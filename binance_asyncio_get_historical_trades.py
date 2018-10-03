import yaml
import requests
from collections import deque
import logging
import time
import aiohttp
import asyncio

REQUEST_TIMES = deque()
BINANCE_RESPONSE_LENGTH = 1000
RATE_LIMIT = 239
logger = logging.getLogger()

def get_api_key():
    with open('binance.yml', 'r') as ymlfile:
        return yaml.load(ymlfile)["api_key"]

API_KEY = get_api_key()

def do_something_with_data(data):
    logging.error(data)

def is_rate_limit_exceeded():
    global RATE_LIMIT
    global REQUEST_TIMES
    start_time = 0
    now = int(time.time() * 1000)
    while len(REQUEST_TIMES) > 0 and (now - start_time) > 60000:
        # REQUEST_TIMES is a deque of timestamps of all of the requests made in the last 60 seconds
        # Update REQUEST_TIMES and then check how many requests there are
        start_time = REQUEST_TIMES.popleft()
        if (now - start_time) <= 60000:
            REQUEST_TIMES.appendleft(start_time)

    if len(REQUEST_TIMES) >= RATE_LIMIT:
        return True
    else:
        REQUEST_TIMES.append(now)
        print("request rate = {}".format(len(REQUEST_TIMES)))
        return False

def chunks(arr, n):
    """Yield successive n-sized chunks from arr"""
    for i in range(0, len(arr), n):
        yield arr[i:i + n]

async def get_trades(symbols):
    global BINANCE_RESPONSE_LENGTH
    for symbol in  symbols:
        # Binance trade tick data requires a public api_key in the header
        headers = {'X-MBX-APIKEY': API_KEY}
        params = {'symbol':symbol, 'limit':1000, 'fromId': 1}
        url = 'https://api.binance.com/api/v1/historicalTrades'
        response_length  = BINANCE_RESPONSE_LENGTH
        while response_length == BINANCE_RESPONSE_LENGTH:
            if is_rate_limit_exceeded():
                await asyncio.sleep(1)
            else:
                async with aiohttp.ClientSession().get(url=url, params=params, headers=headers) as response:
                    try:
                        response.raise_for_status()
                    except:
                        logger.exception("Error getting data for {}".format(symbol))
                        await asyncio.sleep(61)
                    else:
                        json_response = await response.json()
                        response_length = len(json_response)
                        params['fromId'] = json_response[-1]['id']
                        do_something_with_data(json_response)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    url = 'https://api.binance.com/api/v1/exchangeInfo'
    r = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols']
    symbols = [x['symbol'] for x in r]
    chunks =  list((chunks(symbols, 75)))
    for chunk in chunks:
        loop.create_task(get_trades(chunk))
    
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))

