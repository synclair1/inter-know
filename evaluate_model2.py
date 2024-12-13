import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load pre-trained DistilBERT model and tokenizer for intent classification
def evaluate_intent(input_text, model, tokenizer):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = softmax(logits, dim=-1)
    intent = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities.max().item()
    return intent, confidence

# Load the text-generation pipeline for conversation using GODEL for task-specific responses
def generate_chat_response_with_task(input_text, intent):
    try:
        # Load the tokenizer and model for GODEL
        model_name = "microsoft/GODEL-v1_1-large-seq2seq"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Define task-specific prompts for GODEL
        task_responses = {
            0: "You are an assistant setting an alarm for the user. Respond accordingly.",
            1: "You are an assistant setting a reminder for the user. Respond accordingly.",
            2: "You are an assistant fetching contact details for the user. Respond accordingly.",
            3: "You are an assistant calling a contact. Respond accordingly.",
            4: "You are an assistant opening an application. Respond accordingly."
        }

        prompt = task_responses.get(intent, "I didn't understand that task. Please clarify.")

        # Concatenate the input text with the task-specific prompt
        full_prompt = f"User: {input_text}\n{prompt}\nAssistant:"

        # Generate a response using GODEL
        input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids
        output_ids = model.generate(input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Main function
def main():
    # Load the trained model and tokenizer from the saved directory
    task_model_path = './saved_model'  # Path to your trained DistilBERT model
    task_tokenizer = DistilBertTokenizerFast.from_pretrained(task_model_path)
    task_model = DistilBertForSequenceClassification.from_pretrained(task_model_path)  # Load the trained DistilBERT model

    print("Hello! I am Inter-Know.")
    
    while True:
        input_text = input("You: ")  # Get text input
        
        if input_text.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # Evaluate the intent using the trained model
        intent, confidence = evaluate_intent(input_text, task_model, task_tokenizer)

        if confidence < 0.25:  # Low confidence, fall back to GODEL for response
            print("Confidence is low, switching to GODEL for response.")
            response = generate_chat_response_with_task(input_text, intent)
        else:
            # If confidence is high, generate a predefined response
            response = generate_task_response(input_text, intent)
        
        # Output the generated response
        print(f"Bot: {response}")

# Function to generate task-based responses based on intent
def generate_task_response(input_text, intent):
    task_responses = {
        0: "Okay, setting an alarm.",
        1: "Sure, I'll set that reminder for you.",
        2: "I'll fetch the contact details for you.",
        3: "Calling a contact.",
        4: "Opening the application now."
    }
    response = task_responses.get(intent, "I didn't understand that task.")
    return response

if __name__ == "__main__":
    main()
