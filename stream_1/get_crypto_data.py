import requests
import pandas as pd
import time

# File path for storing data
excel_file = "crypto_market_cap_history.xlsx"
num_coins = 100  # Number of top coins to fetch, excluding stablecoins

# CoinGecko API endpoints
COINS_MARKET_ENDPOINT = "https://api.coingecko.com/api/v3/coins/markets"
COIN_MARKET_CHART_ENDPOINT = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

# List of excluded coins (BTC, ETH, USDT, USDC)
EXCLUDED_COINS = {"bitcoin", "ethereum", "tether", "usd-coin"}

# Function to fetch the top N coins by market cap excluding specified coins
def fetch_top_coins(n=num_coins):
    url = COINS_MARKET_ENDPOINT
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n * 2,  # Fetch more coins to account for exclusions
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    coins = [coin['id'] for coin in data if coin['id'] not in EXCLUDED_COINS]
    return coins[:n]  # Return only the requested number of coins

# Function to fetch historical market cap data for a specific coin
def fetch_historical_market_cap(coin_id, days=365):
    url = COIN_MARKET_CHART_ENDPOINT.format(id=coin_id)
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    if response.status_code == 429:
        print(f"Rate limit exceeded while fetching {coin_id}. Waiting for 60 seconds.")
        time.sleep(60)
        response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame({
        "Timestamp": pd.to_datetime([entry[0] for entry in data["market_caps"]], unit="ms"),
        f"{coin_id} Market Cap": [entry[1] for entry in data["market_caps"]]
    })

# Fetch historical market cap data for Bitcoin, Ethereum, USDT, and USDC
bitcoin_df = fetch_historical_market_cap("bitcoin")
ethereum_df = fetch_historical_market_cap("ethereum")
usdt_df = fetch_historical_market_cap("tether")
usdc_df = fetch_historical_market_cap("usd-coin")

# Rename columns for consistency
bitcoin_df.rename(columns={"bitcoin Market Cap": "Bitcoin Market Cap"}, inplace=True)
ethereum_df.rename(columns={"ethereum Market Cap": "Ethereum Market Cap"}, inplace=True)
usdt_df.rename(columns={"tether Market Cap": "USDT Market Cap"}, inplace=True)
usdc_df.rename(columns={"usd-coin Market Cap": "USDC Market Cap"}, inplace=True)

# Merge dataframes on the Timestamp column
final_df = bitcoin_df.merge(ethereum_df, on="Timestamp", how="outer")
final_df = final_df.merge(usdt_df, on="Timestamp", how="outer")
final_df = final_df.merge(usdc_df, on="Timestamp", how="outer")

# Fetch top altcoins (excluding BTC, ETH, USDT, USDC)
top_coins = fetch_top_coins()

# Initialize an empty DataFrame for altcoins
altcoins_df = pd.DataFrame()

# Fetch and merge altcoin data
for index, coin_id in enumerate(top_coins):
    print(f"Fetching data for {coin_id} ({index + 1}/{len(top_coins)})")
    coin_df = fetch_historical_market_cap(coin_id)
    if altcoins_df.empty:
        altcoins_df = coin_df
    else:
        altcoins_df = altcoins_df.merge(coin_df, on="Timestamp", how="outer")
    time.sleep(2)  # Add delay to avoid rate limits

# Fill missing values with zero in altcoin data
altcoins_df = altcoins_df.fillna(0)

# Calculate Altcoins Market Cap (excluding BTC, ETH, USDT, USDC)
altcoin_columns = [col for col in altcoins_df.columns if col not in {"Timestamp"}]
altcoins_df["Altcoins Market Cap"] = altcoins_df[altcoin_columns].sum(axis=1)

# Merge Altcoins Market Cap into the final DataFrame
final_df = final_df.merge(altcoins_df[["Timestamp", "Altcoins Market Cap"]], on="Timestamp", how="outer")

# Fill missing values with zero in the final DataFrame
final_df = final_df.fillna(0)

# Add total stablecoin market cap
final_df["Stablecoin Total Market Cap"] = final_df["USDT Market Cap"] + final_df["USDC Market Cap"]

# Calculate total market cap excluding stablecoins
final_df["Total Market Cap Excluding Stablecoins"] = (
    final_df["Bitcoin Market Cap"] +
    final_df["Ethereum Market Cap"] +
    final_df["Altcoins Market Cap"]
)

# Calculate Bitcoin and Ethereum dominance excluding stablecoins
final_df["Bitcoin Dominance (%)"] = (
    final_df["Bitcoin Market Cap"] / final_df["Total Market Cap Excluding Stablecoins"]
) * 100
final_df["Ethereum Dominance (%)"] = (
    final_df["Ethereum Market Cap"] / final_df["Total Market Cap Excluding Stablecoins"]
) * 100

# Sort the DataFrame by Timestamp
final_df.sort_values("Timestamp", inplace=True)

# Reset the index after sorting
final_df.reset_index(drop=True, inplace=True)

# Select and organize columns for the final Excel file
final_df = final_df[[
    "Timestamp", "Bitcoin Market Cap", "Ethereum Market Cap", "USDT Market Cap",
    "USDC Market Cap", "Stablecoin Total Market Cap", "Altcoins Market Cap",
    "Total Market Cap Excluding Stablecoins", "Bitcoin Dominance (%)", "Ethereum Dominance (%)"
]]

# Filter the DataFrame to include only rows with timestamps at midnight
final_df["Timestamp"] = pd.to_datetime(final_df["Timestamp"])  # Ensure Timestamp is in datetime format
final_df = final_df[final_df["Timestamp"].dt.time == pd.to_datetime("00:00:00").time()]

# Reset the index after filtering
final_df.reset_index(drop=True, inplace=True)

# Save to Excel
final_df.to_excel(excel_file, index=False)
print(f"Historical market cap data (midnight only) saved to {excel_file}")

