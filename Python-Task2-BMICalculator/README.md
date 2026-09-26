# BMI Calculator

A simple desktop **BMI Calculator** built with **Python, PyQt5, SQLite, and Matplotlib**.

The application allows users to calculate their Body Mass Index (BMI), automatically save each calculation locally, and visualize BMI history over time through a graph.

## Features

* 🧮 Calculate BMI using weight and height
* 👤 Store BMI records by first name
* 💾 Persist records locally using SQLite
* 📊 Visualize BMI history with Matplotlib
* 📅 Automatically record the calculation date
* ⚠️ Input validation and error handling
* 🎨 Dark-themed PyQt5 graphical interface
* 📑 Separate tabs for the calculator and BMI graphs

## Tech Stack

* **Python**
* **PyQt5** — Desktop GUI
* **SQLite3** — Local database storage
* **Matplotlib** — BMI trend visualization
* **datetime** — Calculation date tracking

## Project Structure

```text
BMI-Calculator/
│
├── main.py
├── records.db
└── README.md
```

> `records.db` is created automatically when the application runs for the first time, so it does not need to be manually created.

## How It Works

### 1. BMI Calculation

The application uses the standard BMI formula:

```text
BMI = weight (kg) / height² (m)
```

For example, a person weighing 80 kg with a height of 1.80 m:

```text
BMI = 80 / (1.80²)
BMI = 24.69
```

The application then categorizes the result as:

| BMI           | Category    |
| ------------- | ----------- |
| Below 18.5    | Underweight |
| 18.5 – 24.9   | Normal      |
| 25.0 – 29.9   | Overweight  |
| 30.0 or above | Obese       |

These categories are based on the thresholds implemented in the application.

### 2. Local Data Storage

Every successful calculation is stored in a local SQLite database.

The database contains a `bmi` table with the following fields:

```sql
CREATE TABLE bmi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    BMI REAL NOT NULL,
    date TEXT NOT NULL
);
```

Each record contains:

* `id` — Automatically generated record ID
* `NAME` — User's first name
* `BMI` — Calculated BMI value
* `date` — Date of the calculation

### 3. BMI History Graph

The **Graphs** tab allows the user to enter a previously used name.

The application retrieves all BMI records associated with that name and displays them as a line graph:

* X-axis → Date
* Y-axis → BMI
* Individual calculations → Displayed as points
* Multiple records → Connected to show the BMI trend

This makes it possible to track how a user's BMI changes over time.

## Input Validation

The application handles several invalid input scenarios.

### Missing Name

If the name field is empty:

```text
Name is missing. Please enter your first name.
```

### Invalid Weight or Height

If weight or height cannot be converted to a number:

```text
Please enter valid numbers.
```

### Non-positive Values

Weight and height must be greater than zero:

```text
Weight and height must be positive numbers. Please try again.
```

### Missing Graph Name

If no name is entered in the Graphs tab:

```text
Name is missing. Please enter the first name.
```

### Name Without Records

If the entered name does not have any stored BMI calculations:

```text
Name not found. Please enter a name with BMI records.
```

SQLite errors are also caught and displayed to the user.

## Installation

### Prerequisites

Make sure Python is installed on your system.

You can check your Python version with:

```bash
python --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bmi-calculator.git
cd bmi-calculator
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install PyQt5 matplotlib
```

`sqlite3`, `sys`, `os`, and `datetime` are part of Python's standard library and do not require separate installation.

### 3. Run the Application

```bash
python main.py
```

The application window should open with two tabs:

```text
Calculator | Graphs
```

## Usage

### Calculate BMI

1. Open the **Calculator** tab.
2. Enter your first name.
3. Enter your weight in kilograms.
4. Enter your height in meters.
5. Click **Calculate**.
6. Your BMI and corresponding category will be displayed.
7. The calculation is automatically saved to the local database.

### View BMI History

1. Open the **Graphs** tab.
2. Enter the same name used when saving BMI records.
3. Click **Show Graph**.
4. A Matplotlib window will display the BMI trend.

## Example

Suppose the following records have been saved:

```text
Name: Marwan
Weight: 86 kg
Height: 1.83 m
```

The application calculates:

```text
BMI = 86 / (1.83²)
BMI ≈ 25.68
```

The result is displayed in the application and saved to `records.db`.

If multiple records exist for the same name, the **Graphs** tab can visualize the changes between those calculations.

## Database

The SQLite database is stored in the same directory as the Python script:

```text
records.db
```

The path is generated using:

```python
db_path = os.path.join(os.path.dirname(__file__), "records.db")
```

This means the database is stored alongside the application rather than relying on the current working directory.

## Design

The application uses a dark user interface implemented with PyQt5 stylesheets.

The interface consists of two main tabs:

### Calculator

Contains:

* First name input
* Weight input
* Height input
* Calculate button
* BMI result display

### Graphs

Contains:

* Name search field
* Show Graph button
* Error/status messages
* Matplotlib BMI trend visualization

## Error Handling

The application includes error handling for:

* Invalid numeric input
* Empty input fields
* Negative or zero measurements
* Missing database records
* SQLite database errors
* Database transaction rollback after database insertion errors

This prevents common user-input and database errors from terminating the application unexpectedly.

## Future Improvements

Potential improvements include:

* Add weight and height units selection
* Add the ability to delete or edit records
* Display BMI history directly inside the PyQt5 interface
* Add more detailed statistics such as average BMI
* Improve graph date formatting
* Add user profiles instead of relying only on names
* Prevent duplicate records for accidental repeated submissions
* Add data export to CSV
* Package the application as a standalone executable
* Add automated tests
* Improve database architecture by separating database operations from the GUI logic

## Disclaimer

BMI is a general screening measurement and does not directly measure body fat or overall health. The BMI categories used by this application are intended for informational purposes only and should not be treated as a medical diagnosis.

## License

This project is available for educational and personal use. Add an appropriate open-source license if you intend to distribute the project publicly.
