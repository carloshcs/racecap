import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set up Streamlit page configuration with an icon
st.set_page_config(
    page_title="Stable Coin Coverage Dashboard",
    layout="wide",
    page_icon="icon.png"
)

# Load Excel data
excel_file = "crypto_market_cap_history.xlsx"

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

data = load_data(excel_file)

# Ensure Timestamp column is datetime
data["Timestamp"] = pd.to_datetime(data["Timestamp"])

# Add filter options on top of the chart
st.header("Cryptocurrency Market Cap Dashboard")
filter_option = st.radio(
    "Select Date Range:",
    options=["Last 7 Days", "Last 1 Month", "Last 3 Months", "All Time"],
    index=3,
    horizontal=True
)

# Determine the date range for filtering
today = datetime.now()
if filter_option == "Last 7 Days":
    start_date = today - timedelta(days=7)
elif filter_option == "Last 1 Month":
    start_date = today - timedelta(days=30)
elif filter_option == "Last 3 Months":
    start_date = today - timedelta(days=90)
else:
    start_date = data["Timestamp"].min()

# Filter the data based on the selected date range
filtered_data = data[data["Timestamp"] >= start_date]

# Perform stablecoin backup calculations (corrected to show percentage correctly)
filtered_data["Stablecoin Backup (Bitcoin)"] = (
    filtered_data["Stablecoin Total Market Cap"] / filtered_data["Bitcoin Market Cap"] * 100
)
filtered_data["Stablecoin Backup (Altcoins + Ethereum)"] = (
    filtered_data["Stablecoin Total Market Cap"] /
    (filtered_data["Ethereum Market Cap"] + filtered_data["Altcoins Market Cap"]) * 100
)
filtered_data["Stablecoin Backup (Bitcoin + Altcoins + Ethereum)"] = (
    filtered_data["Stablecoin Total Market Cap"] /
    (filtered_data["Bitcoin Market Cap"] + filtered_data["Ethereum Market Cap"] + filtered_data["Altcoins Market Cap"]) * 100
)

# Create the chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered_data["Timestamp"],
    y=filtered_data["Stablecoin Backup (Bitcoin)"],
    mode='lines',
    name="Stable/BTC",
    line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=filtered_data["Timestamp"],
    y=filtered_data["Stablecoin Backup (Altcoins + Ethereum)"],
    mode='lines',
    name="Stable/(Altcoins + Ethereum)",
    line=dict(color='red')
))
fig.add_trace(go.Scatter(
    x=filtered_data["Timestamp"],
    y=filtered_data["Stablecoin Backup (Bitcoin + Altcoins + Ethereum)"],
    mode='lines',
    name="Stable/Total",
    line=dict(color='green')
))

# Update layout
fig.update_layout(
    title=f"Marketcap Stablecoin to Bitcoin or Altcoin Ratios ({filter_option})",
    xaxis_title="Date",
    yaxis_title="Stablecoin Coverage (%)",
    xaxis=dict(title_font=dict(size=16, color='black')),
    yaxis=dict(title_font=dict(size=16, color='black')),
    height=600,
    width=1200,
    template="plotly_white"
)

# Display chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Display explanation below the chart
st.markdown("""
### Explanation for the Chart

This chart highlights the role of stablecoins (e.g., USDT, USDC) in providing liquidity to the cryptocurrency market. Stablecoins are crucial as they act as a buffer between fiat currencies and crypto investments.

The ratios show how much stablecoin liquidity backs different segments of the market:
1. **Stable/BTC** - Stablecoin liquidity compared to Bitcoin’s market cap.
2. **Stable/(Altcoins + Ethereum)** - Liquidity backing altcoins and Ethereum.
3. **Stable/Total** - Overall stablecoin backing across Bitcoin, Ethereum, and altcoins.

### What the Chart Shows:
- **Higher Ratios:** Indicate more stablecoins available to cover exits, suggesting a safer liquidity cushion for market positions.
- **Lower Ratios:** Suggest less liquidity, potentially signaling tighter conditions for large market exits.
- Only consideres the top 100 altcoins

This data helps assess market stability and liquidity trends.
""")

# Add last updated note
last_date = data["Timestamp"].max().strftime("%Y-%m-%d")
st.info(f"**Note:** Chart last updated on {last_date}.")

# Add donation message below
st.markdown("""
### Support This Website

If you like the content, you can help by donating any amount (e.g., $0.01) to improve this website and motivate its development:

- **Solana:** `ApAVasEykd9g26YpwjaHKZRUGrjKBVwTarPRptBqbnub`
- **Bitcoin:** `bc1qhumnm6fdasatvtnelgv6an97nrvg25uxl29fqh`
- **Ethereum:** `0x14effaF60778faBF31Ae3D69BD27a520c1dD8bb8`
- **Base:** `0x14effaF60778faBF31Ae3D69BD27a520c1dD8bb8`
""")
