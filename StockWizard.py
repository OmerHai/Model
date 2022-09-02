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

# Gets JSON file with all the stock market data from the last 20 years
url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(stock,api_key)

# Save the receiving data to file
file_to_save = 'stock_market_data-%s.csv'%stock

# Check if file already exist
if not os.path.exists(file_to_save):
    with urllib.request.urlopen(url_string) as url:
        # Load json from url
        data = json.loads(url.read().decode())
        # Extract stock market data for daily time series
        data = data['Time Series (Daily)']
        # Create data frame with columns date, low, high, close and open
        df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
        # Loop over all the data
        for k,v in data.items():
            # Create date 
            date = dt.datetime.strptime(k, '%Y-%m-%d')
            data_row = [date.date(),float(v['3. low']),float(v['2. high']), float(v['4. close']),float(v['1. open'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
    print('Data saved to : %s'%file_to_save)    
    # Save data in csv file   
    df.to_csv(file_to_save)
# If the data is already there, just load it from the CSV
else:
    print('File already exists. Loading data from CSV')
    df = pd.read_csv(file_to_save)

# Sort dataFrame by date
df = df.sort_values('Date')
# Print the first 5 rows in the data
print(df.head())

# Calculate the high price 
high_prices = df.loc[:,'High'].to_numpy()
# Calculate the low price 
low_prices = df.loc[:,'Low'].to_numpy()
# Calculate the mid price 
mid_prices = (high_prices+low_prices)/2.0

# Split data to training and test when data is the mid price
train_data = mid_prices[:11000]
test_data = mid_prices[11000:]

# Normalize the data to be between 0 to 1
scaler = MinMaxScaler()
train_data = train_data.reshape(-1,1)
test_data = test_data.reshape(-1,1)



