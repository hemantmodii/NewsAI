import torch
from transformers import Trainer, TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from torch.utils.data import Dataset

# Choose a smaller model
model_name = "EleutherAI/gpt-neo-125M"  # ✅ Replace with "gpt2" or "distilgpt2" if needed
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

class NewsDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# Load preprocessed dataset
train_dataset = torch.load("data/train_dataset.pt", weights_only=False)  # ✅ Load processed dataset

# Define training arguments
training_args = TrainingArguments(
    output_dir="output",
    overwrite_output_dir=True,
    per_device_train_batch_size=4,  # ✅ Increase since model is smaller
    num_train_epochs=3,
    save_steps=1000,
    save_total_limit=2,
    logging_dir="logs",
    logging_steps=500,
    evaluation_strategy="no",  # Set to "steps" if validation is needed
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  # ✅ No need for max_steps now
)

# Start training
trainer.train()

# Save final model
trainer.save_model("trained_model")
print("✅ Model training complete and saved!")
