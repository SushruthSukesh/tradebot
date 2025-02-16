import os
import pandas as pd
import unicodedata
import yfinance as yf
import streamlit as st
import nltk  
from nltk.sentiment.vader import SentimentIntensityAnalyzer  

# ✅ Download VADER lexicon if not available
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self, tweet_file='stock_tweets.csv'):
        """Initialize the Sentiment Analyzer with a tweet dataset."""
        self.tweet_file = tweet_file
        self.sent_df = None
        self.stock_symbols = ["TSLA", "MSFT", "PG", "META", "AMZN", "GOOG", "AAPL", "AMD", "NFLX",
                              "TSM", "KOF", "PYPL", "NOC", "BX", "BA", "INTC", "CRM", "NU", "DTS",
                              "COST", "ENPH", "NIO", "ZS", "XPEV"]
        self.current_prices = {}
        self.combined_df = None  # Store final data

    def load_tweets(self):
        """Load tweets dataset and ensure required columns exist."""
        if not os.path.exists(self.tweet_file):
            st.error(f"Error: File not found at {self.tweet_file}. Please check the path.")
            st.stop()
        else:
            self.sent_df = pd.read_csv(self.tweet_file)

        # ✅ Rename "Stock Name" to "Stock Symbol" (Fixing Missing Column Issue)
        if "Stock Name" in self.sent_df.columns:
            self.sent_df.rename(columns={"Stock Name": "Stock Symbol"}, inplace=True)

        # ✅ Ensure required columns exist
        required_columns = {"Tweet", "Stock Symbol"}
        if not required_columns.issubset(self.sent_df.columns):
            st.error("Error: Required columns missing. Expected columns: 'Tweet', 'Stock Symbol'.")
            st.stop()

        # ✅ Add sentiment score columns
        self.sent_df["sentiment_score"] = 0.0
        self.sent_df["Negative"] = 0.0
        self.sent_df["Neutral"] = 0.0
        self.sent_df["Positive"] = 0.0

    def analyze_sentiment(self):
        """Perform sentiment analysis on tweets."""
        if self.sent_df is None:
            st.error("Tweet dataset not loaded.")
            return

        sia = SentimentIntensityAnalyzer()

        for index, row in self.sent_df.iterrows():
            try:
                sentence_i = unicodedata.normalize('NFKD', row['Tweet'])
                sentence_sentiment = sia.polarity_scores(sentence_i)
                self.sent_df.at[index, 'sentiment_score'] = sentence_sentiment['compound']
                self.sent_df.at[index, 'Negative'] = sentence_sentiment['neg']
                self.sent_df.at[index, 'Neutral'] = sentence_sentiment['neu']
                self.sent_df.at[index, 'Positive'] = sentence_sentiment['pos']
            except TypeError:
                print(f"Error processing tweet at index {index}")
                break

    def fetch_stock_prices(self):
        """Fetch current stock prices from Yahoo Finance."""
        for symbol in self.stock_symbols:
            try:
                stock = yf.Ticker(symbol)
                data = stock.history(period="1d")
                if not data.empty:
                    self.current_prices[symbol] = data["Close"].iloc[-1]
                else:
                    self.current_prices[symbol] = None
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                self.current_prices[symbol] = None

    def compute_sentiment_scores(self):
        """Compute and merge sentiment scores with stock prices."""
        if self.sent_df is None:
            st.error("Sentiment data not available.")
            return

        # ✅ Ensure grouping by stock symbol
        avg_sentiment = self.sent_df.groupby('Stock Symbol', as_index=False)['sentiment_score'].mean()

        # ✅ Ensure current prices are in a DataFrame
        current_prices_df = pd.DataFrame(self.current_prices.items(), columns=['Stock Symbol', 'Current Price'])

        # ✅ Merge with stock prices
        self.combined_df = pd.merge(current_prices_df, avg_sentiment, on='Stock Symbol', how='inner')

        # ✅ Save to CSV
        self.combined_df.to_csv('combined_stock_data.csv', index=False)

    def display_results(self):
        """Display stock prices and exact sentiment scores in Streamlit."""
        if self.combined_df is not None and not self.combined_df.empty:
            st.subheader("📊 Stock Prices and Sentiment Scores")
            st.dataframe(self.combined_df)

            for _, row in self.combined_df.iterrows():
                symbol = row['Stock Symbol']
                sentiment = row['sentiment_score']
                st.markdown(f"✅ **{symbol} Sentiment Score:** {sentiment:.4f}")

        else:
            st.error("No data available for display. Run sentiment analysis first.")
