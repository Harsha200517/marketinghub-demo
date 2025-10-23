import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# ------------------------------
# CONFIGURATION
# ------------------------------
st.set_page_config(page_title="MarketingHub Demo", page_icon="🚴", layout="wide")

# Theme Colors
PRIMARY_COLOR = "#2563EB"
ACCENT_COLOR = "#FACC15"
CARD_BG = "#F8FAFC"

# ------------------------------
# HEADER
# ------------------------------
st.markdown(
    f"""
    <h1 style='text-align:center; color:{PRIMARY_COLOR};'>
        🚴 MarketingHub – Hyperlocal Advertising Platform
    </h1>
    <h4 style='text-align:center; color:gray;'>
        Connecting brands and riders through AI-powered outdoor advertising
    </h4>
    <hr style='margin-top:10px; margin-bottom:20px;'>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# GLOBAL DATA STRUCTURES
# ------------------------------
if "campaigns" not in st.session_state:
    st.session_state.campaigns = []

if "riders" not in st.session_state:
    st.session_state.riders = [
        {"name": "Ravi", "city": "Bangalore", "available": True, "lat": 12.97, "lon": 77.59, "active_campaign": None},
        {"name": "Ankit", "city": "Delhi", "available": True, "lat": 28.61, "lon": 77.21, "active_campaign": None},
        {"name": "Zara", "city": "Pune", "available": False, "lat": 18.52, "lon": 73.85, "active_campaign": None}
    ]

# ------------------------------
# SIDEBAR MENU
# ------------------------------
menu = st.sidebar.radio("Select Mode", ["Merchant Dashboard", "Rider Dashboard"])

# ===========================================================
# MERCHANT DASHBOARD
# ===========================================================
if menu == "Merchant Dashboard":
    st.subheader("🧑‍💼 Merchant Dashboard")

    with st.expander("➕ Create New Campaign", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            title = st.text_input("Campaign Title")
            desc = st.text_area("Campaign Description")
            budget = st.slider("Budget (₹)", 1000, 100000, 5000)
            duration = st.selectbox("Duration", ["1 Week", "2 Weeks", "1 Month"])
        with col2:
            ad_image = st.file_uploader("Upload Ad Image", type=["png", "jpg", "jpeg"])

        if st.button("Launch Campaign 🚀"):
            if title and desc:
                new_campaign = {
                    "title": title,
                    "desc": desc,
                    "budget": budget,
                    "duration": duration,
                    "ad_image": ad_image,
                    "status": "Waiting",
                    "assigned_riders": [],
                    "created": datetime.now().strftime("%d-%b %H:%M")
                }
                st.session_state.campaigns.append(new_campaign)
                st.success(f"✅ Campaign '{title}' launched successfully!")
            else:
                st.error("Please enter both title and description.")

    st.markdown("---")

    st.subheader("📋 Available Riders")
    available_riders = [r for r in st.session_state.riders if r["available"]]
    if available_riders:
        for rider in available_riders:
            st.markdown(
                f"""
                <div style='background-color:{CARD_BG};padding:10px;border-radius:10px;margin-bottom:10px;'>
                    <b>{rider['name']}</b> – {rider['city']}<br>
                    <i>Status: Available</i>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No riders are currently available.")

    st.markdown("---")
    st.subheader("🚴 Active Campaigns and Tracking")

    if st.session_state.campaigns:
        for c in st.session_state.campaigns:
            st.markdown(f"**📢 {c['title']}** — *{c['status']}* | Created: {c['created']}")
            if c["ad_image"]:
                st.image(c["ad_image"], width=200)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Invite Riders for '{c['title']}'"):
                    for r in st.session_state.riders:
                        if r["available"]:
                            r["active_campaign"] = c["title"]
                            c["assigned_riders"].append(r["name"])
                    c["status"] = "Invites Sent"
                    st.success(f"📨 Invites sent to available riders for '{c['title']}'")

            with col2:
                if st.button(f"Show Map for '{c['title']}'"):
                    active_coords = []
                    for r in st.session_state.riders:
                        if r["active_campaign"] == c["title"]:
                            # Simulate slight random movement
                            r["lat"] += random.uniform(-0.01, 0.01)
                            r["lon"] += random.uniform(-0.01, 0.01)
                            active_coords.append({"lat": r["lat"], "lon": r["lon"]})
                    if active_coords:
                        df = pd.DataFrame(active_coords)
                        st.map(df, zoom=6)
                    else:
                        st.info("No active riders sharing location yet.")

    else:
        st.info("No campaigns created yet.")

# ===========================================================
# RIDER DASHBOARD
# ===========================================================
elif menu == "Rider Dashboard":
    st.subheader("🛵 Rider Dashboard")
    rider_name = st.text_input("Enter Your Name to Login", "Ravi")

    rider = next((r for r in st.session_state.riders if r["name"].lower() == rider_name.lower()), None)

    if rider:
        st.success(f"Welcome back, {rider['name']} from {rider['city']} 👋")

        st.markdown("---")
        st.subheader("📢 Available Campaigns")

        waiting_campaigns = [c for c in st.session_state.campaigns if rider['name'] in c['assigned_riders'] and c['status'] in ["Invites Sent", "Waiting"]]
        if waiting_campaigns:
            for c in waiting_campaigns:
                with st.container():
                    st.image(c["ad_image"], width=200)
                    st.markdown(f"**{c['title']}** — {c['desc']}")
                    if st.button(f"Accept '{c['title']}'"):
                        c["status"] = "Accepted by Rider"
                        rider["active_campaign"] = c["title"]
                        st.success(f"✅ You accepted '{c['title']}' campaign!")
        else:
            st.info("No pending campaigns for you right now.")

        st.markdown("---")
        st.subheader("📍 My Active Campaign")

        if rider["active_campaign"]:
            active = next((c for c in st.session_state.campaigns if c["title"] == rider["active_campaign"]), None)
            if active:
                st.info(f"Active Campaign: {active['title']}")
                st.image(active["ad_image"], width=200)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📡 Share Live Location"):
                        rider["lat"] += random.uniform(-0.01, 0.01)
                        rider["lon"] += random.uniform(-0.01, 0.01)
                        st.map(pd.DataFrame([{"lat": rider["lat"], "lon": rider["lon"]}]), zoom=6)
                        st.success("📍 Live location updated!")
                with col2:
                    if st.button("✅ Mark as Complete"):
                        active["status"] = "Completed"
                        rider["active_campaign"] = None
                        rider["available"] = True
                        st.success("🎉 Campaign marked as completed!")

        else:
            st.info("No active campaign right now.")

    else:
        st.error("Rider not found. Please enter a registered name.")
