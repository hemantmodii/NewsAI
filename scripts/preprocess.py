import json
import gzip
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

# Load dataset
with open("data/news_dataset.json", "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]  # Read each line as JSON object

train_data = []

for entry in dataset:
    headline = entry.get("headline", "").strip()
    description = entry.get("short_description", "").strip()
    
    if not headline or not description:
        continue  # Skip empty data

    combined_text = f"{headline}. {description}"  # Combine headline + description
    train_data.append(combined_text)  # Save raw text

# Tokenize data
class NewsDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)  # FIX: Implements length

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        return {key: val.squeeze(0) for key, val in encoding.items()}

# Create dataset object
train_dataset = NewsDataset(train_data, tokenizer)

# Save dataset using torch
torch.save(train_dataset, "data/train_dataset.pt")

print(f"✅ Preprocessing complete! Saved {len(train_data)} entries in train_dataset.pt")
