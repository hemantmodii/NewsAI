import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Set the title of the app
st.title("📰 AI News Article Generator")

# Fetch news headlines from NewsAPI
def fetch_news_headlines(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles if article["title"]]
    else:
        st.error("Failed to fetch news headlines.")
        return []

# Load API key (ideally from Streamlit secrets)
NEWS_APIKEY = os.getenv("NEWS_API_KEY")  # Replace with st.secrets["NEWS_API_KEY"] for production
GENERATE_API_URL = "http://127.0.0.1:8000/generate/"  # Define the URL for the article generation API

# Fetch headlines
headlines = fetch_news_headlines(NEWS_APIKEY)

# Allow user to select a headline or enter their own
if headlines:
    selected_headline = st.selectbox("Select a News Headline:", headlines)
else:
    st.warning("No headlines available. Please enter a custom headline.")
    selected_headline = ""

headline = st.text_input("Or enter a news headline:")

# Use the selected headline if no custom headline is entered
if not headline:
    headline = selected_headline

# Generate article on button click
if st.button("Generate Article"):
    if headline:
        try:
            response = requests.post(GENERATE_API_URL, json={"headline": headline})
            if response.status_code == 200:
                article = response.json().get("article", "")
                st.write(article)
            else:
                st.error("Failed to generate article.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter or select a headline.")