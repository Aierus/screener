# Import data from polygon.io or from yahoo finance (stocks over 500M MKT CAP)
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import time

# Variables
spooz = si.tickers_sp500()
naz = si.tickers_nasdaq()
dow = si.tickers_dow()
naz_name = '^IXIC'   #NASDAQ
spooz_name = '^GSPC' #SPX
dow_name = '^DJI'    #DOW
indicies = [spooz, naz, dow]
index_name = [spooz_name, naz_name, dow_name]
for i in range(len(indicies)):
  indicies[i] = [item.replace(".", "-") for item in indicies[i]] #formatting
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
yester_date = datetime.datetime.now() - datetime.timedelta(days=1)
end_date = datetime.date.today()
exportList = pd.DataFrame(columns=['Stock', 'Volume', 'Weighted Volume'])

spooz_data = pdr.get_data_yahoo('SPY', start_date, end_date)
spooz_data.to_csv('SPY.csv')

spooz_yester_data = pdr.get_data_yahoo('SPY', yester_date - datetime.timedelta(days=1), end_date)
spooz_yester_data.to_csv('SPY_YESTERDAY.csv')

spooz_today_data = pdr.get_data_yahoo('SPY', yester_date, end_date)
spooz_today_data.to_csv('SPY_TODAY.csv')

# spooz_list = list(spooz_today_data)
# print(spooz_list)

# spooz_today = pd.read_csv('SPY_TODAY.csv')
# print(spooz_today.columns.values.tolist())
# print(spooz_today['Volume'])

# spooz_data.columns.values.tolist()
# for i in range len(spooz_data.columns):
#   spooz_volume = spooz_today.loc[spooz_today.index, 'Volume'].iat[i]

# Write data to CSV
for i in range(len(index_name)):
  for ticker in indicies[i]:
    df = pdr.get_data_yahoo(ticker, start_date, end_date)
    rows = len(df.index)
    weighted_vol = []

    for i in range(rows):
      tmp = df.loc[df.index, 'Volume'].iat[i]
      weighted_vol.append(tmp)
      weighted_vol[i] = weighted_vol[i] / (spooz_data.loc[spooz_data.index, 'Volume'].iat[i]/100)
    df['SPY Weighted Volume'] = weighted_vol

    # Create a 365 day average volume and average SPY weighted vol
    total_vol = 0
    total_spy_vol = 0
    for i in range(rows):
      total_vol += df.loc[df.index, 'Volume'].iat[i]
      total_spy_vol += spooz_data.loc[spooz_data.index, 'Volume'].iat[i]
    average_vol = total_vol / rows
    average_spy_vol = total_spy_vol / rows

    # Check to see if day's volume is 50% greater than previous day
    volume_deviation = []
    volume_deviation_values = []
    for i in range(rows):
      if ((df.loc[df.index, 'SPY Weighted Volume'].iat[i]) > (1.5 * df.loc[df.index, 'SPY Weighted Volume'].iat[i-1])):
        volume_deviation.append('+')
        p_vol_dev = ((df.loc[df.index, 'SPY Weighted Volume'].iat[i] - df.loc[df.index, 'SPY Weighted Volume'].iat[i-1]) / df.loc[df.index, 'SPY Weighted Volume'].iat[i]) * 100
        p_vol_dev = round(p_vol_dev, 4)
        volume_deviation_values.append(p_vol_dev)
        # print('Ticker %s on day %d; Had a weighted volume deviation of %.4f from the previous day\n' % (ticker, i, p_vol_dev))
      else:
        volume_deviation.append('-')
        volume_deviation_values.append('-')
    df['Volume Deviation'] = volume_deviation
    df['Volume Deviation Value'] = volume_deviation_values

    df.to_csv(f'{ticker}.csv')
    print(f'Writing {ticker} to csv')

# Create DataFrame
#vol_df = pd.DataFrame(list(zip(tickers, )))



