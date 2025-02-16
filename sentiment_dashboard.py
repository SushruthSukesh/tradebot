import streamlit as st
import pandas as pd

class SentimentDashboard:
    def __init__(self, csv_file="combined_stock_data.csv"):
        """Initialize the sentiment dashboard with the given dataset."""
        self.csv_file = csv_file
        self.df = None  # Placeholder for the dataframe

    def load_data(self):
        """Load the sentiment data and process decisions."""
        try:
            self.df = pd.read_csv(self.csv_file)

            # ✅ Decision Logic (Buy/Sell/Hold)
            def get_decision(sentiment_score):
                if sentiment_score > 0.2:
                    return "BUY ✅"
                elif sentiment_score < -0.2:
                    return "SELL ❌"
                else:
                    return "HOLD ⏸️"

            # ✅ Apply Decision
            self.df["Decision"] = self.df["sentiment_score"].apply(get_decision)

        except FileNotFoundError:
            st.error(f"Error: The sentiment data file '{self.csv_file}' was not found. Please run sentiment analysis first.")

    def display_dashboard(self):
        """Render the sentiment analysis results in Streamlit."""
        if self.df is None:
            st.error("❌ No data available for sentiment analysis.")
            return
        
        st.markdown("<h1>📊 AI-Powered Stock Sentiment Analyzer</h1>", unsafe_allow_html=True)

        # ✅ Display Data with Color Coding
        st.subheader("📑 Sentiment-Based Stock Recommendations")
        st.dataframe(self.df.style.applymap(
            lambda x: "background-color: lightgreen" if x == "BUY ✅" else 
                      "background-color: salmon" if x == "SELL ❌" else 
                      "background-color: #ADD8E6" if x == "HOLD ⏸️" else "",  # Light Blue for HOLD
            subset=["Decision"]
        ))

        # ✅ Investment Summary
        buy_stocks = self.df[self.df["Decision"] == "BUY ✅"]
        sell_stocks = self.df[self.df["Decision"] == "SELL ❌"]

        st.markdown("### 📌 Investment Recommendations:")
        st.success(f"💰 **Stocks to BUY:** {', '.join(buy_stocks['Stock Symbol'].tolist())}" if not buy_stocks.empty else "No stocks recommended for buying.")
        st.error(f"🚨 **Stocks to SELL:** {', '.join(sell_stocks['Stock Symbol'].tolist())}" if not sell_stocks.empty else "No stocks recommended for selling.")
        st.info("⏳ **Stocks to HOLD:** Market sentiment is neutral for remaining stocks.")
