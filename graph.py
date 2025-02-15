import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class StockGraphs:
    def __init__(self, df):
        self.df = df

    def calculate_indicators(self, df, short_window=12, long_window=26, signal_window=9, ma_window=200):
        """Calculates MACD, Signal Line, Histogram, and 200-day Moving Average."""
        df["EMA_12"] = df["Close"].ewm(span=short_window, adjust=False).mean()
        df["EMA_26"] = df["Close"].ewm(span=long_window, adjust=False).mean()
        df["MACD"] = df["EMA_12"] - df["EMA_26"]
        df["Signal_Line"] = df["MACD"].ewm(span=signal_window, adjust=False).mean()
        df["Histogram"] = df["MACD"] - df["Signal_Line"]
        df["MA_200"] = df["Close"].rolling(window=ma_window, min_periods=1).mean()
        return df

    def plot_graphs(self, selected_stock):
        """Generates and displays the stock price & MACD graphs."""
        df_stock = self.df[self.df["Symbol"] == selected_stock].sort_values(by="Date")
        df_stock = self.calculate_indicators(df_stock)

        # --- STOCK PRICE CHART ---
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["Close"], mode="lines", name="Stock Price", line=dict(color="blue")))
        fig_price.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["MA_200"], mode="lines", name="200-day MA", line=dict(color="orange", dash="dash"), opacity=0.8))
        fig_price.update_layout(title=f"{selected_stock} - Stock Price & 200-day Moving Average", xaxis_title="Date", yaxis_title="Stock Price", template="plotly_dark")

        # --- MACD INDICATOR CHART ---
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["MACD"], mode="lines", name="MACD Line", line=dict(color="red")))
        fig_macd.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["Signal_Line"], mode="lines", name="Signal Line", line=dict(color="green")))
        fig_macd.add_trace(go.Bar(x=df_stock["Date"], y=df_stock["Histogram"], name="MACD Histogram", marker_color=df_stock["Histogram"].apply(lambda x: "green" if x > 0 else "red")))
        fig_macd.add_trace(go.Scatter(x=df_stock["Date"], y=[0] * len(df_stock), mode="lines", name="Zero Line", line=dict(color="black", dash="dot")))
        fig_macd.update_layout(title=f"{selected_stock} - MACD Indicator", xaxis_title="Date", yaxis_title="MACD Value", template="plotly_dark")

        # Display both graphs in Streamlit
        st.plotly_chart(fig_price, use_container_width=True)
        st.plotly_chart(fig_macd, use_container_width=True)
