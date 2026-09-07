import sys
import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QTabWidget)

import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

try:
    db_path = os.path.join(os.path.dirname(__file__), "records.db")
    db = sqlite3.connect(db_path)
    db.execute('''CREATE TABLE IF NOT EXISTS bmi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    BMI REAL NOT NULL,
    date TEXT NOT NULL);''')
    db.commit()
except sqlite3.Error as e:
    print(f"Database initialization error: {e}")
    sys.exit()    

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
            QTabWidget::pane { 
                border: none; 
            }
            QTabBar::tab {
                background: #313244;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #89b4fa;
                color: #1e1e2e;
            }            
        """)        
        # self.setFixedSize(QSize(400, 250))
        self.setWindowTitle("BMI Calculator")

        # Initialize Tab Manager
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1
        calc_layout = QVBoxLayout()
        self.calc_tab = QWidget()
        self.calc_tab.setLayout(calc_layout)


        self.name_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.height_input = QLineEdit()
        self.calculate_btn = QPushButton("Calculate")
        self.result_label = QLabel()

        calc_layout.addWidget(QLabel("First Name:"))
        calc_layout.addWidget(self.name_input)

        calc_layout.addWidget(QLabel("Weight (kg):"))
        calc_layout.addWidget(self.weight_input)

        calc_layout.addWidget(QLabel("Height (m):"))
        calc_layout.addWidget(self.height_input)

        calc_layout.addWidget(self.calculate_btn)
        calc_layout.addWidget(self.result_label)       

        self.result_label.setAlignment(Qt.AlignCenter)
        self.calculate_btn.clicked.connect(self.calculate_bmi)

        #Tab 2
        self.graph_tab = QWidget()
        graph_layout = QVBoxLayout()
        self.graph_tab.setLayout(graph_layout)

        self.searchFor_input = QLineEdit()
        self.graph_btn = QPushButton("Show Graph")
        self.error_label = QLabel()

        graph_layout.addWidget(QLabel("Name: "))
        graph_layout.addWidget(self.searchFor_input)
        graph_layout.addWidget(self.graph_btn)
        graph_layout.addWidget(self.error_label)
        self.graph_btn.clicked.connect(self.show_graph)

        # Inject the tabs
        self.tabs.addTab(self.calc_tab, "Calculator")
        self.tabs.addTab(self.graph_tab, "Graphs")

    def show_graph(self):
        try:
            self.error_label.clear()
            searchFor = self.searchFor_input.text().strip()
            if not searchFor.strip():
                self.error_label.setStyleSheet("color: red; font-weight: bold")
                self.error_label.setText("Name is missing. Please enter the first name.")
                return       

            cursor = db.execute('''SELECT date, BMI FROM bmi WHERE NAME = ? ORDER BY date''', (searchFor,))
            x = []
            y = []
            for i in cursor:
                x.append(i[0]) #date
                y.append(i[1]) #BMI

            if not x:
                self.error_label.setStyleSheet("color: red; font-weight: bold")
                self.error_label.setText("Name not found. Please enter a name with BMI records.")
                return
            self.error_label.clear()
            plt.plot(x, y, marker="o")
            plt.title(f"BMI Trend for {searchFor}")
            plt.xlabel("Date")
            plt.ylabel("BMI")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except sqlite3.Error as e:
            self.error_label.setStyleSheet("color: red; font-weight: bold")
            self.error_label.setText(f"SQL ERROR: {e}")


        
    def calculate_bmi(self):
        try:
            name = self.name_input.text()
            if not name.strip():
                self.result_label.setStyleSheet("color: red; font-weight: bold")
                self.result_label.setText("Name is missing. Please enter your first name.")
                return
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            if weight <= 0 or height <= 0:
                self.result_label.setStyleSheet("color: red; font-weight: bold")
                self.result_label.setText("Weight and height must be positive numbers. Please try again.")
                return
            BMI = weight / (height ** 2)
            date = datetime.now().strftime("%Y-%m-%d")
            user_data = (name, BMI, date)
            db.execute('''INSERT INTO bmi(name, bmi, date) VALUES(?, ?, ?)''', user_data)
            db.commit()       
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
            self.result_label.setText("Please enter valid numbers.")
        except sqlite3.Error as e:
            self.result_label.setStyleSheet("color: red; font-weight: bold")
            self.result_label.setText(f"SQL ERROR: {e}")
            db.rollback()
            return         

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        