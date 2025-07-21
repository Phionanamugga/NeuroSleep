import streamlit as st
import requests
from datetime import date, time

# Configuration
API_URL = "http://127.0.0.1:8501"

# Streamlit Page Config
st.set_page_config(page_title="NeuroSleep Recommender", layout="centered")

st.title("🧠 NeuroSleep - Smart Sleep Assistant")
st.markdown("Track your sleep and get **personalized recommendations** based on your sleep debt.")

# --- Log New Sleep Entry ---
st.header("🛌 Log Your Sleep")

with st.form("sleep_log_form"):
    sleep_date = st.date_input("Select Sleep Date", value=date.today())
    sleep_duration = st.slider("Sleep Duration (hours)", 0.0, 12.0, 7.5, step=0.25)
    mood = st.selectbox("How was your mood after waking up?", ["😴 Tired", "🙂 Okay", "😃 Refreshed"])
    submit_log = st.form_submit_button("Submit Sleep Log")

    if submit_log:
        response = requests.post(f"{API_URL}/sleep-log/", json={
            "date": sleep_date.isoformat(),
            "sleep_duration": sleep_duration,
            "mood": mood
        })
        if response.status_code == 201:
            st.success("✅ Sleep log saved successfully!")
        else:
            st.error(f"❌ Failed to save log. Status: {response.status_code}")

# --- Get Recommendation ---
st.header("💡 Sleep Recommendation")

wake_time = st.time_input("Preferred Wake Time", value=time(7, 0))
if st.button("Get Recommendation"):
    response = requests.get(f"{API_URL}/recommendation", params={"wake_time": wake_time.strftime("%H:%M")})
    if response.status_code == 200:
        result = response.json()
        st.metric("📉 Sleep Debt", f"{result['sleep_debt_hours']} hours")
        st.metric("🕒 Recommended Bedtime", result["recommended_bedtime"])
        st.info(result["message"])
    else:
        st.error("Failed to fetch recommendation.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by NeuroSleep Team")
