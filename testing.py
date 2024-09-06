from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QComboBox, QHBoxLayout
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle('Invert Button Color Example')

        # Set layout
        self.widget = QWidget()
        layout = QHBoxLayout()

        # Create a button
        self.combo = QComboBox()
        self.ref = QPushButton("Reference")
        self.button = QPushButton('Generate CSV', self)

        # Set the style sheet to invert the button's colors
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                padding: 3px 18px 5px 18px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)

        layout.addWidget(self.combo)
        layout.addWidget(self.ref)
        layout.addWidget(self.button)

        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)


# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
