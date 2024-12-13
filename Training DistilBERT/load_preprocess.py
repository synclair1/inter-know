import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer

# Load the CSV file
def load_data(csv_file):
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} samples from the CSV file.")
    return df

# Initialize the tokenizer (make sure it's compatible with the model)
def initialize_tokenizer(model_name="distilbert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer

# Tokenize the dataset
def tokenize_data(df, tokenizer, max_length=128):
    # Ensure we're tokenizing with padding and truncation
    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding="max_length", max_length=max_length)

    # Convert DataFrame to Hugging Face Dataset
    dataset = Dataset.from_pandas(df)

    # Apply the tokenizer to the dataset
    tokenized_dataset = dataset.map(preprocess_function, batched=True)
    return tokenized_dataset

# Save the tokenized dataset
def save_tokenized_data(tokenized_dataset, save_path="tokenized_dataset"):
    tokenized_dataset.save_to_disk(save_path)
    print(f"Tokenized dataset saved to {save_path}")

# Main processing function
def main():
    csv_file = "augmented_intents.csv"  # Adjust path if necessary
    df = load_data(csv_file)
    tokenizer = initialize_tokenizer()
    tokenized_dataset = tokenize_data(df, tokenizer)
    save_tokenized_data(tokenized_dataset)

if __name__ == "__main__":
    main()
