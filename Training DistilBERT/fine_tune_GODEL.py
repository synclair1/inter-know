import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load the model and tokenizer
model_name = "TheFuzzyScientist/diabloGPT_open-instruct"  # Replace with the correct model name
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Ensure the model has a padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load the dataset (daily_dialog dataset as an example)
dataset = load_dataset("daily_dialog")

# Check the first sample in the dataset for debugging
print("First sample in training dataset:", dataset['train'][0])

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['dialog'], truncation=True, padding=True, max_length=512)

# Apply tokenization to the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["dialog", "act", "emotion"])

# Print dataset columns after tokenization for debugging
print("Dataset columns after tokenization:", tokenized_datasets['train'].column_names)

# Configure training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_diabloGPT",          # Directory to save model
    evaluation_strategy="epoch",                  # Evaluate every epoch
    learning_rate=5e-5,                           # Learning rate
    per_device_train_batch_size=4,                # Batch size for training
    per_device_eval_batch_size=4,                 # Batch size for evaluation
    num_train_epochs=3,                           # Number of epochs
    weight_decay=0.01,                            # Weight decay to avoid overfitting
    save_strategy="epoch",                        # Save model every epoch
    logging_dir="./logs",                         # Directory for logs
    logging_steps=200,                            # Log every 200 steps
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,  # Pass the tokenizer to handle padding, truncation, etc.
)

# Start the training process
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained("./fine_tuned_diabloGPT")
tokenizer.save_pretrained("./fine_tuned_diabloGPT")

print("Fine-tuning completed and model saved.")
