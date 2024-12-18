import csv

# Define the intents and their corresponding example sentences
data = [
    # Setting Alarms
    ("Set an alarm for 6:00 AM.", "Setting Alarms"),
    ("Can you wake me up at 8 AM tomorrow?", "Setting Alarms"),
    ("I need an alarm for 7:30 in the morning, please.", "Setting Alarms"),
    ("Please set an alarm for 3 PM on Friday.", "Setting Alarms"),
    ("Wake me up at noon tomorrow.", "Setting Alarms"),
    ("Can you remind me at 5 PM today?", "Setting Alarms"),
    ("Set an alarm for 9:15 AM next Tuesday.", "Setting Alarms"),
    ("Please wake me up at 7 AM tomorrow morning.", "Setting Alarms"),
    ("Set an alarm for 10:30 in the morning, but only on weekdays.", "Setting Alarms"),
    ("Remind me at 6:45 PM to pick up the package.", "Setting Alarms"),
    ("Can you set an alarm for 5:00 PM sharp?", "Setting Alarms"),
    ("Set an alarm for 4:30 AM, just to be sure.", "Setting Alarms"),
    ("I need a reminder for 11:00 PM to finish my homework.", "Setting Alarms"),
    ("Set an alarm at 7:15 AM on the weekend.", "Setting Alarms"),
    ("Please wake me at 8:00 AM sharp, no snooze.", "Setting Alarms"),
    ("Set the alarm for 1:30 PM, for an important call.", "Setting Alarms"),
    ("Set an alarm for today at 2 PM, make sure it's loud!", "Setting Alarms"),
    ("Can you set a wake-up alarm for 10 AM tomorrow? Don’t forget!", "Setting Alarms"),
    ("Please wake me up at 5:30 PM for my meeting.", "Setting Alarms"),
    ("Can you set an alarm at 6:00 PM on Thursday?", "Setting Alarms"),
    ("Wake me up at 9", "Setting Alarms")
    ("Set an alarm for 8", "Setting Alarms")
    ("Set an alarm for 12", "Setting Alarms")
    ("Set an alarm for 2300 hours", "Setting Alarms")
    ("Wake me up at 15:30", "Setting Alarms")
    
    
    # Calling a Person
    ("Call John.", "Calling a Person"),
    ("Can you dial Mark's number?", "Calling a Person"),
    ("Please call Sarah right now.", "Calling a Person"),
    ("I need to call Robert, his number is in my contacts.", "Calling a Person"),
    ("Dial Emma’s number.", "Calling a Person"),
    ("Please call my mom.", "Calling a Person"),
    ("Can you ring up Jane on her cell?", "Calling a Person"),
    ("Make a call to Peter at his office.", "Calling a Person"),
    ("Can you connect me to David on his home number?", "Calling a Person"),
    ("Call my dad on his mobile phone.", "Calling a Person"),
    ("Please make a phone call to Anna, her number's saved.", "Calling a Person"),
    ("Dial my friend Steve at 555-0123.", "Calling a Person"),
    ("Could you call Chris on Skype?", "Calling a Person"),
    ("Call Lisa, please.", "Calling a Person"),
    ("Please call Mike's number for a business update.", "Calling a Person"),
    ("Make a call to the office, it’s urgent.", "Calling a Person"),
    ("Connect me to my brother in California.", "Calling a Person"),
    ("Call Tom's mobile, it’s an emergency.", "Calling a Person"),
    ("Please ring up Alex right away.", "Calling a Person"),
    ("Can you make a call to my friend in New York?", "Calling a Person"),
    ("Call Dad", "Calling a Person"),
    ("Call Mom.", "Calling a Person"),
    ("Call Ali", "Calling a Person"),
    ("Call Zain", "Calling a Person"),
    ("Call Zara", "Calling a Person"),
    ("Call John", "Calling a Person"),
    ("Call Shane", "Calling a Person"),

    # Opening Applications
    ("Open Spotify.", "Opening Applications"),
    ("Can you launch Instagram?", "Opening Applications"),
    ("Please open WhatsApp.", "Opening Applications"),
    ("Open Google Chrome.", "Opening Applications"),
    ("Can you start the weather app for me?", "Opening Applications"),
    ("Launch YouTube.", "Opening Applications"),
    ("Open the calendar app and show me my meetings.", "Opening Applications"),
    ("Start the music player.", "Opening Applications"),
    ("Can you open Gmail?", "Opening Applications"),
    ("Please open Facebook.", "Opening Applications"),
    ("Launch the camera app.", "Opening Applications"),
    ("Open Twitter.", "Opening Applications"),
    ("Can you run the Notes app?", "Opening Applications"),
    ("Start the Maps app to check the route.", "Opening Applications"),
    ("Please open the calculator.", "Opening Applications"),
    ("Open Slack.", "Opening Applications"),
    ("Can you launch the clock app for a timer?", "Opening Applications"),
    ("Start my email app to check for updates.", "Opening Applications"),
    ("Please open Netflix for me.", "Opening Applications"),
    ("Open the settings app.", "Opening Applications"),
    
    # Setting Reminders
    ("Remind me to take my medicine at 9 AM.", "Setting Reminders"),
    ("Please remind me to call John at 3 PM.", "Setting Reminders"),
    ("Set a reminder for my meeting at 2:00 PM today.", "Setting Reminders"),
    ("Remind me to pick up groceries at 4 PM.", "Setting Reminders"),
    ("Please set a reminder for my dentist appointment at 10 AM tomorrow.", "Setting Reminders"),
    ("Can you remind me to buy tickets by 6 PM?", "Setting Reminders"),
    ("Remind me to call my mom in an hour.", "Setting Reminders"),
    ("Please remind me to pick up the dry cleaning later.", "Setting Reminders"),
    ("Set a reminder to pay the bills at 5 PM today.", "Setting Reminders"),
    ("Can you remind me to check my email at noon?", "Setting Reminders"),
    ("Remind me to make dinner at 7 PM.", "Setting Reminders"),
    ("Please remind me to water the plants in 30 minutes.", "Setting Reminders"),
    ("Remind me to finish my report at 5:30 PM.", "Setting Reminders"),
    ("Can you remind me to buy groceries at 8 AM tomorrow?", "Setting Reminders"),
    ("Please remind me to schedule the meeting at 9:30 AM.", "Setting Reminders"),
    ("Remind me to pay my rent by the 1st of the month.", "Setting Reminders"),
    ("Can you remind me to call the plumber at 4 PM?", "Setting Reminders"),
    ("Set a reminder to finish the presentation by 3 PM.", "Setting Reminders"),
    ("Remind me to check the car's oil level tomorrow.", "Setting Reminders"),
    ("Can you remind me to pack my bag for the trip?", "Setting Reminders"),
    
    # Browsing the Web
    ("Search for the nearest coffee shop.", "Browsing the Web"),
    ("Can you look up the weather today?", "Browsing the Web"),
    ("Find me a good recipe for pasta.", "Browsing the Web"),
    ("Search for the latest news on technology.", "Browsing the Web"),
    ("Look up how to tie a tie.", "Browsing the Web"),
    ("Find a tutorial on how to code in Python.", "Browsing the Web"),
    ("Search for the best restaurants near me.", "Browsing the Web"),
    ("Find me a new workout routine.", "Browsing the Web"),
    ("Search for the nearest gym in my area.", "Browsing the Web"),
    ("Can you find reviews for the latest iPhone?", "Browsing the Web"),
    ("Look up how to change a tire.", "Browsing the Web"),
    ("Search for the best travel destinations in Europe.", "Browsing the Web"),
    ("Find me information on the stock market.", "Browsing the Web"),
    ("Search for a new car under $20,000.", "Browsing the Web"),
    ("Find a good movie to watch tonight.", "Browsing the Web"),
    ("Search for the latest trends in fashion.", "Browsing the Web"),
    ("Can you find a good deal on a new laptop?", "Browsing the Web"),
    ("Look up how to fix a leaky faucet.", "Browsing the Web"),
    ("Search for news on the next Olympics.", "Browsing the Web"),
    ("Find a tutorial on playing the guitar.", "Browsing the Web"),
]

# Write to CSV
with open('user_intents.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Sentence', 'Intent'])  # Header row
    for row in data:
        writer.writerow(row)

print("CSV file created successfully!")
