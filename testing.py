import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QLabel, QHBoxLayout, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Email Client")

        # Create the QListWidget
        list_widget = QListWidget()

        # Add custom widgets to the QListWidget
        for email in data:
            item_widget = ListItem(
                email['subject'], email['from'], email['date'])
            list_item = QListWidgetItem(list_widget)

            # Set size hint to ensure the item widget is displayed properly
            list_item.setSizeHint(item_widget.sizeHint())

            # Add the widget to the QListWidget
            list_widget.setItemWidget(list_item, item_widget)

        # Set the QListWidget as the central widget
        self.setCentralWidget(list_widget)


class ListItem(QWidget):
    def __init__(self, subject, sender, date):
        super().__init__()

        layout = QHBoxLayout()
        subject_label = QLabel(subject)
        sender_label = QLabel(sender)
        date_label = QLabel(date)

        layout.addWidget(subject_label)
        layout.addWidget(sender_label)
        layout.addWidget(date_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Sample data
    data = [
        {"subject": "Meeting Reminder", "from": "Alice", "date": "2024-08-16"},
        {"subject": "Project Update", "from": "Bob", "date": "2024-08-15"},
        {"subject": "Vacation Request", "from": "Charlie", "date": "2024-08-14"},
    ]

    window = MainWindow(data)
    window.show()
    sys.exit(app.exec_())
