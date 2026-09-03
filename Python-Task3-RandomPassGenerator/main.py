import random
import string
import sys 
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLineEdit,  QLabel, QCheckBox, QVBoxLayout, QSlider)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
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

        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_password)

        self.result_label = QLabel()
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)


        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.criteria_label)
        layout.addWidget(self.use_upper)
        layout.addWidget(self.use_lower)
        layout.addWidget(self.use_numbers)
        layout.addWidget(self.use_symbols)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_input)


    def length_changed(self, i ):
        length = i
        self.length_label.setText(f"Length : {length}")

    def generate_password(self):
        length = self.length_input.value()

        use_upper = self.use_upper.isChecked()
        use_lower = self.use_lower.isChecked()
        use_numbers = self.use_numbers.isChecked()
        use_symbols = self.use_symbols.isChecked()

        selected_types = sum((use_upper, use_lower, use_numbers, use_symbols))
        if selected_types < 2:
            self.result_label.setText("Error: Select atleast two types")
            return

        password = generate_random_password(length, use_upper, use_lower, use_numbers, use_symbols)
        self.result_input.setText(password)
        self.result_label.hide()
        




def generate_random_password(length, use_upper, use_lower, use_numbers, use_symbols):

    selected_pools = []
    if use_upper:
        selected_pools.append(string.ascii_uppercase)
    if use_lower:
        selected_pools.append(string.ascii_lowercase)
    if use_numbers: 
        selected_pools.append(string.digits)
    if use_symbols:
         selected_pools.append(string.punctuation)

    #We need to make the selected pool into a list to ensure we use every type picked, not just a random string where we pick random characters from, this might cause a password of 8 A even though the user selected to use symbols.

    password = [random.choice(pool) for pool in selected_pools]
    pool = ''.join(selected_pools)
    password += random.choices(pool, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()        