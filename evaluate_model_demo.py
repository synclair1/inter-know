import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request, jsonify

# Load pre-trained DistilBERT model and tokenizer for intent classification
def evaluate_intent(input_text, model, tokenizer):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = softmax(logits, dim=-1)
    intent = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities.max().item()
    return intent, confidence

# Function to generate task-specific responses using GODEL
def generate_task_response(input_text, intent):
    task_responses = {
        0: "Setting an alarm.",
        1: "Setting a reminder.",
        2: "Fetching contact details.",
        3: "Calling a contact.",
        4: "Opening an application."
    }

    # Dynamically generate response based on task
    if intent == 3:  # If the task is to call a contact (e.g., "call dad")
        response = f"Sure, I will initiate the call to {input_text.split()[1]}."
    elif intent == 4:  # If the task is to open an application
        response = f"Opening the application for {input_text.split()[1]}."
    else:
        # For other intents, return a general response
        response = task_responses.get(intent, "I didn't understand that task.")
    
    return response

# Load GODEL model for conversation
def generate_chat_response(input_text):
    try:
        # Load the tokenizer and model for GODEL
        model_name = "microsoft/GODEL-v1_1-large-seq2seq"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Encode the input and generate a response
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**inputs, max_length=100, num_beams=5, early_stopping=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def handle_request():
    # Load the trained model and tokenizer from the saved directory
    task_model_path = './saved_model'
    task_tokenizer = DistilBertTokenizerFast.from_pretrained(task_model_path)
    task_model = DistilBertForSequenceClassification.from_pretrained(task_model_path)  # Load the trained DistilBERT model
    
    # Get input from the POST request
    data = request.json
    input_text = data.get('message', '')
    
    # Check if the input text is valid and process accordingly
    if input_text.lower() in ["exit", "quit", "bye"]:
        return "Goodbye"
    
    # Evaluate the intent using the trained model
    intent, confidence = evaluate_intent(input_text, task_model, task_tokenizer)
    
    if confidence < 0.25:  # Low confidence, use GODEL for conversational response
        bot_response = generate_chat_response(input_text)
    else:  # Otherwise, generate task-specific response
        bot_response = generate_task_response(input_text, intent)
    
    return bot_response

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port = 5000)
