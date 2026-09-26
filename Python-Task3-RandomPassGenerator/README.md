# Password Generator

A desktop **Password Generator** built with **Python and PyQt5** that generates randomized passwords based on user-selected criteria.

The application uses Python's `secrets` module for password generation, provides configurable password length and character types, checks password strength, keeps a short generation history, and allows generated passwords to be copied to the clipboard.

## Features

* 🔐 Secure password generation using Python's `secrets` module
* 📏 Adjustable password length from **8 to 32 characters**
* 🔠 Uppercase letter support
* 🔡 Lowercase letter support
* 🔢 Digit support
* 🔣 Symbol support
* 👀 Option to exclude ambiguous characters
* 🛡️ Password strength evaluation
* 📋 Copy generated passwords to the clipboard
* 🕘 Keeps the **last 5 generated passwords** in memory
* 🎨 Dark-themed PyQt5 graphical interface
* ⚠️ Input validation and user feedback

## Tech Stack

* **Python**
* **PyQt5** — Desktop GUI
* **secrets** — Cryptographically secure random selection
* **string** — Built-in character sets
* **re** — Password strength pattern matching
* **pyperclip** — Clipboard interaction
* **sys** — Application execution

## Project Structure

```text
Password-Generator/
│
├── main.py
└── README.md
```

## How It Works

### 1. Password Length

The password length is controlled using a horizontal slider.

The available range is:

```text
8 - 32 characters
```

The selected length is displayed dynamically above the slider.

### 2. Password Criteria

Users can select from four character types:

* **Upper Letters**
* **Lower Letters**
* **Digits**
* **Symbols**

At least **two character types** must be selected before generating a password.

For example:

```text
✓ Upper Letters
✓ Lower Letters
✗ Digits
✓ Symbols
```

is valid.

However:

```text
✓ Lower Letters
✗ Upper Letters
✗ Digits
✗ Symbols
```

will result in an error.

The application displays:

```text
Error: Select atleast two types
```

## Password Generation

The generator creates character pools based on the selected criteria.

### Uppercase

Uses:

```python
string.ascii_uppercase
```

which provides:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

### Lowercase

Uses:

```python
string.ascii_lowercase
```

which provides:

```text
abcdefghijklmnopqrstuvwxyz
```

### Digits

Uses:

```python
string.digits
```

which provides:

```text
0123456789
```

### Symbols

Uses:

```python
string.punctuation
```

which provides Python's standard punctuation character set.

## Ensuring Selected Character Types

The generator does more than randomly select characters from one combined pool.

It first guarantees that **at least one character from every selected character type** appears in the generated password.

For example, if the user selects:

```text
✓ Upper Letters
✓ Lower Letters
✓ Digits
✓ Symbols
```

the initial password contains at least:

```text
1 uppercase
1 lowercase
1 digit
1 symbol
```

The remaining characters are then randomly selected from the combined character pool.

Finally, the characters are shuffled before the password is returned.

This prevents a situation where the user selects multiple character categories but random selection happens to produce a password containing only one or two of them.

## Secure Randomness

Password generation uses Python's built-in `secrets` module:

```python
secrets.choice(...)
```

and:

```python
secrets.SystemRandom().shuffle(...)
```

The `secrets` module is designed for generating random values suitable for security-sensitive applications, making it more appropriate for password generation than ordinary pseudo-random functions such as `random.choice()`.

## Excluding Ambiguous Characters

The application includes an **Exclude Ambigious** option.

When enabled, the following characters are removed from the available character pools:

```text
0 O I l 1 5 S
```

This can make passwords easier to visually distinguish, particularly when manually reading or typing them.

For example, visually similar characters such as:

```text
0 / O
1 / I / l
5 / S
```

will not appear when the option is enabled.

> Note: The UI currently spells this option as `Exclude Ambigious`; the conventional spelling is `Exclude Ambiguous`.

## Password Strength Checker

