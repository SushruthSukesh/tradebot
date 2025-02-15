import streamlit as st
import pandas as pd
import base64
import os
import requests
from graph import StockGraphs
from home import AIStockChatbot
from analysis import AnalysisData  # ✅ Import Stock Analysis Class

# ✅ Ensure set_page_config is the FIRST Streamlit command
st.set_page_config(page_title="AI Stock Market Dashboard", layout="wide")

# ✅ Function to set background with fade effect
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_with_fade(jpg_file):
    # Check if the image file exists
    if not os.path.exists(jpg_file):
        st.error(f"Image file '{jpg_file}' not found!")
        return  # Exit if image not found

    # If image exists, continue with the background setting
    bin_str = get_base64(jpg_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Adjust the last value (0.5) for fade intensity */
        z-index: -1;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def load_external_image(url):
    try:
        # Check if URL is accessible
        response = requests.get(url)
        if response.status_code == 200:
            return url  # URL is accessible, return it
        else:
            st.error("Image URL not found. Using default image.")
            return "https://source.unsplash.com/featured/?technology"  # Fallback image
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading image: {e}. Using fallback image.")
        return "https://source.unsplash.com/featured/?technology"  # Fallback image

# ✅ Function to load and inject CSS
def load_css(file_name):
    """Reads and applies a local CSS file."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Apply the CSS styles
load_css("styles.css")

# ✅ Load stock data
file_path = "stock.csv"  # Ensure correct path
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# ✅ Create instances
stock_graphs = StockGraphs(df)
analysis_data = AnalysisData()  # ✅ Initialize Stock Analysis class

# ✅ Sidebar with Dropdown Navigation
st.sidebar.title("🌍 AI Trading Dashboard")
page = st.sidebar.selectbox("🔍 Choose a Page:", ["Home", "Stock Analysis", "Stock Data"])

# --- Home Page ---
if page == "Home":
    AIStockChatbot()  # Initialize and render the chatbot UI

# --- Stock Analysis Page ---
elif page == "Stock Analysis":
    st.markdown("<h1>📊 AI-Powered Stock Analysis</h1>", unsafe_allow_html=True)

    # Dropdown for stock selection
    stocks = df["Symbol"].unique()
    selected_stock = st.selectbox("📈 Select a Stock", stocks)

    

    # Generate and display stock graphs
    try:
        stock_graphs.plot_graphs(selected_stock)
    except Exception as e:
        st.error(f"An error occurred while plotting the graphs: {e}")

# --- Stock Data Page (Newly Added) ---
elif page == "Stock Data":
    analysis_data.display_analysis()  # ✅ Call the Stock Data Analysis Method

# Set background (Ensure correct path to 'bg.jpeg')
set_background_with_fade("bg.jpeg")
