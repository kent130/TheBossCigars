import os
import subprocess

# Ensure required packages are installed
required_packages = ["requests", "beautifulsoup4", "pandas", "streamlit"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(["pip", "install", package])

import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Function to fetch cigar prices in real-time
def fetch_cigar_prices(cigar_name):
    stores = {
        "Cigars International": "https://www.cigarsinternational.com/shop/cigars/2050396/",
        "JR Cigars": "https://www.jrcigars.com/cigars/all-cigars/",
        "Famous Smoke Shop": "https://www.famous-smoke.com/cigars",
    }
    
    prices = []
    
    for store, url in stores.items():
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Simulated scraping: Find price based on store structure (Modify based on actual HTML structure)
            price = soup.find("span", class_="price")  # Adjust based on retailer HTML
            
            if price:
                price_text = price.text.strip()
            else:
                price_text = "Price not found"
            
            prices.append({"Store": store, "Cigar": cigar_name, "Price": price_text, "URL": url})
        except Exception as e:
            prices.append({"Store": store, "Cigar": cigar_name, "Price": "Error fetching", "URL": url})
    
    return pd.DataFrame(prices)

# Manual Data Entry Feature
manual_entries = []
def add_manual_entry(store, cigar_name, price, url):
    manual_entries.append({"Store": store, "Cigar": cigar_name, "Price": price, "URL": url})

def get_combined_results(cigar_name):
    real_time_data = fetch_cigar_prices(cigar_name)
    manual_data = pd.DataFrame(manual_entries)
    return pd.concat([real_time_data, manual_data], ignore_index=True)

# Streamlit UI
st.set_page_config(page_title="KingBoss Cigars", layout="wide")
st.title("🔎 KingBoss Cigars Price Finder")
st.markdown("Find the best deals on premium cigars in real-time!")

cigar_name = st.text_input("Enter cigar name:")
if st.button("Find Best Prices"):
    if cigar_name:
        results = get_combined_results(cigar_name)
        st.dataframe(results)
    else:
        st.warning("Please enter a cigar name.")

st.sidebar.title("📝 Manual Price Entry")
store = st.sidebar.text_input("Store Name:")
cigar_manual = st.sidebar.text_input("Cigar Name:")
price = st.sidebar.text_input("Price:")
url = st.sidebar.text_input("URL:")
if st.sidebar.button("Add Manual Entry"):
    add_manual_entry(store, cigar_manual, price, url)
    st.sidebar.success("Manual entry added successfully!")
