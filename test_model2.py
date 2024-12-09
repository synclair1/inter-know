import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import time

# Measure the start time for loading the model
start_time = time.time()

# Load model and tokenizer
print("Loading model...")
model_name = "xlm-roberta-base"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)  # Adjust num_labels based on your intent classes
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Print how long it took to load the model
print("Model loaded in", time.time() - start_time, "seconds")

# Test cases for the assistant
test_cases = [
    "Can you set an alarm for 7 AM?",
    "Remind me to take medicine at 8 PM",
    "Who is my contact named John?",
    "Set an alarm at 5:30 PM"
]

for input_text in test_cases:
    print(f"Input: {input_text}")
    
    # Tokenize input text and pass it through the model
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    
    # Apply softmax to get probabilities
    probabilities = F.softmax(logits, dim=-1)
    
    # Get the predicted intent (highest probability)
    intent = torch.argmax(probabilities, dim=-1).item()

    # Check which intent was recognized
    if intent == 0:
        print("Action: Setting an alarm!")
    elif intent == 1:
        print("Action: Setting a reminder!")
    elif intent == 2:
        print("Action: Checking contacts!")
    else:
        print("Action: No recognizable action found.")
