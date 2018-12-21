import pandas as pd

bar = '1h'
data = pd.read_csv("ETHUSD.csv")
data = data[['timestamp', 'price', 'volume']]
data.rename(columns={'timestamp': 'datetime', 'price': 'close', 'volume': 'volume'}, inplace=True)
data['volume_abs'] = data['volume'].abs()

data = data.set_index('datetime')
data.index = pd.to_datetime(data.index, unit='ms', errors='coerce')

""" Logic to create ohlc candles data along with sum of positives, sum of negatives, sum of volumes"""
df_ohlc = data['close'].resample(bar).ohlc()
df_abs_vol = data['volume_abs'].resample(bar).sum()  # sums absolutes of volumes
df_cum_vol = data['volume'].resample(bar).sum()  # sums all volumes with their signs
df_pos_vol = (df_abs_vol + df_cum_vol) / 2  # sums only positive volumes
df_pos_vol.rename('pos_volume', inplace=True)
df_neg_vol = df_pos_vol - df_abs_vol  # sums only negative volumes
df_neg_vol.rename('neg_volume', inplace=True)

"""Create candle dataframe """
df_ohlcvv = pd.concat([df_ohlc, df_pos_vol, df_neg_vol, df_cum_vol], axis=1)

"""Drop windows which don't have any trades"""
df_ohlcvv.dropna(how='any', inplace=True)

"""Add timestamp column and reshuffle the columns"""
df_ohlcvv['timestamp'] = pd.to_datetime(df_ohlcvv.index).astype(int) // 10 ** 6
df_ohlcvv = df_ohlcvv[list(df_ohlcvv)[-1:] + list(df_ohlcvv)[:-1]]

"""Get max timestamp from the dataframe and drop last window because it is not complete"""

"""Check if data is non-empty and create if snapshotfile for first time or append tempfile to the snapshotfile file"""
print(df_ohlcvv)

for month in range(1,13):
    df_ohlcvv_monthly = df_ohlcvv.loc[df_ohlcvv.index.month == month]
    if len(df_ohlcvv_monthly > 0):
        print(df_ohlcvv_monthly)

