import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout)

#  while True:
#     try:
#         weight = float(input('Please enter your weight in kilograms: '))
#         height = float(input('Please enter your height in meters: '))
#         if weight <= 0 or height <= 0:
#             print("Weight and height must be positive numbers. Please try again.")
#             continue
#         break
#     except ValueError:
#         print("Invalid input. Please enter numeric values for weight and height.")
        
# BMI = weight / (height ** 2)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }

            QLabel {
                color: white;
                font-size: 14px;
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
        self.setFixedSize(QSize(400, 250))
        self.setWindowTitle("BMI Calculator")

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.weight_input = QLineEdit()
        self.height_input = QLineEdit()
        self.calculate_btn = QPushButton("Calculate")
        self.result_label = QLabel()

        layout.addWidget(QLabel("Weight (kg):"))
        layout.addWidget(self.weight_input)

        layout.addWidget(QLabel("Height (m):"))
        layout.addWidget(self.height_input)

        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.result_label)        
        self.result_label.setAlignment(Qt.AlignCenter)
        self.calculate_btn.clicked.connect(self.calculate_bmi)
    def calculate_bmi(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            if weight <= 0 or height <= 0:
                self.result_label.setStyleSheet("color: red; font-weight: bold")
                self.result_label.setText("Weight and height must be positive numbers. Please try again.")
                return
            BMI = weight / (height ** 2)
            if BMI < 18.5:
                result = "Underweight"
                color = "orange"
            elif BMI < 25.0:
                result = "Normal"
                color = "green"
            elif BMI < 30.0:
                result = "Overweight"
                color = "orange"
            else:
                result = "Obese"
                color = "red"
            self.result_label.setText(
                f'Your BMI is <b>{BMI:.2f}</b><br>'
                f'You are <b><span style="color: {color};">{result}</span></b>'
            )
        except ValueError:
            self.result_label.setStyleSheet("color: red; font-weight: bold")
            self.result_label.setText("Please enter invalid numbers.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        