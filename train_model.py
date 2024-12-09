from datasets import load_from_disk
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
from transformers import DistilBertTokenizerFast
import torch

def train_model():
    # Load the tokenized dataset
    dataset = load_from_disk('tokenized_dataset')  # Adjust the path if necessary

    # Split dataset into train and test sets manually (80% train, 20% test)
    if 'train' not in dataset or 'test' not in dataset:
        dataset = dataset.train_test_split(test_size=0.2)  # Split 80/20
    train_dataset = dataset['train']
    test_dataset = dataset['test']

    # Check and adjust the labels if necessary
    def preprocess_labels(example):
        if example['label'] > 8:  # If the label exceeds 8, cap it at 8 (for 9 classes)
            example['label'] = 8
        return example

    # Apply label adjustment to the train and test datasets
    train_dataset = train_dataset.map(preprocess_labels)
    test_dataset = test_dataset.map(preprocess_labels)

    # Load DistilBERT tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    # Load DistilBERT model for sequence classification with 9 labels
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=9)

    # Define the training arguments
    training_args = TrainingArguments(
        output_dir='./results',          # output directory
        evaluation_strategy="epoch",     # evaluation strategy to use
        learning_rate=2e-5,              # learning rate
        per_device_train_batch_size=16,  # batch size for training
        per_device_eval_batch_size=64,   # batch size for evaluation
        num_train_epochs=3,              # number of training epochs
        weight_decay=0.01,               # strength of weight decay
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,                         # the model to train
        args=training_args,                  # training arguments
        train_dataset=train_dataset,         # training dataset
        eval_dataset=test_dataset,           # evaluation dataset
    )

    # Start training
    trainer.train()
    tokenizer.save_pretrained('./saved_model')
    
    # Save the trained model
    model.save_pretrained('saved_model')

# Run the training function
if __name__ == "__main__":
    train_model()
