# evaluate_model.py
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from voice_input import get_audio_input  # Import voice input function
from tts_output import speak  # Import the text-to-speech function


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
    
    return intent, input_text


# Generate conversational task response
def generate_task_response(input_text, intent, is_speech=False):
    # Check the predicted intent and generate response accordingly
    if intent == 0:  # Setting an alarm
        response = "Okay, setting an alarm."
    elif intent == 1:  # Setting a reminder
        response = "Sure, I'll set that reminder for you."
    elif intent == 2:  # Fetching contacts
        response = "I'll fetch the contact details for you."
    elif intent == 3:  # Calling a contact
        # Extract name from input (assuming it's a simple task like 'call [name]')
        name = input_text.split("call")[-1].strip()  # Get the name after the word 'call'
        response = f"Calling {name}."
    elif intent == 4:  # Opening an application
        response = "Opening the application now."
    else:
        response = "I'm not sure about that task."

    # Return response based on whether it's speech or text
    if is_speech:
        return response  # Speech output
    else:
        return f"I will now perform the task you've inputted: {response}"  # Text output


# Function to confirm the user's input
def confirm_input(input_text):
    # Ask the user for confirmation on the input
    speak(f"You said: {input_text}. Is that correct?")
    confirmation = input("You said: '{}'. Is that correct? (yes/no): ".format(input_text)).strip().lower()

    if confirmation in ['yes', 'y']:
        return True
    else:
        return False


if __name__ == "__main__":
    while True:  # Loop to keep asking for input until confirmed
        # Step 1: Ask for input type (speech or text)
        input_choice = input("Would you like to use speech input or text input? (Enter 'speech' or 'text'): ").strip().lower()

        # Step 2: Get input based on user choice
        if input_choice == 'speech':
            input_text = get_audio_input()  # Get voice input
        elif input_choice == 'text':
            input_text = input("Please enter your command: ")  # Get text input
        else:
            print("Invalid input choice. Exiting.")
            continue  # Restart the loop if the input choice is invalid

        # Step 3: Confirm the input
        if confirm_input(input_text):
            # Step 4: Ask for output type (text or speech)
            output_choice = input("Would you like text output or speech output? (Enter 'text' or 'speech'): ").strip().lower()

            if input_text:
                # Get the model's prediction and probabilities
                intent, task = evaluate_model(input_text)

                # Step 5: Output based on user's choice
                if output_choice == 'text':
                    print(f"The predicted intent is: {intent}")
                    print(generate_task_response(task, intent, is_speech=False))  # Modular response for text
                elif output_choice == 'speech':
                    # Just speak the task response, not the intent or probabilities
                    speak(generate_task_response(task, intent, is_speech=True))  # Speech output
                else:
                    print("Invalid output choice. Please choose 'text' or 'speech'.")
            break  # Exit the loop after task execution
        else:
            # If not confirmed, ask again
            print("Please provide the input again in the same manner as initially.")
