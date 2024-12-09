from transformers import pipeline
import csv

# Load the pre-trained T5 model for paraphrasing
paraphrase_model = pipeline("text2text-generation", model="t5-base")

# Function to generate paraphrases for a sentence
def generate_paraphrases(sentence, num_paraphrases=30, max_length=50):
    paraphrases = set()  # Using a set to avoid duplicate paraphrases
    while len(paraphrases) < num_paraphrases:
        paraphrased_text = paraphrase_model(f"paraphrase: {sentence}", max_length=max_length)
        paraphrases.add(paraphrased_text[0]['generated_text'])
    return list(paraphrases)

# Original sentences for setting alarms
original_data = [
    "Set an alarm for 6:00 AM.",
    "Can you wake me up at 8 AM tomorrow?",
    "I need an alarm for 7:30 in the morning, please.",
    "Please set an alarm for 3 PM on Friday.",
    "Wake me up at noon tomorrow.",
    "Can you remind me at 5 PM today?",
    "Set an alarm for 9:15 AM next Tuesday.",
    "Please wake me up at 7 AM tomorrow morning.",
    "Set an alarm for 10:30 in the morning, but only on weekdays.",
    "Remind me at 6:45 PM to pick up the package.",
    "Can you set an alarm for 5:00 PM sharp?",
    "Set an alarm for 4:30 AM, just to be sure.",
    "I need a reminder for 11:00 PM to finish my homework.",
    "Set an alarm at 7:15 AM on the weekend.",
    "Please wake me at 8:00 AM sharp, no snooze.",
    "Set the alarm for 1:30 PM, for an important call.",
    "Set an alarm for today at 2 PM, make sure it's loud!",
    "Can you set a wake-up alarm for 10 AM tomorrow? Don’t forget!",
    "Please wake me up at 5:30 PM for my meeting.",
    "Can you set an alarm at 6:00 PM on Thursday?"
]

# Create the CSV data (sentence, intent)
intent = "Setting Alarms"
csv_data = []

for sentence in original_data:
    # Add the original sentence and intent to the CSV data
    csv_data.append([sentence, intent])
    
    # Generate paraphrases and add them to the CSV data
    paraphrases = generate_paraphrases(sentence, num_paraphrases=30)
    for paraphrase in paraphrases:
        csv_data.append([paraphrase, intent])

# Save the data to a CSV file
with open('intent_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['sentence', 'intent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for sentence, intent in csv_data:
        writer.writerow({'sentence': sentence, 'intent': intent})

print("CSV file has been generated with paraphrased sentences!")
