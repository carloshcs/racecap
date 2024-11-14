

#####################################



# import requests
# import pandas as pd
# from datetime import datetime

# # File path for storing data
# csv_file = "crypto_market_cap_history.csv"

# # List of top 10 coins by market cap with their CoinGecko IDs
# top_10_coins = {
#     "bitcoin": "Bitcoin (BTC)",
#     "ethereum": "Ethereum (ETH)",
#     "tether": "Tether (USDT)",
#     "solana": "Solana (SOL)",
#     "binancecoin": "BNB (BNB)",
#     "dogecoin": "Dogecoin (DOGE)",
#     "ripple": "XRP (XRP)",
#     "usd-coin": "USD Coin (USDC)",
#     "cardano": "Cardano (ADA)",
#     "tron": "Tron (TRX)"
# }

# # Fetch historical data from CoinGecko for each coin and save to a single CSV
# full_df = pd.DataFrame()

# for coin_id, coin_name in top_10_coins.items():
#     url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
#     parameters = {
#         "vs_currency": "usd",
#         "days": "365",
#         "interval": "daily"
#     }
#     response = requests.get(url, params=parameters)
#     data = response.json()

#     # Check if the 'market_caps' data exists
#     if 'market_caps' in data:
#         timestamps = [entry[0] for entry in data['market_caps']]
#         market_caps = [entry[1] for entry in data['market_caps']]
#         df = pd.DataFrame({
#             "Timestamp": pd.to_datetime(timestamps, unit='ms'),
#             "Market Cap (USD)": market_caps,
#             "Coin": coin_name
#         })
#         full_df = pd.concat([full_df, df], ignore_index=True)
#     else:
#         print(f"Failed to fetch data for {coin_name}")

# # Save the combined data for all 10 coins to a CSV
# full_df.to_csv(csv_file, index=False)
# print(f"Data for top 10 cryptocurrencies saved to {csv_file}")


# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import os

# # Set up Streamlit page configuration
# st.set_page_config(page_title="Cryptocurrency Market Cap Dashboard", layout="wide")

# # File path for storing data
# csv_file = "crypto_market_cap_history.csv"

# # List of top 10 coins by market cap for filtering (names displayed on the chart)
# top_10_coins = {
#     "bitcoin": "Bitcoin (BTC)",
#     "ethereum": "Ethereum (ETH)",
#     "tether": "Tether (USDT)",
#     "solana": "Solana (SOL)",
#     # "binancecoin": "BNB (BNB)",
#     # "dogecoin": "Dogecoin (DOGE)",
#     # "ripple": "XRP (XRP)",
#     # "usd-coin": "USD Coin (USDC)",
#     # "cardano": "Cardano (ADA)",
#     # "tron": "Tron (TRX)"
# }

# # Define a function to load or display a warning if the CSV is missing
# def load_csv_data():
#     if os.path.exists(csv_file):
#         st.info("Using existing data from CSV file.")
#         df_data = pd.read_csv(csv_file)
#         return df_data
#     else:
#         st.warning("The CSV file does not exist in the directory.")
#         return pd.DataFrame(columns=["Timestamp", "Market Cap (USD)", "Coin"])

# # Load data from CSV and ensure proper datetime format
# df = load_csv_data()
# if not df.empty:
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'])
#     df.sort_values(by=['Coin', 'Timestamp'], inplace=True)
#     df.reset_index(drop=True, inplace=True)

# # Title of the dashboard
# st.title("Cryptocurrency Market Cap Dashboard")

# # Display a warning if no data is loaded
# if df.empty:
#     st.warning("No data available. Please ensure 'crypto_market_cap_history.csv' is in the working directory and contains valid data.")
#     st.stop()

# # Select coins to display on the chart using a multi-select box
# available_coins = df['Coin'].unique().tolist()
# selected_coins = st.multiselect(
#     "Select coins to display on chart:", 
#     options=available_coins, 
#     default=available_coins,
#     help="Choose which cryptocurrency market caps to visualize on the chart."
# )

# # Filter data based on selected coins
# filtered_df = df[df['Coin'].isin(selected_coins)]

# # If no coins selected, inform the user
# if filtered_df.empty:
#     st.warning("No data to display. Please select at least one coin.")
#     st.stop()

