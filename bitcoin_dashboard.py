import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import os

# Set up Streamlit page configuration with an icon
st.set_page_config(
    page_title="Cryptocurrency Market Cap Dashboard",
    layout="wide",
    page_icon="icon.png"
)

# Load the external HTML file for the header
with open("header.html", "r") as f:
    header_html = f.read()

# Display the HTML header
components.html(header_html, height=80)

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


# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import os


    

# # The rest of your code remains unchanged...

# # Set up Streamlit page configuration
# st.set_page_config(page_title="Cryptocurrency Market Cap Dashboard", layout="wide")

# # File paths for data
# excel_file = "crypto_market_cap_history.xlsx"
# categories_file = "crypto_categories.xlsx"

# # Define a function to load market cap data from the Excel file
# def load_market_cap_data():
#     if os.path.exists(excel_file):
#         market_cap_df = pd.read_excel(excel_file, sheet_name="Market Cap Data")
#         if 'Timestamp' in market_cap_df.columns:
#             market_cap_df['Timestamp'] = pd.to_datetime(market_cap_df['Timestamp'])
#             # Melt the DataFrame from wide format to long format
#             melted_df = market_cap_df.melt(
#                 id_vars=["Timestamp"], 
#                 var_name="Coin", 
#                 value_name="Market Cap (USD)"
#             )
#             # Remove rows with no market cap data
#             melted_df.dropna(subset=["Market Cap (USD)"], inplace=True)
            
#             # Display the last update date
#             if not melted_df.empty:
#                 last_update_date = melted_df['Timestamp'].max()
#                 st.info(f"Last update on {last_update_date:%Y-%m-%d}")
            
#             return melted_df
#         else:
#             return pd.DataFrame()
#     else:
#         return pd.DataFrame(columns=["Timestamp", "Coin", "Market Cap (USD)"])

# # Define a function to load category data from the Excel file
# def load_category_data():
#     if os.path.exists(categories_file):
#         categories_df = pd.read_excel(categories_file)
#         # Ensure the columns are named as expected
#         if "Coin" in categories_df.columns and "Category" in categories_df.columns:
#             return categories_df
#         else:
#             return pd.DataFrame(columns=["Coin", "Category"])
#     else:
#         return pd.DataFrame(columns=["Coin", "Category"])

# # Load market cap data and categories data
# market_cap_df = load_market_cap_data()
# categories_df = load_category_data()

# # Merge market cap data with categories if both are available
# if not market_cap_df.empty and not categories_df.empty:
#     market_cap_df = pd.merge(market_cap_df, categories_df, on="Coin", how="left")
#     market_cap_df["Category"].fillna("Top 50 Coins", inplace=True)
# else:
#     market_cap_df["Category"] = "Top 50 Coins"

# # Filter to only show the top 50 coins by latest market cap
# latest_data = market_cap_df.groupby('Coin').apply(lambda x: x.iloc[-1])
# top_50_coins = latest_data.nlargest(50, 'Market Cap (USD)')['Coin'].tolist()
# filtered_df = market_cap_df[market_cap_df['Coin'].isin(top_50_coins)]

# # Title of the dashboard
# st.title("Cryptocurrency Market Cap Dashboard")

# # Display a warning if no data is loaded
# if filtered_df.empty:
#     st.warning("No data available. Please ensure the data files exist and contain valid data.")
#     st.stop()

# # Sidebar filters
# st.sidebar.header("Filters and Settings")

# # Top 10 coins filter checkbox
# show_top_10 = st.sidebar.checkbox(
#     "Show Top 10 Coins by Market Cap",
#     value=False,
#     help="Check this box to filter the chart to only display the top 10 coins by market cap."
# )

# # Apply top 10 filter if selected
# if show_top_10:
#     # Filter to show only the top 10 coins by market cap
#     top_10_coins = latest_data.nlargest(10, 'Market Cap (USD)')['Coin'].tolist()
#     filtered_df = filtered_df[filtered_df['Coin'].isin(top_10_coins)]

# # Filter by category within the top 50, with categories hidden by default
# available_categories = sorted(filtered_df['Category'].dropna().unique().tolist())
# with st.sidebar.expander("Select categories to display", expanded=False):
#     selected_categories = st.multiselect(
#         "Choose Categories",
#         options=available_categories,
#         default=available_categories,
#         help="Filter cryptocurrencies by category.",
#         label_visibility="collapsed"
#     )
# filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

# # Filter by coin within the top 50
# available_coins = sorted(filtered_df['Coin'].unique().tolist())
# with st.sidebar.expander("Select coins to display", expanded=False):
#     selected_coins = st.multiselect(
#         "Choose Coins",
#         options=available_coins,
#         default=available_coins,
#         help="Choose which cryptocurrency market caps to visualize on the chart.",
#         label_visibility="collapsed"
#     )

# # If no coins selected, inform the user
# if not selected_coins:
#     st.warning("No data to display. Please select at least one coin.")
#     st.stop()

# # Filter data based on selected coins
# filtered_df = filtered_df[filtered_df['Coin'].isin(selected_coins)]

# # Determine the latest market cap for each coin to order them in the chart
# latest_data = filtered_df.groupby('Coin').apply(lambda x: x.iloc[-1])
# latest_data.sort_values(by='Market Cap (USD)', ascending=False, inplace=True)
# ordered_coins = latest_data.index.tolist()

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

# # Create the Plotly figure
# fig = go.Figure()

# # Plot data for each selected coin, ordered by their latest market cap (descending)
# for i, coin in enumerate(ordered_coins, start=1):
#     if coin in selected_coins:
#         coin_data = filtered_df[filtered_df['Coin'] == coin].sort_values(by="Timestamp")
#         fig.add_trace(
#             go.Scatter(
#                 x=coin_data['Timestamp'],
#                 y=coin_data['Market Cap (USD)'],
#                 mode='lines+markers',
#                 name=f"#{i} {coin}"
#             )
#         )

# # Update layout with logarithmic Y-axis scale and user-adjustable chart size
# fig.update_layout(
#     title="Cryptocurrency Market Cap Over Time (Log Scale)",
#     xaxis_title="<b>Date</b>",
#     yaxis_title="<b>Market Cap (USD)</b>",
#     xaxis=dict(
#         title_font=dict(size=16, color='black')
#     ),
#     yaxis=dict(
#         title_font=dict(size=16, color='black'),
#         type="log"  # Apply logarithmic scale to the Y-axis
#     ),
#     height=vertical_size,
#     width=horizontal_size,
#     template="plotly_white",
#     legend_title="Coin (Ordered by Market Cap)"
# )

# # Display the chart on the main page without the subtitle list of coins
# st.plotly_chart(fig, use_container_width=(horizontal_size == 2000))


