import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QListWidget, QDockWidget
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email Client")
        layout = QVBoxLayout()
        header_layout = self.build_header()
        body_layout = self.build_body()

        layout.addLayout(header_layout)
        layout.addLayout(body_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        inbox_dock_widget = MailInboxDW()
        self.addDockWidget(Qt.RightDockWidgetArea, inbox_dock_widget)

    def build_header(self):
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)
        sender_info_layout = QHBoxLayout()
        subject_layout = QHBoxLayout()

        # Date
        date_label = QLabel("Date")
        date_output = QLineEdit("")

        sender_label = QLabel("From")
        sender_output = QLineEdit("")

        subject_label = QLabel("Subject")
        subject_output = QLineEdit("")

        sender_info_layout.addWidget(date_label)
        sender_info_layout.addWidget(date_output)
        sender_info_layout.addWidget(sender_label)
        sender_info_layout.addWidget(sender_output)

        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(subject_output)

        header_layout.addLayout(sender_info_layout)
        header_layout.addLayout(subject_layout)

        return header_layout

    def build_body(self):
        body_layout = QVBoxLayout()
        content_output = QPlainTextEdit("")
        body_layout.addWidget(content_output)

        return body_layout


class MailContentDW(QDockWidget):
    def __init__(self):
        super().__init__()


class MailContent(QWidget):
    def __init__(self):
        super().__init__()


class MailInboxDW(QDockWidget):
    def __init__(self):
        super().__init__()

        self.widget = MailInbox()
        self.setWidget(self.widget)
        self.setFloating(False)


class MailInbox(QListWidget):
    def __init__(self):
        super().__init__()

        self.addItems(["One", "Two", "Three"])
        self.currentItemChanged.connect(self.index_changed)
        self.currentTextChanged.connect(self.text_changed)

    def index_changed(self, i):
        print(i.text())

    def text_changed(self, s):
        print(s)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Start event loop
    app.exec_()