# # User-adjustable chart dimensions
# st.sidebar.header("Adjust Chart Dimensions")
# vertical_size = st.sidebar.slider(
#     "Chart Height (pixels)", 
#     min_value=400, 
#     max_value=1200, 
#     value=800, 
#     step=50, 
#     help="Adjust the height of the chart."
# )
# horizontal_size = st.sidebar.slider(
#     "Chart Width (pixels)", 
#     min_value=400, 
#     max_value=2000, 
#     value=1200, 
#     step=100, 
#     help="Adjust the width of the chart."
# )

# # Plot the data using Plotly
# fig = go.Figure()

# for coin in selected_coins:
#     coin_data = filtered_df[filtered_df['Coin'] == coin]
#     fig.add_trace(
#         go.Scatter(
#             x=coin_data['Timestamp'],
#             y=coin_data['Market Cap (USD)'],
#             mode='lines+markers',
#             name=coin
#         )
#     )

# # Update layout with logarithmic Y-axis scale and user-adjustable chart size
# fig.update_layout(
#     title="Cryptocurrency Market Cap Over Time (Log Scale)",
#     xaxis_title="Date",
#     yaxis_title="Market Cap (USD)",
#     yaxis_type="log",  # Apply logarithmic scale to the Y-axis
#     height=vertical_size,
#     width=horizontal_size,
#     template="plotly_white"
# )

# # Display the chart on the main page
# st.plotly_chart(fig, use_container_width=(horizontal_size == 2000))


# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import os

# # Set up Streamlit page configuration
# st.set_page_config(page_title="Cryptocurrency Market Cap Dashboard", layout="wide")

# # File paths for data
# excel_file = "crypto_market_cap_history.xlsx"
# categories_file = "crypto_categories.xlsx"

# # Define a function to load market cap data from the Excel file
# def load_market_cap_data():
#     if os.path.exists(excel_file):
#         st.info("Using existing data from the Excel file.")
#         market_cap_df = pd.read_excel(excel_file, sheet_name="Market Cap Data")
#         # Ensure the Timestamp column is of datetime type
#         if 'Timestamp' in market_cap_df.columns:
#             market_cap_df['Timestamp'] = pd.to_datetime(market_cap_df['Timestamp'])
#             # Melt the DataFrame from wide format to long format
#             market_cap_df = market_cap_df.melt(id_vars=["Timestamp"], var_name="Coin", value_name="Market Cap (USD)")
#         else:
#             st.warning("No 'Timestamp' column found in 'Market Cap Data' sheet. Please ensure the data is in the correct format.")
#             return pd.DataFrame()
#         return market_cap_df
#     else:
#         st.warning("The Excel file does not exist in the directory.")
#         return pd.DataFrame(columns=["Timestamp", "Coin", "Market Cap (USD)"])

# # Define a function to load category data from the Excel file
# def load_category_data():
#     if os.path.exists(categories_file):
#         categories_df = pd.read_excel(categories_file)
#         # Ensure that the columns are named as expected
#         if "Coin" in categories_df.columns and "Category" in categories_df.columns:
#             return categories_df
#         else:
#             st.warning("The categories file does not have the required 'Coin' and 'Category' columns.")
#             return pd.DataFrame(columns=["Coin", "Category"])
#     else:
#         st.warning("The categories Excel file does not exist in the directory.")
#         return pd.DataFrame(columns=["Coin", "Category"])

# # Load market cap data and categories data
# market_cap_df = load_market_cap_data()
# categories_df = load_category_data()

# # Merge market cap data with categories
# if not market_cap_df.empty and not categories_df.empty:
#     market_cap_df = pd.merge(market_cap_df, categories_df, on="Coin", how="left")

# # Title of the dashboard
# st.title("Cryptocurrency Market Cap Dashboard")

# # Display a warning if no data is loaded
# if market_cap_df.empty:
#     st.warning("No data available. Please ensure the data files exist and contain valid data.")
#     st.stop()

# # Sidebar filters
# st.sidebar.header("Filters and Settings")

# # Filter by category
# if "Category" in market_cap_df.columns and market_cap_df["Category"].notna().any():
#     available_categories = market_cap_df['Category'].dropna().unique().tolist()
#     selected_categories = st.sidebar.multiselect(
#         "Select categories to display:",
#         options=available_categories,
#         default=available_categories,
#         help="Filter cryptocurrencies by category."
#     )
#     # Filter data based on selected categories
#     filtered_df = market_cap_df[market_cap_df['Category'].isin(selected_categories)]
# else:
#     filtered_df = market_cap_df
#     st.warning("No category data available. All coins will be displayed.")

