import speech_recognition as sr
import time
import datetime as dt
import webbrowser
import pyttsx3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import smtplib
from email.mime.text import MIMEText


conversation_state = None   # tracks what we're waiting for, across multiple callback() calls
pending_data = {}           # scratch space to build up the email as answers come in
EMAIL_ADDRESS = "email1@gmail.com"
EMAIL_APP_PASSWORD = "NOTYouRrRealPassword"   
# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()
mic = sr.Microphone()

training_data = {
    "greeting": ["hello", "hi there", "hey", "good morning"],
    "time":     ["what time is it", "tell me the time", "current time please"],
    "date":     ["what's the date", "what day is it today"],
    "search":   ["search for", "look up", "google", "find information about"],
    "email": ["send an email", "email someone", "compose an email"],
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

def send_email(to_address, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)

        speak("Your email has been sent.")
    except Exception as e:
        print(f"Email error: {e}")
        speak("Sorry, I couldn't send that email.")
def parse_spoken_email(text):
    text = text.strip()
    text = text.replace(" at ", "@")
    text = text.replace(" dot ", ".")
    text = text.replace(" underscore ", "_")
    text = text.replace(" dash ", "-")
    return text.replace(" ", "")


def callback(recognizer, audio):
    global conversation_state, pending_data
    try: 
        text = recognizer.recognize_google(audio)
        text = text.lower()     
        if "abort" in text and conversation_state is not None:
            speak("Okay, cancelled.")
            conversation_state = None
            pending_data = {}
            
            return        
        if conversation_state == "awaiting_search":
            speak(f"Searching for '{text}'...")
            conversation_state = None
            webbrowser.open_new_tab(f"https://www.google.com/search?q={text}")
        else:
            if conversation_state == "awaiting_email_to":
                pending_data["to"] = parse_spoken_email(text)
                speak(f"I heard the address as {pending_data['to']}. Say yes to confirm")
                conversation_state = "confirming_email_to"
                return

            if conversation_state == "confirming_email_to":
                if "yes" in text:
                    speak("What should the subject be?")
                    conversation_state = "awaiting_email_subject"
                else:
                    speak("Okay, say the email address again.")
                    conversation_state = "awaiting_email_to"
                return

            if conversation_state == "awaiting_email_subject":
                pending_data["subject"] = text
                speak("And what should the email say?")
                conversation_state = "awaiting_email_body"
                return

            if conversation_state == "awaiting_email_body":
                pending_data["body"] = text
                send_email(pending_data["to"], pending_data["subject"], pending_data["body"])
                conversation_state = None
                pending_data = {}
                return            
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
                conversation_state = "awaiting_search"
            elif intent == "email":
                speak("Who should I send it to?")
                conversation_state = "awaiting_email_to"

    except sr.UnknownValueError:
        #Recognizer could not understand the audio, so we just reinitialize the recognizer and continue listening for new audio.
        print("Ghozal Assistant: I'm sorry. I couldn't understand what you said. Please try again.")


stop_listening = recognizer.listen_in_background(mic, callback)
recognizer.pause_threshold = 1.5   # was 0.8 by default
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