After generating a password, the application evaluates its strength using several characteristics.

The scoring system checks:

### Password Length

Passwords with at least 12 characters receive more points.

```text
12+ characters → 2 points
Below 12 → 1 point
```

### Lowercase Letters

```text
Contains lowercase → +1
```

### Uppercase Letters

```text
Contains uppercase → +1
```

### Digits

```text
Contains a digit → +1
```

### Symbols

```text
Contains a symbol → +1
```

### Strength Ratings

The resulting score determines the displayed rating:

|   Score | Rating |
| ------: | ------ |
|       6 | Strong |
|     4–5 | Medium |
| Below 4 | Weak   |

The rating is also displayed with a corresponding visual indicator in the application.

## Generation History

Every generated password is temporarily stored in an in-memory list.

The application keeps a maximum of **five passwords**:

```text
Password 5
Password 4
Password 3
Password 2
Password 1
```

The newest generated password is placed at the top of the history.

When a sixth password is generated, the oldest entry is removed.

### Important

The history is **not persisted to a database or file**.

It exists only while the application is running and is cleared when the application closes.

## Copy to Clipboard

The **Copy to Clipboard** button uses the `pyperclip` library.

To copy a password:

1. Generate one or more passwords.
2. Select a password from the generation history.
3. Click **Copy to Clipboard**.
4. The selected password is copied to the system clipboard.

The button only becomes available after passwords have been generated.

## Installation

### Prerequisites

Make sure Python is installed:

```bash
python --version
```

### Install Dependencies

Install the required external packages:

```bash
pip install PyQt5 pyperclip
```

The following modules are included with Python's standard library and require no separate installation:

* `re`
* `secrets`
* `string`
* `sys`

### Run the Application

```bash
python main.py
```

The Password Generator window should open.

## Usage

### Generate a Password

1. Select the desired password length using the slider.
2. Select at least two password criteria.
3. Optionally enable **Exclude Ambigious**.
4. Click **Generate**.
5. The generated password will appear in the history.
6. The application will display its calculated strength.

### Copy a Password

1. Select a password from the history list.
2. Click **Copy to Clipboard**.
3. The selected password is copied to the system clipboard.

## Example

A user might select:

```text
Length: 16

✓ Upper Letters
✓ Lower Letters
✓ Digits
✓ Symbols
✓ Exclude Ambigious
```

The generator will:

1. Build the selected character pools.
2. Remove ambiguous characters.
3. Select at least one character from each selected category.
4. Fill the remaining characters randomly.
5. Shuffle the password.
6. Return the final password.
7. Evaluate its strength.
8. Add it to the generation history.

## Security Considerations

The application uses `secrets` rather than Python's standard `random` module for generating password characters.

However, this project should still be considered a **personal/educational password generator** rather than a complete password-management solution.

In particular:

* Generated passwords are stored temporarily in application memory.
* The five-password history remains visible in the application.
* Copying a password places it in the system clipboard.
* Passwords are not encrypted or stored securely.
* The application does not provide password vault functionality.

For sensitive passwords, users should avoid leaving them visible in the application's history or clipboard longer than necessary.

## Future Improvements

Potential improvements include:

* Add a **Clear History** button
* Add a dedicated password display field
* Automatically clear the clipboard after a configurable period
* Add a password visibility toggle
* Allow users to exclude custom characters
* Add configurable minimum requirements for each character type
* Improve the password strength algorithm
* Add entropy estimation
* Add a secure password vault
* Encrypt stored passwords if persistent storage is introduced
* Add application settings
* Add a standalone executable build
* Add automated unit tests
* Improve accessibility and keyboard navigation

## Disclaimer

This project is intended for educational and personal use. Although it uses Python's `secrets` module for cryptographically secure random selection, the application does not provide the complete security features of a dedicated password manager.

## License

This project is available for educational and personal use. Add an appropriate open-source license if you intend to distribute the project publicly.
