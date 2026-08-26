import speech_recognition as sr
import time
import datetime as dt
import webbrowser
import pyttsx3
# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()
mic = sr.Microphone()
userWantstoSearch = False

search_triggers = [
    "search",
    "google",
    "look up",
    "find"
]


def callback(recognizer, audio):
    global userWantstoSearch
    try: 
        text = recognizer.recognize_google(audio)
        text = text.lower()
        if userWantstoSearch:
            speak(f"Searching for '{text}'...")
            userWantstoSearch = False
            webbrowser.open_new_tab(f"https://www.google.com/search?q={text}")
        else:
            print(f"Recognized audio: {text}")
            if "hello" in text:
                speak("Hello to you too!")
            elif "date" in text:
                now = dt.date.today()
                speak(f"Today's date is {now.strftime('%d-%m-%Y')}.")         
            elif "time" in text:
                now = dt.datetime.now()
                speak(f" The current time is {now.strftime('%H:%M:%S')}.")
            elif any(trigger in text for trigger in search_triggers):
                speak("What would you like to search for?")
                userWantstoSearch = True


    except sr.UnknownValueError:
        #Recognizer could not understand the audio, so we just reinitialize the recognizer and continue listening for new audio.
        print("Ghozal Assistant: I'm sorry. I couldn't understand what you said. Please try again.")


stop_listening = recognizer.listen_in_background(mic, callback)

def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 125) 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) #Female voice
    engine.say(text)
    engine.runAndWait()
    engine.stop()

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
    stop_listening(wait_for_stop=True)