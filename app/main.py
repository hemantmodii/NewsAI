from fastapi import FastAPI
from pydantic import BaseModel
from app.model import generate_article

app = FastAPI()

# Define request structure
class HeadlineRequest(BaseModel):
    headline: str

@app.post("/generate/")
def generate_news(data: HeadlineRequest):
    article = generate_article(data.headline)
    return {"headline": data.headline, "article": article}

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the AI News Generator API!"}
