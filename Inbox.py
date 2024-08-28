from PyQt5.QtWidgets import QListWidget, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidgetItem


class Inbox(QWidget):
    def __init__(self, data):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        inbox_label = InboxLabel()
        self.inbox_list = InboxList(data)

        # Add to Layout
        layout.addWidget(inbox_label)
        layout.addWidget(self.inbox_list)

        self.setLayout(layout)


class InboxLabel(QLabel):
    def __init__(self):
        super().__init__("Payments")

        self.setContentsMargins(10, 10, 0, 0)
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)


class InboxList(QListWidget):
    def __init__(self, data):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.data = data
        self.populate_inbox()

    def populate_inbox(self):
        for email in self.data:
            item_widget = ItemWidget(email)
            list_item = QListWidgetItem(self)

            list_item.setSizeHint(item_widget.sizeHint())
            self.setItemWidget(list_item, item_widget)


class ItemWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        layout = QHBoxLayout()
        subject_label = QLabel(data["subject"])
        sender_label = QLabel(data["from"])
        date_label = QLabel(data["date"])

        layout.addWidget(subject_label)
        layout.addWidget(sender_label)
        layout.addWidget(date_label)

        self.setLayout(layout)