# # Filter by coin based on filtered categories
# if not filtered_df.empty:
#     available_coins = filtered_df['Coin'].unique().tolist()
#     selected_coins = st.sidebar.multiselect(
#         "Select coins to display:",
#         options=available_coins,
#         default=available_coins,
#         help="Choose which cryptocurrency market caps to visualize on the chart."
#     )
# else:
#     selected_coins = []
#     st.warning("No coins available after applying category filters.")

# # If no coins selected, inform the user
# if not selected_coins:
#     st.warning("No data to display. Please select at least one coin.")
#     st.stop()

# # Filter data based on selected coins
# filtered_df = filtered_df[filtered_df['Coin'].isin(selected_coins)]

# # User-adjustable chart dimensions
# vertical_size = st.sidebar.slider(
#     "Chart Height (pixels)",
#     min_value=400,
#     max_value=1200,
#     value=800,
#     step=50,
#     help="Adjust the height of the chart."
# )
# horizontal_size = st.sidebar.slider(
#     "Chart Width (pixels)",
#     min_value=400,
#     max_value=2000,
#     value=1200,
#     step=100,
#     help="Adjust the width of the chart."
# )

# # Create a section in the main area for market cap chart
# st.subheader("Market Cap Top 50 Coins")

# # Plot the data using Plotly
# fig = go.Figure()

# if not filtered_df.empty:
#     # Group data by coin and plot each coin's market cap over time
#     for coin in selected_coins:
#         coin_data = filtered_df[filtered_df['Coin'] == coin]
#         fig.add_trace(
#             go.Scatter(
#                 x=coin_data['Timestamp'],
#                 y=coin_data['Market Cap (USD)'],
#                 mode='lines+markers',
#                 name=coin
#             )
#         )

#     # Update layout with logarithmic Y-axis scale and user-adjustable chart size
#     fig.update_layout(
#         title="Cryptocurrency Market Cap Over Time (Log Scale)",
#         xaxis_title="Date",
#         yaxis_title="Market Cap (USD)",
#         yaxis_type="log",  # Apply logarithmic scale to the Y-axis
#         height=vertical_size,
#         width=horizontal_size,
#         template="plotly_white"
#     )

#     # Display the chart on the main page
#     st.plotly_chart(fig, use_container_width=(horizontal_size == 2000))
# else:
#     st.warning("No data available after applying filters.")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Set up Streamlit page configuration
st.set_page_config(page_title="Cryptocurrency Market Cap Dashboard", layout="wide")

# File paths for data
excel_file = "crypto_market_cap_history.xlsx"
categories_file = "crypto_categories.xlsx"

# Define a function to load market cap data from the Excel file
def load_market_cap_data():
    if os.path.exists(excel_file):
        market_cap_df = pd.read_excel(excel_file, sheet_name="Market Cap Data")
        if 'Timestamp' in market_cap_df.columns:
            market_cap_df['Timestamp'] = pd.to_datetime(market_cap_df['Timestamp'])
            # Melt the DataFrame from wide format to long format
            melted_df = market_cap_df.melt(
                id_vars=["Timestamp"], 
                var_name="Coin", 
                value_name="Market Cap (USD)"
            )
            # Remove rows with no market cap data
            melted_df.dropna(subset=["Market Cap (USD)"], inplace=True)
            
            # Display the last update date
            if not melted_df.empty:
                last_update_date = melted_df['Timestamp'].max()
                st.info(f"Last update on {last_update_date:%Y-%m-%d}")
            
            return melted_df
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame(columns=["Timestamp", "Coin", "Market Cap (USD)"])

# Define a function to load category data from the Excel file
def load_category_data():
    if os.path.exists(categories_file):
        categories_df = pd.read_excel(categories_file)
        # Ensure the columns are named as expected
        if "Coin" in categories_df.columns and "Category" in categories_df.columns:
            return categories_df
        else:
            return pd.DataFrame(columns=["Coin", "Category"])
    else:
        return pd.DataFrame(columns=["Coin", "Category"])

# Load market cap data and categories data
market_cap_df = load_market_cap_data()
categories_df = load_category_data()

