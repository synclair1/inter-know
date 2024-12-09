# voice_input.py
import speech_recognition as sr

def get_audio_input():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google's speech recognition
        print("You said: " + recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None
