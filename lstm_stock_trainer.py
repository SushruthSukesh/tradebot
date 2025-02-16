import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

class LSTMStockTrainer:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.models = {}  # Store trained models
        self.summary_df = pd.DataFrame(columns=["Symbol", "Final Train Loss", "Final Val Loss", "Sentiment Score", "Prediction Signal"])
        self.sentiment_threshold = 0.1  # Adjust sentiment threshold as needed

    def create_sequences(self, data, seq_length=15):
        """Create sequences for LSTM training."""
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length, :-1])  # Features: Close price & sentiment
            y.append(data[i + seq_length, 0])  # Target: Next day's closing price
        return np.array(X), np.array(y)

    def train_models(self):
        """Train LSTM models for all stocks."""
        stock_groups = self.stock_data.groupby("Symbol")

        for symbol, stock_data in stock_groups:
            print(f"\n🔄 Training LSTM model for {symbol}...\n")
            stock_data = stock_data.sort_values(by="Date")

            # Convert to numpy array
            stock_array = stock_data[['Close', 'sentiment_score']].values
            X, y = self.create_sequences(stock_array)

            if len(X) == 0:
                print(f"⚠️ Insufficient data for {symbol}. Skipping...")
                continue

            # Split data into training/testing sets (80% train, 20% test)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

            # Build LSTM Model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25, activation="relu"),
                Dense(1)  # Output: Next day's stock price
            ])

            # Compile & Train
            model.compile(optimizer="adam", loss="mean_squared_error")
            history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)

            # Save trained model
            self.models[symbol] = model

            # Evaluate & Log Results
            final_train_loss = history.history['loss'][-1]
            final_val_loss = history.history['val_loss'][-1]
            avg_sentiment_score = stock_data['sentiment_score'].mean()

            # Determine Buy/Sell Signal
            if final_val_loss < 0.01 and avg_sentiment_score > self.sentiment_threshold:
                prediction_signal = "BUY"
            elif final_val_loss > 0.02:
                prediction_signal = "SELL"
            else:
                prediction_signal = "HOLD"

            # Append to Summary DataFrame
            self.summary_df = self.summary_df._append({
                "Symbol": symbol,
                "Final Train Loss": final_train_loss,
                "Final Val Loss": final_val_loss,
                "Sentiment Score": avg_sentiment_score,
                "Prediction Signal": prediction_signal
            }, ignore_index=True)

            # Plot Training Loss
            plt.figure(figsize=(8, 4))
            plt.plot(history.history['loss'], label='Train Loss')
            plt.plot(history.history['val_loss'], label='Test Loss')
            plt.title(f'{symbol} - LSTM Training Loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            plt.show()

        # Save Summary
        self.summary_df.to_csv("stock_summary_signals.csv", index=False)
        print("\n✅ Summary of stock signals saved to 'stock_summary_signals.csv'!")
