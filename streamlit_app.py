import streamlit as st
import google.generativeai as genai
import requests
import json

# Configure Google Generative AI API key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Horoscope API configuration
ASTROLOGY_API_URL = "https://kebrya-astrology-and-horoscope.p.rapidapi.com/api/chart"
ASTROLOGY_API_HEADERS = {
    "x-rapidapi-key": st.secrets["HOROSCOPE_API_KEY"],
    "x-rapidapi-host": "kebrya-astrology-and-horoscope.p.rapidapi.com",
    "Content-Type": "text/plain"
}

# Streamlit App
st.title("Karma AI - Your Astrology Bot")
st.write("Discover astrological insights and get AI-powered responses.")

# User Input for Astrology Chart
st.subheader("Generate Your Astrology Chart")
latitude = st.text_input("Enter Latitude (e.g., 35.708309):", "35.708309")
longitude = st.text_input("Enter Longitude (e.g., 51.380730):", "51.380730")
year = st.number_input("Year of Birth:", min_value=1900, max_value=2100, value=1991)
month = st.number_input("Month of Birth:", min_value=1, max_value=12, value=11)
day = st.number_input("Day of Birth:", min_value=1, max_value=31, value=1)
hour = st.number_input("Hour of Birth (24-hour format):", min_value=0, max_value=23, value=7)
minute = st.number_input("Minute of Birth:", min_value=0, max_value=59, value=45)
time_zone = st.text_input("Enter Time Zone (e.g., +03:30):", "+03:30")

# Generate Astrology Chart Button
if st.button("Generate Astrology Chart"):
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "min": minute,
        "sec": 0,
        "varga": [
            "D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", 
            "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"
        ],
        "nesting": 4,
        "time_zone": time_zone,
        "infolevel": ["basic", "ashtakavarga", "grahabala", "rashibala", "yogas", "panchanga"]
    }

    try:
        # Send API request
        response = requests.post(
            ASTROLOGY_API_URL, 
            data=json.dumps(payload), 
            headers=ASTROLOGY_API_HEADERS
        )
        chart_data = response.json()

        # Display Chart Data
        st.subheader("Astrology Chart Data")
        st.json(chart_data)
    except Exception as e:
        st.error(f"Error fetching astrology chart: {e}")

st.markdown("---")  # Separator

# Generative AI Section
st.subheader("Generative AI - Ask Anything!")
prompt = st.text_input("Enter your astrology-related or general prompt:", "What are the traits of a Scorpio?")

if st.button("Generate AI Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Display the response
        st.write("Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating AI response: {e}")

# Footer
st.markdown("---")
st.caption("Powered by [Google Generative AI](https://cloud.google.com/vertex-ai) and Kebrya Astrology API.")
