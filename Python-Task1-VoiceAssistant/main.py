import speech_recognition as sr
import time
import datetime as dt
import webbrowser
import pyttsx3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()
mic = sr.Microphone()
userWantstoSearch = False

training_data = {
    "greeting": ["hello", "hi there", "hey", "good morning"],
    "time":     ["what time is it", "tell me the time", "current time please"],
    "date":     ["what's the date", "what day is it today"],
    "search":   ["search for", "look up", "google", "find information about"],
}


X_train, y_train = [], []
for intent, phrases in training_data.items():
    for phrase in phrases:
        X_train.append(phrase)
        y_train.append(intent)

vectorizer = TfidfVectorizer()
X_vectors = vectorizer.fit_transform(X_train)

intent_model = LogisticRegression()
intent_model.fit(X_vectors, y_train)


def classify_intent(text, confidence_threshold=0.25):
    vec = vectorizer.transform([text])
    probabilities = intent_model.predict_proba(vec)[0]
    best_index = probabilities.argmax()
    confidence = probabilities[best_index]
    if confidence < confidence_threshold:
        return "unknown"
    return intent_model.classes_[best_index]

# search_triggers = [
#     "search",
#     "google",
#     "look up",
#     "find"
# ]


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
            intent = classify_intent(text)
            if intent == "greeting":
                speak("Hello to you too!")
            elif intent == "date":
                now = dt.date.today()
                speak(f"Today's date is {now.strftime('%d-%m-%Y')}.")         
            elif intent == "time":
                now = dt.datetime.now()
                speak(f" The current time is {now.strftime('%H:%M:%S')}.")
            # elif any(trigger in text for trigger in search_triggers):
            elif intent == "search":
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