import os
import speech_recognition as sr
import time
import datetime as dt
import webbrowser
from urllib.parse import quote_plus
import pyttsx3
import pythoncom


import json
import subprocess
from pathlib import Path


import requests 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import smtplib
from email.mime.text import MIMEText

import threading
is_speaking = threading.Event()

import re

from dotenv import load_dotenv

load_dotenv()

conversation_state = None
pending_data = {}

EMAIL_ADDRESS = os.environ.get("GHOZAL_EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("GHOZAL_EMAIL_APP_PASSWORD")
WEATHER_API_KEY = os.environ.get("GHOZAL_WEATHER_API_KEY")

print("Weather API key loaded:", bool(WEATHER_API_KEY))
print("Email App Password loaded:", bool(EMAIL_APP_PASSWORD))
print("Email loaded:", bool(EMAIL_ADDRESS))

BASE_DIR = Path(__file__).resolve().parent
COMMANDS_FILE = BASE_DIR / "commands.json"


def load_custom_commands():
    if not COMMANDS_FILE.exists():
        print("Custom commands file not found.")
        return {}

    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as file:
            commands = json.load(file)

        print(f"Custom commands loaded: {len(commands)}")
        return commands

    except (json.JSONDecodeError, OSError) as e:
        print(f"Custom commands error: {e}")
        return {}


custom_commands = load_custom_commands()


recognizer = sr.Recognizer()
mic = sr.Microphone()

training_data = {
    "greeting": ["hello", "hi there", "hey", "good morning", "good evening", "how are you"],
    
    "time": [
        "what time is it",
        "tell me the time",
        "current time please",
        "do you know the time"
    ],

    "date": [
        "what's the date",
        "what day is it today",
        "what's today's date"
    ],

    "search": [
        "search for",
        "look up",
        "google",
        "find information about",
        "can you search"
    ],

    "email": [
        "send an email",
        "email someone",
        "compose an email",
        "i want to send an email"
    ],

    "reminder": [
        "remind me",
        "reminder",
        "set a reminder",
        "remind me in",
        "set a timer",
        "remind me to",
        "can you remind me",
        "i need a reminder",
        "set a reminder for me"
    ],

    "chitchat": [
        "i think",
        "i was wondering",
        "just talking",
        "never mind",
        "i was saying",
        "i don't know",
        "i like that",
        "i guess so",
        "okay never mind"
    ],

    "weather": [
        "what's the weather",
        "what is the weather",
        "check the weather",
        "tell me the weather",
        "how's the weather",
        "how is the weather",
        "weather update",
        "current weather"
    ],

    "knowledge": [
        "what is python",
        "what is programming",
        "what is artificial intelligence",
        "what is machine learning",
        "what is a computer",
        "what is the internet",
        "what is linux",
        "what is a database",
        "who is alan turing",
        "who invented the computer",
        "explain python",
        "explain artificial intelligence",
        "tell me about programming",
        "tell me about linux"
    ],
}
knowledge_base = {
    "python": (
        "Python is a high-level programming language known for its "
        "simple syntax and wide use in web development, automation, "
        "data science, and artificial intelligence."
    ),

    "programming": (
        "Programming is the process of writing instructions that a "
        "computer can execute to perform tasks."
    ),

    "artificial intelligence": (
        "Artificial intelligence is a field of computing focused on "
        "creating systems that can perform tasks that normally require "
        "human intelligence, such as understanding language, recognizing "
        "images, and making decisions."
    ),

    "machine learning": (
        "Machine learning is a branch of artificial intelligence where "
        "computers learn patterns from data to make predictions or decisions."
    ),

    "computer": (
        "A computer is an electronic device that processes data according "
        "to instructions called programs."
    ),

    "internet": (
        "The Internet is a global network of interconnected computer "
        "networks that communicate using standardized protocols."
    ),

    "linux": (
        "Linux is a family of open-source operating systems based on the "
        "Linux kernel and commonly used on servers, computers, and embedded systems."
    ),

    "database": (
        "A database is an organized collection of data that can be "
        "stored, managed, and retrieved efficiently."
    ),

    "alan turing": (
        "Alan Turing was a British mathematician and computer scientist "
        "whose work contributed significantly to theoretical computer "
        "science and codebreaking."
    ),
}
X_train, y_train = [], []
for intent, phrases in training_data.items():
    for phrase in phrases:
        X_train.append(phrase)
        y_train.append(intent)

# stop_words='english' strips filler words (i, is, it, the, you...) out of
# the vocabulary entirely, so they can no longer act as an accidental
# fingerprint for whichever intent happened to use them in its training
# phrase (e.g. "i" was previously unique to "i need a reminder").
vectorizer = TfidfVectorizer(stop_words='english')
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


def send_email(to_address, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        print("Email error: GHOZAL_EMAIL_ADDRESS / GHOZAL_EMAIL_APP_PASSWORD not set")
        speak("I can't send email right now, my credentials aren't configured.")
        return
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


def set_reminder(minutes, message):
    speak(f"Okay, I'll remind you in {minutes} minutes.")

    def alert():
        # speak() -> _get_engine() already calls CoInitialize() for
        # whatever thread it's running on (this Timer creates a fresh
        # one each time), so no need to duplicate that here.
        try:
            speak(f"Reminder: {message}")
        except Exception as e:
            print(f"Reminder alert error: {e}")

    timer = threading.Timer(minutes * 60, alert)
    timer.daemon = True
    timer.start()


REMINDER_PATTERN = re.compile(r"(\d+)\s*(minute|minutes|min)")


def get_weather(city):
    if not WEATHER_API_KEY:
        speak("I can't check the weather because my weather API key isn't configured.")
        return False

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            speak(f"I couldn't find the city {city}.")
            return False

        response.raise_for_status()

        data = response.json()

        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        speak(
            f"The current weather in {city} is {weather_description}. "
            f"The temperature is {temperature:.0f} degrees Celsius, "
            f"and it feels like {feels_like:.0f} degrees. "
            f"Humidity is {humidity} percent."
        )

        return True

    except requests.RequestException as e:
        print(f"Weather API error: {e}")
        speak("Sorry, I couldn't retrieve the weather right now.")
        return False

    except (KeyError, ValueError) as e:
        print(f"Weather data error: {e}")
        speak("Sorry, I couldn't process the weather information.")
        return False

def answer_knowledge_question(text):
    text = text.lower()

    for topic, answer in knowledge_base.items():
        if topic in text:
            speak(answer)
            return True

    return False

def execute_custom_command(text):
    text = text.lower().strip()

    for command, details in custom_commands.items():
        if text == command.lower():
            command_type = details.get("type")
            target = details.get("target")

            if not target:
                print(f"Custom command '{command}' has no target.")
                return True

            print(f"DEBUG: Executing custom command: {command}")

            if command_type == "url":
                webbrowser.open_new_tab(target)
                speak(f"Opening {command}.")
                return True

            elif command_type == "program":
                try:
                    subprocess.Popen(target)
                    speak(f"Executing {command}.")
                except Exception as e:
                    print(f"Custom command error: {e}")
                    speak(f"Sorry, I couldn't open {command}.")

                return True

            else:
                print(f"Unknown custom command type: {command_type}")
                speak("Sorry, that custom command type is not supported.")
                return True

    return False

def extract_reminder_minutes(text):
    match = REMINDER_PATTERN.search(text)
    return int(match.group(1)) if match else None


def callback(recognizer, audio):
    global conversation_state, pending_data
    print(f"DEBUG: callback entered | state={conversation_state}")

    if is_speaking.is_set():
        print("DEBUG: Ignoring audio because Ghozal is speaking")
        return
    try:
        text = recognizer.recognize_google(audio)
        text = text.lower()

        if "abort" in text and conversation_state is not None:
            speak("Okay, cancelled.")
            conversation_state = None
            pending_data = {}
            return

        if conversation_state == "awaiting_weather_city":
            success = get_weather(text)

            if success:
                conversation_state = None
            else:
                speak("Please tell me another city.")

            return

        if conversation_state == "awaiting_search":
            speak(f"Searching for '{text}'...")
            conversation_state = None
            # Fix #3: URL-encode the spoken text before building the URL
            webbrowser.open_new_tab(f"https://www.google.com/search?q={quote_plus(text)}")
            return

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

        if conversation_state == "awaiting_reminder_message":
            pending_data["reminder_message"] = text
            speak("And in how many minutes?")
            conversation_state = "awaiting_reminder_minutes"
            return

        if conversation_state == "awaiting_reminder_minutes":
            minutes = extract_reminder_minutes(text)
            if minutes:
                set_reminder(minutes, pending_data["reminder_message"])
                conversation_state = None
                pending_data = {}
            else:
                retries = pending_data.get("retry_count", 0) + 1
                if retries >= 2:
                    speak("I'm still not catching a number, so I'll cancel this reminder for now.")
                    conversation_state = None
                    pending_data = {}
                else:
                    pending_data["retry_count"] = retries
                    speak("Sorry, I didn't catch a number. How many minutes?")
            return

        print(f"Recognized audio: {text}")
        print(f"DEBUG: Current state = {conversation_state}")
        if execute_custom_command(text):
            return

        intent = classify_intent(text)

        if intent == "greeting":
            speak("Hello to you too!")
        elif intent == "date":
            now = dt.date.today()
            speak(f"Today's date is {now.strftime('%d-%m-%Y')}.")
        elif intent == "time":
            now = dt.datetime.now()
            speak(f"The current time is {now.strftime('%H:%M:%S')}.")
        elif intent == "search":
            speak("What would you like to search for?")
            conversation_state = "awaiting_search"
        elif intent == "email":
            speak("Who should I send it to?")
            conversation_state = "awaiting_email_to"
        elif intent == "reminder":
            speak("What should I remind you about? Say abort at any point to cancel.")
            conversation_state = "awaiting_reminder_message"


        elif intent == "weather":
            print("DEBUG: Weather state set")
            conversation_state = "awaiting_weather_city"
            speak("Which city would you like the weather for?")
            print("DEBUG: Weather question finished")

        elif intent == "knowledge":
            print("DEBUG: Knowledge question detected")

            answered = answer_knowledge_question(text)

            if not answered:
                speak("Sorry, I don't know the answer to that yet.")

        elif intent == "chitchat" or intent == "unknown":
            pass  # not a command — say nothing rather than force a guess
    except sr.UnknownValueError:
        print("No understandable speech detected.")

_tts_lock = threading.Lock()


def speak(text):
    with _tts_lock:
        is_speaking.set()
        pythoncom.CoInitialize()

        engine = None

        try:
            print(f"TTS: {text}")

            engine = pyttsx3.init("sapi5")
            engine.setProperty("rate", 125)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")

            if voices:
                print(f"TTS voices found: {len(voices)}")
                print(f"Using voice: {voices[0].name}")
                engine.setProperty("voice", voices[0].id)

            engine.say(text)
            engine.runAndWait()

            print("TTS: finished")

        except Exception as e:
            print(f"TTS ERROR: {e}")

        finally:
            if engine is not None:
                try:
                    engine.stop()
                except Exception:
                    pass

            pythoncom.CoUninitialize()
            is_speaking.clear()
# --- Fix #6 (the "say it's listening" request) ---
# listen_in_background() owns its own internal loop and gives you no hook
# to know when it has actually started recording a phrase, so there's no
# clean way to print/say "Listening..." at the right moment with it.
# Switching to a manual loop that calls recognizer.listen() ourselves
# gives us that control, and as a side benefit it naturally avoids the
# assistant hearing itself: speak() blocks this same thread, so the loop
# simply isn't back at recognizer.listen() while it's talking.

stop_event = threading.Event()


def listen_loop():
    with mic as source:
        print("Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    recognizer.pause_threshold = 1.5
    print("Ghozal is ready.")

    while not stop_event.is_set():
        with mic as source:
            print("🎤 Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            except sr.WaitTimeoutError:
                continue
        try:
            callback(recognizer, audio)
        except Exception as e:
            print(f"callback error: {e}")


speak("Ghozal is starting.")

listener_thread = threading.Thread(
    target=listen_loop,
    daemon=True
)

listener_thread.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    stop_event.set()
