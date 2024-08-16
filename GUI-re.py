import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QListView, QSplitter, QStyledItemDelegate
from PyQt5.QtCore import Qt
from Inbox import Inbox
from MailView import MailView


class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Papa Airbnb")

        # Inbox Widget
        self.inbox = Inbox(data)

        # Mail View Widget
        self.mail_view = MailView()

        # Splitter View
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.inbox)
        splitter.addWidget(self.mail_view)
        splitter.setSizes([1000, 1000])

        self.setCentralWidget(splitter)


def load_email_data(filename="email_data.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        email_data_list = json.load(file)
    print(f"Email data loaded from {filename}")
    return email_data_list


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Get data
    data = load_email_data()

    window = MainWindow(data)
    window.show()
    # Start event loop
    app.exec_()
