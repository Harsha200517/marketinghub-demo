import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="MarketingHub Demo", layout="wide")

st.title("🚴 MarketingHub – Hyperlocal Advertising Platform")

menu = st.sidebar.selectbox("Choose User", ["Merchant Dashboard", "Rider App"])

if menu == "Merchant Dashboard":
    st.header("📊 Brand Campaign Dashboard")
    st.subheader("Create New Campaign")
    brand = st.text_input("Brand Name")
    budget = st.slider("Budget (₹)", 1000, 50000, 10000)
    duration = st.selectbox("Duration", ["1 Week", "2 Weeks", "1 Month"])
    st.file_uploader("Upload Ad Logo", type=["jpg", "png"])
    
    if st.button("Launch Campaign"):
        st.success(f"Campaign for {brand} launched successfully!")
    
    st.markdown("---")
    st.subheader("Active Campaigns")
    data = {"Rider": ["Ravi", "Ankit", "Zara"], "Location": ["Bangalore", "Delhi", "Pune"], "Status": ["Active", "Active", "Offline"]}
    df = pd.DataFrame(data)
    st.table(df)
    st.map(pd.DataFrame({
        'lat': [12.97, 28.61, 18.52],
        'lon': [77.59, 77.21, 73.85]
    }))
    st.metric("Active Riders", 2)
    st.metric("Impressions", "24,500+")
    st.metric("Avg ROI", "2.4x")

elif menu == "Rider App":
    st.header("🛵 Rider Dashboard")
    rider = st.text_input("Enter Rider Name", "Ravi")
    st.write(f"Welcome, {rider}!")
    st.subheader("Assigned Campaign")
    st.info("BurgerKing - Downtown Zone")
    st.progress(70)
    st.subheader("Earnings This Week: ₹1,800")
    st.button("Mark Ride as Complete ✅")
    st.map(pd.DataFrame({
        'lat': [12.97],
        'lon': [77.59]
    }))
