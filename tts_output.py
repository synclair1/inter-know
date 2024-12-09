# evaluate_model.py
import pyttsx3
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from voice_input import get_audio_input  # Import the voice input function

# Function to speak the text (Text-to-Speech)
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to evaluate the model
def evaluate_model(input_text):
    # Load the fine-tuned model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_model")
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = F.softmax(logits, dim=-1)

    print(f"Probabilities: {probabilities}")
    intent = torch.argmax(probabilities, dim=-1).item()
    print(f"Predicted Intent: {intent}")
    
    return intent

if __name__ == "__main__":
    # Step 1: Ask for input type (speech or text)
    input_choice = input("Would you like to use speech input or text input? (Enter 'speech' or 'text'): ").strip().lower()

    # Step 2: Get input based on user choice
    if input_choice == 'speech':
        input_text = get_audio_input()  # Get voice input
    elif input_choice == 'text':
        input_text = input("Please enter your command: ")  # Get text input
    else:
        print("Invalid input choice. Exiting.")
        exit()

    # Step 3: Ask for output type (text or speech)
    output_choice = input("Would you like text output or speech output? (Enter 'text' or 'speech'): ").strip().lower()

    if input_text:
        # Get the model's prediction
        intent = evaluate_model(input_text)

        # Step 4: Output based on user's choice
        if output_choice == 'text':
            print(f"The predicted intent is: {intent}")
        elif output_choice == 'speech':
            speak(f"The predicted intent is: {intent}")
        else:
            print("Invalid output choice. Please choose 'text' or 'speech'.")
    else:
        print("No input detected.")
