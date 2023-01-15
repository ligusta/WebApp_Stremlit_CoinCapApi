import requests
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import calendar

# Initialize Streamlit
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Creating a sidebar in Streamlit

crypto_name = st.sidebar.selectbox('Crypto coin', ('bitcoin', 'ethereum', 'bitcoin-cash', 'eos', 'stellar', 'litecoin', 'cardano', 'tether', 'iota', 'tron')) 
date_from = st.sidebar.date_input('Date from' ,datetime.date(2022, 10, 15))
date_to = st.sidebar.date_input('Date to' ,datetime.date(2023, 1, 15))

# Converting the date to UNIX format

def to_seconds(d):
    return calendar.timegm(d.timetuple())

date_from = to_seconds(date_from) * 1000
date_to = to_seconds(date_to) * 1000

# Getting data from the CoinCap API

url = f"https://api.coincap.io/v2/assets/{crypto_name}/history?interval=d1&start={date_from}&end={date_to}"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

json_data = json.loads(response.text.encode('utf8'))

bitcoin_data = json_data["data"]

# Writing data received from the Coinsup API to a CSV file
# Adding an additional column 'date' for the date in the "human format"

df = pd.DataFrame(bitcoin_data, columns=['time', 'priceUsd','date'])
df['time'] = (df['time']/1000).astype(int)
df['date'] = df['date'].astype(str)

time = []
for i in range(len(df)): 
    time = datetime.datetime.utcfromtimestamp(df['time'].values[i]).strftime('%Y-%m-%d')
    df['date'].values[i] = time

df['priceUsd'] = pd.to_numeric(df['priceUsd'], errors='coerce').fillna(0, downcast='infer')
df.to_csv('crypto-exchange.csv', index=False)


# Open the csv file to import into Streamlit
crypto_exchange = pd.read_csv('crypto-exchange.csv')

# Creating a column in Streamlit
st.markdown('Cryptocurrency exchange rate')
st.bar_chart(crypto_exchange, x = 'date', y = 'priceUsd')