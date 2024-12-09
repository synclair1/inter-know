import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from torch.nn.functional import softmax
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained DistilBERT model and tokenizer for intent classification
def evaluate_intent(input_text, model, tokenizer):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = softmax(logits, dim=-1)
    intent = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities.max().item()
    return intent, confidence

# Load pre-trained GPT2 model for conversation
def generate_chat_response(input_text):
    tokenizer = GPT2Tokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = GPT2LMHeadModel.from_pretrained("microsoft/DialoGPT-medium")
    
    # Ensure pad_token_id is set (usually this is the same as eos_token)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Encode input with padding and attention_mask
    new_user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt', padding=True, truncation=True)
    
    # Create attention_mask
    attention_mask = new_user_input_ids.ne(tokenizer.pad_token_id).long()
    
    # Generate a response
    chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, attention_mask=attention_mask)
    
    # Decode the generated response
    response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# Generate task response based on predicted intent
def generate_task_response(input_text, intent):
    task_responses = {
        0: "Okay, setting an alarm.",
        1: "Sure, I'll set that reminder for you.",
        2: "I'll fetch the contact details for you.",
        3: "Calling a contact.",
        4: "Opening the application now."
    }
    return task_responses.get(intent, "I didn't understand that task.")

# Main function
def main():
    # Load the trained model and tokenizer from the saved directory
    task_model_path = './saved_model'  # Path to the saved trained model
    
    # Load the tokenizer and model from the saved model directory
    task_tokenizer = DistilBertTokenizerFast.from_pretrained(task_model_path)
    task_model = DistilBertForSequenceClassification.from_pretrained(task_model_path)  # Load your trained model
    
    print("Hi! I am Inter-Know. You can start chatting now.")
    
    while True:
        input_text = input("You: ")  # Get text input
        
        if input_text.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # Evaluate the intent using the trained model
        intent, confidence = evaluate_intent(input_text, task_model, task_tokenizer)

        # Confidence threshold: if confidence is low, fallback to GPT-2 for conversation
        if confidence < 0.6:  # Set confidence threshold
            print(f"Bot: {generate_chat_response(input_text)}")
        else:
            print(f"Bot: {generate_task_response(input_text, intent)}")

if __name__ == "__main__":
    main()
