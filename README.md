# Oasis Infobyte Internship — Python Projects

A collection of **Python desktop applications developed as part of the Oasis Infobyte Internship**.

This repository contains three projects built while completing the internship tasks, with a focus on Python programming, GUI development, application logic, data handling, security, APIs, and user interaction.

## Projects

| Project                   | Description                                                                                                                         | Main Technologies                     |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| 🎤 **Ghozal Assistant**   | Voice-controlled desktop assistant with speech recognition, text-to-speech, reminders, weather, web search, and extensible commands | Python, Speech Recognition, TTS, APIs |
| 🧮 **BMI Calculator**     | Desktop BMI calculator with local record storage and BMI trend visualization                                                        | Python, PyQt5, SQLite, Matplotlib     |
| 🔐 **Password Generator** | Configurable password generator with secure random generation, strength checking, and clipboard support                             | Python, PyQt5, `secrets`, Pyperclip   |

---

# About the Internship

These projects were developed as part of the **Oasis Infobyte Internship Program**, with the goal of applying Python programming concepts to practical application development.

Throughout the projects, different areas of Python development were explored, including:

* GUI application development
* Object-oriented programming
* Database management
* Data visualization
* API integration
* Speech recognition and text-to-speech
* Regular expressions
* Secure random generation
* Input validation
* Exception handling

The projects progressively demonstrate different ways Python can be used to build functional desktop applications.

---

# 1. 🎤 Ghozal Assistant

**Ghozal Assistant** is a Python-based voice assistant designed to interact with users through speech.

The assistant recognizes spoken commands, processes the user's intent, performs supported tasks, and responds using text-to-speech.

## Features

* 🎙️ Voice input and speech recognition
* 🔊 Text-to-speech responses
* 👋 Greeting and conversational commands
* 🌤️ Weather information
* 🔎 Web/search-based information retrieval
* ⏰ Reminders
* 🧠 General knowledge question answering
* ⚙️ Custom commands
* 🗣️ Natural-language intent recognition
* ⚠️ Speech recognition error handling
* 🔐 Privacy considerations and documentation

The assistant is designed with an extensible command structure so additional functionality can be added over time.

### Example Interactions

```text
User: What's the weather today?
Ghozal: [Provides weather information]

User: Set a reminder for 6 PM.
Ghozal: [Creates the reminder]

User: What's the capital of France?
Ghozal: [Provides the answer]
```

### Concepts Demonstrated

* Speech recognition
* Text-to-speech
* Natural-language processing
* Intent recognition
* API integration
* Command routing
* Error handling
* Extensible application design

For complete installation instructions, supported commands, configuration, and privacy information, see the README inside the Ghozal Assistant directory.

---

# 2. 🧮 BMI Calculator

A desktop BMI calculator developed using **Python and PyQt5**.

The application calculates BMI from a user's weight and height, stores calculations locally using SQLite, and allows the user to visualize BMI history over time.

## Features

* Calculate BMI
* First-name based record tracking
* Weight input in kilograms
* Height input in meters
* Automatic BMI categorization
* Local SQLite database
* Automatic calculation dates
* BMI history lookup
* BMI trend visualization
* Input validation
* Dark-themed GUI

## BMI Formula

```text
BMI = weight (kg) / height² (m)
```

The application uses these categories:

|         BMI | Category    |
| ----------: | ----------- |
|  Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal      |
| 25.0 – 29.9 | Overweight  |
|       30.0+ | Obese       |

## Data Storage

BMI records are stored locally in:

```text
records.db
```

The database contains:

```text
id
name
BMI
date
```

The database is automatically initialized when the application starts.

## BMI History

The **Graphs** tab allows users to enter a name and view previously recorded BMI values.

The graph displays:

```text
X-axis → Date
Y-axis → BMI
```

This provides a simple visualization of BMI changes across multiple records.

## Technologies

* Python
* PyQt5
* SQLite3
* Matplotlib
* datetime

---

# 3. 🔐 Password Generator

A desktop password generator developed using **Python and PyQt5**.

The application generates passwords based on user-selected criteria and uses Python's `secrets` module for secure random character selection.

## Features

* 🔐 Secure random password generation
* 📏 Password length from **8 to 32 characters**
* 🔠 Uppercase letters
* 🔡 Lowercase letters
* 🔢 Digits
* 🔣 Symbols
* 👀 Optional ambiguous-character exclusion
* 🛡️ Password strength rating
* 📋 Copy to clipboard
* 🕘 Last 5 generated passwords
* 🎨 Dark-themed GUI

