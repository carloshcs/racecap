import requests
import pandas as pd
import time
from datetime import datetime

# Parameter: Number of top coins to fetch
NUMBER_OF_COINS = 50

# File path for storing data (Excel file)
excel_file = "crypto_market_cap_history.xlsx"

# CoinGecko API endpoints
COIN_MARKETS_ENDPOINT = "https://api.coingecko.com/api/v3/coins/markets"
COIN_MARKET_CHART_ENDPOINT = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

# Parameters for fetching market data
MARKET_PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": NUMBER_OF_COINS,
    "page": 1,
    "sparkline": "false"
}

# Fetch the top N coins by market capitalization from CoinGecko
response = requests.get(COIN_MARKETS_ENDPOINT, params=MARKET_PARAMS)
response.raise_for_status()

top_coins_data = response.json()

# Extract a list of coin IDs and names
top_coin_ids = [coin["id"] for coin in top_coins_data]
top_coin_names = {coin["id"]: coin["name"] for coin in top_coins_data}

# Initialize a list to store DataFrames for each coin
coin_data_frames = []

# Fetch historical market cap data for each of the top N coins
for coin_id in top_coin_ids:
    # Get the human-readable coin name
    coin_name = top_coin_names[coin_id]

    # Fetch historical market cap data
    try:
        parameters = {
            "vs_currency": "usd",
            "days": "365",      # Number of days to fetch
            "interval": "daily" # Fetch daily data
        }

        coin_chart_response = requests.get(COIN_MARKET_CHART_ENDPOINT.format(id=coin_id), params=parameters)
        coin_chart_response.raise_for_status()

        # Parse the JSON data from the response
        chart_data = coin_chart_response.json()

        # Check if 'market_caps' data is available and non-empty
        if 'market_caps' in chart_data and chart_data['market_caps']:
            timestamps = [entry[0] for entry in chart_data['market_caps']]
            market_caps = [entry[1] for entry in chart_data['market_caps']]

            # Create a DataFrame for this coin's market cap history
            df = pd.DataFrame({
                "Timestamp": pd.to_datetime(timestamps, unit='ms'),
                "Market Cap (USD)": market_caps,
                "Coin": coin_name
            })

            # Add this coin's DataFrame to the list
            coin_data_frames.append(df)
            print(f"Data collected for {coin_name}")
        else:
            print(f"Market cap data not found or empty for {coin_name}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {coin_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for {coin_name}: {req_err}")

    # Pause to respect API rate limits 
    time.sleep(15)  # Adjust as necessary

# Combine all coin DataFrames if any data was collected
if coin_data_frames:
    full_df = pd.concat(coin_data_frames, ignore_index=True)
    
    # Sort the DataFrame by Coin name and Timestamp for clarity
    full_df.sort_values(by=['Coin', 'Timestamp'], inplace=True)
    full_df.reset_index(drop=True, inplace=True)
    
    # Pivot the DataFrame so that each coin's market cap is in its own column
    pivot_df = full_df.pivot_table(
        index="Timestamp",
        columns="Coin",
        values="Market Cap (USD)"
    )

    # Sort columns by coin name
    pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

    # Save data to an Excel file
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        pivot_df.to_excel(writer, sheet_name="Market Cap Data")

    print(f"\nMarket cap data saved to {excel_file} in the sheet: 'Market Cap Data'")

    # Confirm the data collected for each coin
    coin_counts = full_df['Coin'].value_counts()
    print("\nData rows for each coin:")
    print(coin_counts)
else:
    print("No data was collected.")


# import requests
# import pandas as pd
# import time
# from datetime import datetime, timedelta

# # File path for storing data (Excel file for multiple sheets)
# excel_file = "crypto_market_cap_history.xlsx"

