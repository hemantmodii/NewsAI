from transformers import pipeline

# Load fine-tuned model
generator = pipeline("text-generation", model="./fine_tuned_model")

def generate_article(headline: str):
    prompt = f"Headline: {headline}\nArticle: "
    article = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']
    return article
