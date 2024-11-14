import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import time
import os

# Set up Streamlit page configuration
st.set_page_config(page_title="Bitcoin Market Cap Dashboard", layout="wide")

# File path for storing data
csv_file = "bitcoin_market_cap_365_days.csv"

# Function to fetch historical data (last 365 days) and save to CSV
def fetch_historical_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    parameters = {
        "vs_currency": "usd",
        "days": "365",
        "interval": "daily"
    }
    response = requests.get(url, params=parameters)
    data = response.json()

    if 'market_caps' in data:
        timestamps = [entry[0] for entry in data['market_caps']]
        market_caps = [entry[1] for entry in data['market_caps']]
        df = pd.DataFrame({
            "Timestamp": pd.to_datetime(timestamps, unit='ms'),
            "Market Cap (USD)": market_caps
        })
        df.to_csv(csv_file, index=False)
        return df
    else:
        st.error("Failed to fetch historical data.")
        return pd.DataFrame(columns=["Timestamp", "Market Cap (USD)"])

# Function to fetch the latest market cap and add to DataFrame
def fetch_latest_market_cap():
    url = "https://api.coingecko.com/api/v3/simple/price"
    parameters = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_market_cap": "true"
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    if "bitcoin" in data and "usd_market_cap" in data["bitcoin"]:
        market_cap = data["bitcoin"]["usd_market_cap"]
        timestamp = datetime.now()
        return {"Timestamp": timestamp, "Market Cap (USD)": market_cap}
    return None

# Load or fetch historical data
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
else:
    df = fetch_historical_data()

# Streamlit header and description
st.title("Real-Time Bitcoin Market Cap Dashboard")
st.write("This dashboard displays the historical and real-time market cap of Bitcoin.")

# Update data every minute (simulating real-time updates)
latest_data = fetch_latest_market_cap()
if latest_data:
    df = df.append(latest_data, ignore_index=True)
    df.to_csv(csv_file, index=False)

# Display the latest market cap
st.subheader("Latest Bitcoin Market Cap (USD)")
st.metric(label="Market Cap", value=f"${latest_data['Market Cap (USD)']:,}")

# Plot the data using Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Timestamp'],
    y=df['Market Cap (USD)'],
    mode='lines+markers',
    name='Bitcoin Market Cap (USD)'
))

fig.update_layout(
    title="Bitcoin Market Cap Over Time",
    xaxis_title="Time",
    yaxis_title="Market Cap (USD)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Add a refresh button to update the data manually
if st.button("Refresh Data"):
    latest_data = fetch_latest_market_cap()
    if latest_data:
        df = df.append(latest_data, ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.experimental_rerun()
