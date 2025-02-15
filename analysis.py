import streamlit as st
import yfinance as yf
import pandas as pd

class AnalysisData:
    def __init__(self):
        """Initialize the stock data analysis module."""
        self.stock_symbols = [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
            "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS",
            "LT.NS", "KOTAKBANK.NS", "AXISBANK.NS", "ASIANPAINT.NS", "BAJFINANCE.NS",
            "MARUTI.NS", "ULTRACEMCO.NS", "TITAN.NS", "SUNPHARMA.NS", "TATASTEEL.NS",
            "WIPRO.NS", "ONGC.NS", "COALINDIA.NS", "NTPC.NS", "POWERGRID.NS",
            "INDUSINDBK.NS", "BAJAJFINSV.NS", "ADANIENT.NS", "GRASIM.NS", "JSWSTEEL.NS",
            "HCLTECH.NS", "TECHM.NS", "NESTLEIND.NS", "CIPLA.NS", "BPCL.NS", "DRREDDY.NS",
            "HDFCLIFE.NS", "BRITANNIA.NS", "DIVISLAB.NS", "SBILIFE.NS", "HEROMOTOCO.NS",
            "BAJAJ-AUTO.NS", "TATAMOTORS.NS", "UPL.NS", "APOLLOHOSP.NS", "ADANIPORTS.NS",
            "M&M.NS", "HINDALCO.NS", "TATACONSUM.NS", "AAPL", "MSFT", "GOOGL", "AMZN",
            "TSLA", "META", "NVDA", "NFLX", "ADBE", "IBM"
        ]

    def display_analysis(self):
        """Displays stock data analysis on the Streamlit app."""
        st.markdown("<h1>📈 Stock Data Dashboard</h1>", unsafe_allow_html=True)

        # Sidebar dropdown for stock selection
        selected_stock = st.sidebar.selectbox("🔍 Select a Stock:", self.stock_symbols)

        # Fetch stock data
        st.subheader(f"Historical Data for {selected_stock}")
        stock = yf.Ticker(selected_stock)
        data = stock.history(period="1mo")
        data.reset_index(inplace=True)
        st.write(data)

        # Display price trend
        st.subheader("📊 Price Trend (Last 1 Month)")
        st.line_chart(data.set_index("Date")["Close"])

        # Fetch and display current stock prices
        st.subheader("📊 Current Stock Prices")
        current_prices = {
            symbol: yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
            for symbol in self.stock_symbols
        }
        current_prices_df = pd.DataFrame(list(current_prices.items()), columns=['Symbol', 'Current Price'])
        st.write(current_prices_df)

        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()
