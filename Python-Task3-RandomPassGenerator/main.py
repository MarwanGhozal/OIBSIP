import re
import secrets 
import string
import sys 
import pyperclip

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLineEdit,  QLabel, QCheckBox, QVBoxLayout, QSlider, QListWidget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.passwords = []
        self.setStyleSheet("""
           QMainWindow {
                background-color: #1e1e2e;
            }

            QLabel {
                color: white;
                font-size: 14px;
            }

            QCheckBox {
                color: white;
                font-size: 14px;
            }
            QListWidget {
                background-color: #313244;
                color: white;
                border: 2px solid #45475a;
                border-radius: 10px;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit {
                background-color: #313244;
                color: white;
                border: 2px solid #45475a;
                border-radius: 10px;
                padding: 10px;
                font-size: 15px;
            }

            QLineEdit:focus {
                border: 2px solid #89b4fa;
            }

            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #74a8f7;
            }

            QPushButton:pressed {
                background-color: #5c8ed6;
            }                

""")


        self.setWindowTitle("Password Generator")

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.length_label = QLabel(f"Length: 8")
        self.length_input = QSlider(Qt.Horizontal)
        self.length_input.setRange(8, 32)
        self.length_input.valueChanged.connect(self.length_changed)

        self.criteria_label = QLabel("Password Criteria:")
        self.use_upper = QCheckBox("Upper Letters")

        self.use_lower = QCheckBox("Lower Letters")
        
        self.use_numbers = QCheckBox("Digits")

        self.use_symbols = QCheckBox("Symbols")

        self.exclude_ambigious = QCheckBox("Exclude Ambigious")

        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_password)

        self.result_label = QLabel()
        # self.result_input = QLineEdit()
        # self.result_input.setReadOnly(True)
        self.feedback_label = QLabel()

        self.CopyToClipBtn =  QPushButton("Copy to Clipboard")
        self.CopyToClipBtn.clicked.connect(self.copy_password)
        self.CopyToClipBtn.hide()

        self.history_label = QLabel("Generation History:")
        self.history_list = QListWidget()
        self.history_label.hide()
        self.history_list.hide()

        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.criteria_label)
        layout.addWidget(self.use_upper)
        layout.addWidget(self.use_lower)
        layout.addWidget(self.use_numbers)
        layout.addWidget(self.use_symbols)
        layout.addWidget(self.exclude_ambigious)

        layout.addWidget(self.generate_btn)
        layout.addWidget(self.result_label)
        # layout.addWidget(self.result_input)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)
        layout.addWidget(self.feedback_label)
        layout.addWidget(self.CopyToClipBtn)

        # self.result_input.hide()
    def copy_password(self):
        selected = self.history_list.currentItem()

        if selected:
            pyperclip.copy(selected.text())

    def length_changed(self, i ):
        length = i
        self.length_label.setText(f"Length : {length}")

    def generate_password(self):

        length = self.length_input.value()

        use_upper = self.use_upper.isChecked()
        use_lower = self.use_lower.isChecked()
        use_numbers = self.use_numbers.isChecked()
        use_symbols = self.use_symbols.isChecked()
        exclude_ambigious = self.exclude_ambigious.isChecked()
        selected_types = sum((use_upper, use_lower, use_numbers, use_symbols))
        if selected_types < 2:
            self.feedback_label.hide()
            # self.result_input.hide()
            self.CopyToClipBtn.hide()
            
            self.result_label.setStyleSheet(("color: red; font-weight: bold"))
            self.result_label.setText("Error: Select atleast two types")
            self.result_label.show()
            return

        self.password = generate_random_password(length, use_upper, use_lower, use_numbers, use_symbols, exclude_ambigious)
        self.passwords.insert(0, self.password)
        if len(self.passwords) > 5:
            self.passwords.pop()

        self.history_list.clear()

        for password in self.passwords:
            self.history_list.addItem(password)
        self.history_label.show()
        self.history_list.show()
        # self.result_input.setText(self.password)
        # self.result_input.show()
        self.CopyToClipBtn.show()
        strength, color = check_password_strength(self.password)
        self.feedback_label.setText(
            f'<b>Password Strength : <span style="color: {color}">{strength}</span>')
        self.feedback_label.show()
        self.result_label.hide()
        




def generate_random_password(length, use_upper, use_lower, use_numbers, use_symbols, exclude_ambigious):

    selected_pools = []
    if use_upper:
        selected_pools.append(string.ascii_uppercase)
    if use_lower:
        selected_pools.append(string.ascii_lowercase)
    if use_numbers: 
        selected_pools.append(string.digits)
    if use_symbols:
         selected_pools.append(string.punctuation)

    if exclude_ambigious:
        ambigious_characters = "0OIl15S"
        cleaned_pools = []
        for pool in selected_pools:
            cleaned_pool = "".join([c for c in pool if c not in ambigious_characters])
            if cleaned_pool:
                cleaned_pools.append(cleaned_pool)
        selected_pools = cleaned_pools

    #We need to make the selected pool into a list to ensure we use every type picked, not just a random string where we pick random characters from, this might cause a password of 8 A even though the user selected to use symbols.
    
    password = [secrets.choice(pool) for pool in selected_pools]
    pool = ''.join(selected_pools)
    for _ in range (length-len(password)):
        password += secrets.choice(pool)
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    else:
        score += 1
    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score >= 6:
        color = "green"
        rating = "Strong"
    elif score >= 4:
        color = "orange"
        rating = "Medium"
    else: 
        color = "red"
        rating = "Weak"

    return rating, color

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        