## Password Generation

Users can select the character types they want to include.

At least **two character types** must be selected.

The generator guarantees that each selected character type appears at least once before filling the remaining characters from the combined character pool.

The resulting password is then shuffled.

## Secure Randomness

The application uses:

```python
secrets.choice()
```

and:

```python
secrets.SystemRandom().shuffle()
```

instead of Python's standard `random` module.

This provides a stronger random-generation mechanism appropriate for password generation.

## Ambiguous Characters

The **Exclude Ambigious** option removes visually similar characters such as:

```text
0 O I l 1 5 S
```

from the available character pools.

> The current UI uses the spelling `Ambigious`; the conventional spelling is `Ambiguous`.

## Password Strength

The generated password is evaluated using:

* Password length
* Lowercase letters
* Uppercase letters
* Digits
* Symbols

The application displays one of three ratings:

```text
Strong
Medium
Weak
```

This is a simple heuristic and is not intended to be a complete password entropy or security analysis.

## Generation History

The application keeps the latest **five generated passwords** in memory.

The history is not stored permanently and is cleared when the application closes.

## Technologies

* Python
* PyQt5
* `secrets`
* `string`
* `re`
* Pyperclip

---

# Repository Structure

The repository is organized into individual internship projects:

```text
OIBSIP/
│
├── Ghozal Assistant/
│   ├── main.py
│   ├── ...
│   └── README.md
│
├── BMI Calculator/
│   ├── main.py
│   ├── records.db
│   └── README.md
│
├── Password Generator/
│   ├── main.py
│   └── README.md
│
└── README.md
```

The exact folder and file names may vary depending on the final repository structure.

---

# Installation

Each project may have different dependencies.

It is recommended to install the dependencies for the specific project you want to run.

## Requirements

* Python 3.x
* pip

Check your Python installation:

```bash
python --version
```

## BMI Calculator

Install dependencies:

```bash
pip install PyQt5 matplotlib
```

Run:

```bash
python main.py
```

## Password Generator

Install dependencies:

```bash
pip install PyQt5 pyperclip
```

Run:

```bash
python main.py
```

## Ghozal Assistant

Ghozal Assistant uses additional dependencies depending on its enabled functionality.

Refer to the **Ghozal Assistant README** for its complete setup instructions.

---

# Skills Demonstrated

These projects provided practical experience with several areas of software development.

### Python

* Functions
* Classes
* Object-oriented programming
* Modules and packages
* Exception handling
* Regular expressions
* File and data handling

### GUI Development

Using PyQt5:

* Windows
* Layouts
* Buttons
* Labels
* Input fields
* Checkboxes
* Sliders
* Lists
* Tabs
* Event handling
* Custom styling

### Databases

The BMI Calculator demonstrates:

* SQLite database creation
* Table creation
* SQL queries
* Parameterized queries
* Data insertion
* Data retrieval
* Transaction handling

### Data Visualization

Matplotlib is used to visualize BMI history and trends.

### Security

The Password Generator demonstrates the use of Python's `secrets` module for security-sensitive random generation.

### APIs & Automation

Ghozal Assistant demonstrates:

* API integration
* Web-based information retrieval
* Speech processing
* Text-to-speech
* Automated command execution

---

# Learning Objectives

The main goal of these projects was to move from basic Python programming toward building complete, interactive applications.

Through the internship, the projects provided practical experience in:

* Designing desktop applications
* Connecting user interfaces to application logic
* Managing local data
* Working with external services
* Handling user input
* Implementing security-conscious functionality
* Debugging Python applications
* Structuring larger Python projects
* Documenting software projects

---

# Future Improvements

Potential improvements across the repository include:

* Add automated unit and integration tests
* Improve project modularity
* Add consistent logging
* Improve GUI accessibility
* Package applications as standalone executables
* Add screenshots and demonstrations
* Improve error handling and user feedback
* Add CI/CD workflows
* Expand application functionality
* Improve documentation for individual projects

Individual project READMEs contain additional project-specific improvements.

---

# Internship

**Program:** Oasis Infobyte Internship
**Domain:** Python Development
**Repository:** Python Internship Projects

This repository contains the practical projects developed during the internship to demonstrate the application of Python programming concepts in real-world-style applications.

---

# License

These projects were developed for educational and internship purposes.

If this repository is distributed publicly, an appropriate open-source license can be added according to the intended usage and distribution terms.
