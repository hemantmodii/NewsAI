import streamlit as st
import requests

st.title("📰 AI News Article Generator")

headline = st.text_input("Enter a news headline:")
if st.button("Generate Article"):
    response = requests.post("http://127.0.0.1:8000/generate/", json={"headline": headline})
    article = response.json()["article"]
    st.write(article)
