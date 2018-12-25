
import psycopg2
import pandas as pd
import logging
import numpy as np
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class DatabaseError(Exception):
    pass


class PgresDatabase:
    def __init__(self, table):
        self.table = table
        self.con = psycopg2.connect("dbname = 'bfx_data' user= 'postgres' host='localhost' port ='5432' password ='helloworld'")
        self.cursor = self.con.cursor()

    def execute_query(self, query):
        '''Helper function to perform Database writes'''
        try:
             self.cursor.execute(query)
        except:
             self.con.rollback()
             logger.error("Could not commit query to DB: {}".format(query))
             #raise DatabaseError
        else:
             self.con.commit()

    def insert_candles(self, symbol, candles):

        last_mts = 0
        for candle in candles:
            if candle[0] != last_mts:
                query = 'INSERT INTO {}(mts, open, close,  high, low,  volume) VALUES({},{},{},{},{},{})'.format(self.table, candle[0],candle[1],candle[2],candle[3],candle[4],candle[5])
                last_mts = candle[0]
                self.execute_query(query)

    def get_latest_candle_date(self, symbol):
        """
        Get the time of the most recent candle for a symbol
        """
        self.cursor.execute('select max(mts) from {}'.format(self.table))
        result = self.cursor.fetchone()[0]
        if result is None:
            return
        else:
            return result


def print_yearly_trades(data, sma, lma):
    print("printing yearly trades")
    initial_num = 365*24*60
    data = pd.DataFrame(data)
    data.columns = ['id', 'mts', 'open', 'close', 'high', 'low', 'volume','datetime']
    data['ma_20'] = data.close.rolling(window=lma).mean()
    data['ma_5'] = data.close.rolling(window=sma).mean()
    data = data.dropna(axis=0, how='any')
    data['difference'] = data.ma_20 - data.ma_5
    data['datetime'] = pd.to_datetime(data.mts, unit='ms')
    data['cross'] = np.sign(data.difference.shift(1))!=np.sign(data.difference)
    data = data[['id', 'mts', 'datetime', 'open', 'close', 'difference', 'cross', 'ma_20', 'ma_5']]
    data.to_csv('data.csv')

    data = data.loc[data.cross == True]
    data['buys'] = data.ma_5 > data.ma_20
    data['sells'] = data.ma_20 > data.ma_5
    data = data[['mts', 'open', 'close', 'ma_20', 'ma_5', 'buys', 'sells']]
    data['profits'] = np.where(data['buys']==True, data.close.shift(1) - data.close,  data.close - data.close.shift(1))
    data['mdd'] = data.profits.cumsum()

    #data = data.loc[data.buys == True]
    profit = data.profits.sum()
    mdd = data.mdd.min()
    mpp = data.mdd.max()
    print(data)
    print('total profit = ', profit)
    print('max drawdown = ', mdd)
    print('max profit = ', mpp)



if __name__ == "__main__":
    table = 'eth_usd'
    day_offset = 100
    start_time = time.time() - (day_offset *24*60*60)
    print(start_time)
    start_time *= 1000
    con = psycopg2.connect("dbname = 'bfx_data' user= 'postgres' host='localhost' port ='5432' password ='helloworld'")
    cursor = con.cursor()
    cursor.execute('select * from {} where mts > {}'.format(table, start_time))
    print('select * from {} where mts > {}'.format(table, start_time))
    data =  cursor.fetchall()
    print(len(data)/(24*60))
    ma= [[5,20], [7,28], [3,12], [100,400], [250, 1000]]
    ma= [[5,20], [3,12], [2,8], [1,4]]
    for m in ma:
        print_yearly_trades(data, m[0], m[1])



