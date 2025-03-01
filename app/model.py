import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API Key (Replace with your actual key or use an environment variable)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found.")

genai.configure(api_key=API_KEY)

# Select the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_article(headline: str) -> str:
    """
    Generates an article based on the given headline using Google's Gemini AI.
    """
    prompt = f"Write a detailed news article about: {headline}"
    
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "Failed to generate article."
    
    except Exception as e:
        return f"Error: {str(e)}"
