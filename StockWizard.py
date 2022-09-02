# Import libaries
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf 
from sklearn.preprocessing import MinMaxScaler

# Api key for alphavantage api
api_key = 'TBIK5DH2QYZIRSOR'

# Varaible for stock we want to check
stock = "AAL"

# JSON file with all the stock market data for the stock from the last 20 years
url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(stock,api_key)

# Save the reciving data to file
file_to_save = 'stock_market_data-%s.csv'%stock

# If you haven't already saved data,
# Go ahead and grab the data from the url
# And store date, low, high, volume, close, open values to a Pandas DataFrame

# Check if data already exist
if not os.path.exists(file_to_save):
    with urllib.request.urlopen(url_string) as url:
        # Load json from url
        data = json.loads(url.read().decode())
        # Extract stock market data for daily time series
        data = data['Time Series (Daily)']
        df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
        for k,v in data.items():
            date = dt.datetime.strptime(k, '%Y-%m-%d')
            data_row = [date.date(),float(v['3. low']),float(v['2. high']), float(v['4. close']),float(v['1. open'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
    print('Data saved to : %s'%file_to_save)        
    df.to_csv(file_to_save)
# If the data is already there, just load it from the CSV
else:
    print('File already exists. Loading data from CSV')
    df = pd.read_csv(file_to_save)