# Merge market cap data with categories if both are available
if not market_cap_df.empty and not categories_df.empty:
    market_cap_df = pd.merge(market_cap_df, categories_df, on="Coin", how="left")
    market_cap_df["Category"].fillna("Top 50 Coins", inplace=True)
else:
    market_cap_df["Category"] = "Top 50 Coins"

# Filter to only show the top 50 coins by latest market cap
latest_data = market_cap_df.groupby('Coin').apply(lambda x: x.iloc[-1])
top_50_coins = latest_data.nlargest(50, 'Market Cap (USD)')['Coin'].tolist()
filtered_df = market_cap_df[market_cap_df['Coin'].isin(top_50_coins)]

# Title of the dashboard
st.title("Cryptocurrency Market Cap Dashboard")

# Display a warning if no data is loaded
if filtered_df.empty:
    st.warning("No data available. Please ensure the data files exist and contain valid data.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters and Settings")

# Top 10 coins filter checkbox
show_top_10 = st.sidebar.checkbox(
    "Show Top 10 Coins by Market Cap",
    value=False,
    help="Check this box to filter the chart to only display the top 10 coins by market cap."
)

# Apply top 10 filter if selected
if show_top_10:
    # Filter to show only the top 10 coins by market cap
    top_10_coins = latest_data.nlargest(10, 'Market Cap (USD)')['Coin'].tolist()
    filtered_df = filtered_df[filtered_df['Coin'].isin(top_10_coins)]

# Filter by category within the top 50, with categories hidden by default
available_categories = sorted(filtered_df['Category'].dropna().unique().tolist())
with st.sidebar.expander("Select categories to display", expanded=False):
    selected_categories = st.multiselect(
        "Choose Categories",
        options=available_categories,
        default=available_categories,
        help="Filter cryptocurrencies by category.",
        label_visibility="collapsed"
    )
filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

# Filter by coin within the top 50
available_coins = sorted(filtered_df['Coin'].unique().tolist())
with st.sidebar.expander("Select coins to display", expanded=False):
    selected_coins = st.multiselect(
        "Choose Coins",
        options=available_coins,
        default=available_coins,
        help="Choose which cryptocurrency market caps to visualize on the chart.",
        label_visibility="collapsed"
    )

# If no coins selected, inform the user
if not selected_coins:
    st.warning("No data to display. Please select at least one coin.")
    st.stop()

# Filter data based on selected coins
filtered_df = filtered_df[filtered_df['Coin'].isin(selected_coins)]

# Determine the latest market cap for each coin to order them in the chart
latest_data = filtered_df.groupby('Coin').apply(lambda x: x.iloc[-1])
latest_data.sort_values(by='Market Cap (USD)', ascending=False, inplace=True)
ordered_coins = latest_data.index.tolist()

# User-adjustable chart dimensions
vertical_size = st.sidebar.slider(
    "Chart Height (pixels)",
    min_value=400,
    max_value=1200,
    value=800,
    step=50,
    help="Adjust the height of the chart."
)
horizontal_size = st.sidebar.slider(
    "Chart Width (pixels)",
    min_value=400,
    max_value=2000,
    value=1200,
    step=100,
    help="Adjust the width of the chart."
)

# Create the Plotly figure
fig = go.Figure()

# Plot data for each selected coin, ordered by their latest market cap (descending)
for i, coin in enumerate(ordered_coins, start=1):
    if coin in selected_coins:
        coin_data = filtered_df[filtered_df['Coin'] == coin].sort_values(by="Timestamp")
        fig.add_trace(
            go.Scatter(
                x=coin_data['Timestamp'],
                y=coin_data['Market Cap (USD)'],
                mode='lines+markers',
                name=f"#{i} {coin}"
            )
        )

# Update layout with logarithmic Y-axis scale and user-adjustable chart size
fig.update_layout(
    title="Cryptocurrency Market Cap Over Time (Log Scale)",
    xaxis_title="<b>Date</b>",
    yaxis_title="<b>Market Cap (USD)</b>",
    xaxis=dict(
        title_font=dict(size=16, color='black')
    ),
    yaxis=dict(
        title_font=dict(size=16, color='black'),
        type="log"  # Apply logarithmic scale to the Y-axis
    ),
    height=vertical_size,
    width=horizontal_size,
    template="plotly_white",
    legend_title="Coin (Ordered by Market Cap)"
)

# Display the chart on the main page without the subtitle list of coins
st.plotly_chart(fig, use_container_width=(horizontal_size == 2000))