# # List of top 10 coins by market cap with their CoinGecko IDs
# top_10_coins = {
#     "bitcoin": "Bitcoin (BTC)",
#     "ethereum": "Ethereum (ETH)",
#     # "tether": "Tether (USDT)",
#     # "solana": "Solana (SOL)",
#     # "binancecoin": "BNB (BNB)",
#     # "dogecoin": "Dogecoin (DOGE)",
#     # "ripple": "XRP (XRP)",
#     # "usd-coin": "USD Coin (USDC)",
#     # "cardano": "Cardano (ADA)",
#     # "tron": "Tron (TRX)"
# }

# # Coin categories (for demonstration)
# coin_categories = {
#     "Bitcoin (BTC)": "Store of Value",
#     "Ethereum (ETH)": "Smart Contract Platform",
#     # "Tether (USDT)": "Stablecoin",
#     # "Solana (SOL)": "Smart Contract Platform",
#     # "BNB (BNB)": "Exchange Token",
#     # "Dogecoin (DOGE)": "Meme Coin",
#     # "XRP (XRP)": "Payment Coin",
#     # "USD Coin (USDC)": "Stablecoin",
#     # "Cardano (ADA)": "Smart Contract Platform",
#     # "Tron (TRX)": "Smart Contract Platform"
# }

# # Initialize a list to store DataFrames for each coin
# coin_data_frames = []

# # Fetch historical data for each coin
# for coin_id, coin_name in top_10_coins.items():
#     url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
#     parameters = {
#         "vs_currency": "usd",
#         "days": "365",
#         "interval": "daily"
#     }
    
#     try:
#         # Send a GET request to the CoinGecko API
#         response = requests.get(url, params=parameters)
#         response.raise_for_status()  # Raise HTTPError for non-2xx response statuses

#         # Parse the JSON data from the response
#         data = response.json()

#         # Check if 'market_caps' data is available and non-empty
#         if 'market_caps' in data and data['market_caps']:
#             timestamps = [entry[0] for entry in data['market_caps']]
#             market_caps = [entry[1] for entry in data['market_caps']]

#             # Create a DataFrame for this coin's market cap history
#             df = pd.DataFrame({
#                 "Timestamp": pd.to_datetime(timestamps, unit='ms'),
#                 "Market Cap (USD)": market_caps,
#                 "Coin": coin_name
#             })

#             # Add this coin's DataFrame to the list
#             coin_data_frames.append(df)
#             print(f"Data collected for {coin_name}")
#         else:
#             print(f"Market cap data not found or empty for {coin_name}")
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred for {coin_name}: {http_err}")
#     except requests.exceptions.RequestException as req_err:
#         print(f"Request error occurred for {coin_name}: {req_err}")

#     # Pause briefly to respect API rate limits (60 seconds recommended for safety)
#     time.sleep(60)

# # Combine all coin DataFrames if any data was collected
# if coin_data_frames:
#     full_df = pd.concat(coin_data_frames, ignore_index=True)
    
#     # Sort the DataFrame by Coin name and Timestamp for clarity
#     full_df.sort_values(by=['Coin', 'Timestamp'], inplace=True)
#     full_df.reset_index(drop=True, inplace=True)
    
#     # Pivot the DataFrame so that each coin's market cap is in its own column
#     pivot_df = full_df.pivot_table(
#         index="Timestamp",
#         columns="Coin",
#         values="Market Cap (USD)"
#     )
    
#     # Sort columns by coin name
#     pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)
    
#     # Create a DataFrame for coin categories
#     categories_df = pd.DataFrame(list(coin_categories.items()), columns=["Coin", "Category"])
#     categories_df.sort_values(by="Coin", inplace=True)

#     # Save data to an Excel file with multiple sheets
#     with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
#         pivot_df.to_excel(writer, sheet_name="Market Cap Data")
#         categories_df.to_excel(writer, sheet_name="Coin Categories", index=False)

#     print(f"\nMarket cap data saved to {excel_file} in two sheets: 'Market Cap Data' and 'Coin Categories'")

#     # Confirm the data collected for each coin
#     coin_counts = full_df['Coin'].value_counts()
#     print("\nData rows for each coin:")
#     print(coin_counts)
# else:
#     print("No data was collected.")
