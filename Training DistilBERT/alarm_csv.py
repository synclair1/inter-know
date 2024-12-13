from transformers import pipeline
import csv

# Load the pre-trained T5 model for paraphrasing
paraphrase_model = pipeline("text2text-generation", model="t5-base")

# Function to generate paraphrases for a sentence
def generate_paraphrases(sentence, num_paraphrases=8, max_length=50, max_attempts=20):
    paraphrases = set()  # Using a set to avoid duplicate paraphrases
    attempts = 0  # Track the number of attempts
    
    while len(paraphrases) < num_paraphrases and attempts < max_attempts:
        print(f"Generating paraphrase {attempts + 1} for: {sentence}")
        paraphrased_text = paraphrase_model(f"paraphrase: {sentence}", max_length=max_length)
        
        # Check if the model generates valid text
        generated_text = paraphrased_text[0]['generated_text'].strip()
        if generated_text:  # Ensure the generated text is not empty
            paraphrases.add(generated_text)
        attempts += 1
    
    # Print message if max attempts reached
    if attempts >= max_attempts:
        print(f"Max attempts reached for paraphrasing: {sentence}")
    
    return list(paraphrases)

# Original sentences for calling a person
original_data = [
    "Call John.",
    "Can you dial Mark's number?",
    "Please call Sarah right now.",
    "I need to call Robert, his number is in my contacts.",
    "Dial Saira's number.",
    "Please call my mom.",
    "Can you ring up Jane on her cell?",
    "Could you call Fatima's cell phone?",
    "Make a call to Peter at his office.",
    "Give Asmeer a ring at his workplace.",
    "Can you connect me to Ali on his home number?",
    "Call my dad on his mobile phone.",
    "Please make a phone call to Anna, her number's saved.",
    "Dial my friend Steve at 0333-2224319.",
    "My pal Steve's number is 0331-2224319.",
    "Could you call Chris on Skype?",
    "Call Lisa, please.",
    "Please call Mike's number for a business update.",
    "Make a call to the office, it’s urgent.",
    "Connect me to my brother in Punjab.",
    "Call Tom's mobile, it’s an emergency.",
    "Please ring up Alex right away.",
    "Please give Shakeel a call immediately.",
    "Is it possible for you to call Mark?",
    "Can you make a call to my friend in New York?"
]

# Create the CSV data (sentence, intent)
intent = "Calling a Person"
csv_data = []

for sentence in original_data:
    # Add the original sentence and intent to the CSV data
    csv_data.append([sentence, intent])
    
    # Generate paraphrases and add them to the CSV data
    paraphrases = generate_paraphrases(sentence, num_paraphrases=30)
    for paraphrase in paraphrases:
        print(f"Adding paraphrase: {paraphrase}")
        csv_data.append([paraphrase, intent])

# Save the data to a CSV file
with open('calling_intent_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['sentence', 'intent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for sentence, intent in csv_data:
        writer.writerow({'sentence': sentence, 'intent': intent})

print("CSV file has been generated with paraphrased sentences!")
