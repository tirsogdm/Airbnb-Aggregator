from PyQt5.QtWidgets import QWidget, QLineEdit, QDateEdit, QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt


class FilterControls(QWidget):
    def __init__(self):
        super().__init__()

        self.build_layout()

    def build_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Search...")
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.building_filter = QComboBox()

        # Add widgets
        layout.addWidget(self.search_filter)
        # layout.addWidget(self.date_filter)
        # layout.addWidget(self.building_filter)

        self.setLayout(layout)
