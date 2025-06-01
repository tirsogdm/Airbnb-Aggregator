from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QObject, QAbstractListModel, pyqtSignal, QDate

class ControllerSignals(QObject):
    update = pyqtSignal(int, int)

class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = ControllerSignals()
        self.date = QDate.currentDate()

        self.build_layout()

    def build_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Search...")
        self.month_selector = MonthSelector(self.date)
        self.year_selector = YearSelector(self.date)
        self.export_btn = QPushButton("Generate CSV")
        self.export_btn.setStyleSheet("""
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

        # Add widgets
        layout.addWidget(self.search_filter)
        layout.addWidget(self.month_selector)
        layout.addWidget(self.year_selector)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

        # Connect signals
        self.year_selector.currentIndexChanged.connect(self.year_selected)
        self.month_selector.currentIndexChanged.connect(self.month_selected)

    def year_selected(self, index):
        self.date = QDate(index + 2020, self.date.month(), 1)
        self.signals.update.emit(self.date.year(), self.date.month())

    def month_selected(self, index):
        self.date = QDate(self.date.year(), index + 1, 1)
        self.signals.update.emit(self.date.year(), self.date.month())

    def get_date(self):
        return self.date

    def trigger_initial_signals(self):
        self.signals.update.emit(self.date.year(), self.date.month())


class MonthSelector(QComboBox):
    def __init__(self, date):
        super().__init__()

        data = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "Nomvember", "December"]

        self.model = CustomListModel(data)
        self.setModel(self.model)

        self.setCurrentIndex(date.month()-1)


class YearSelector(QComboBox):
    def __init__(self, date):
        super().__init__()
        data = [str(year) for year in range(2020, 2030)]

        self.model = CustomListModel(data)
        self.setModel(self.model)

        self.setCurrentIndex(date.year()-2020)


class CustomListModel(QAbstractListModel):
    def __init__(self, data):
        super(CustomListModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()]

        return None

    def rowCount(self, index):
        return len(self._data)
