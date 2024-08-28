from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QObject, QAbstractListModel, pyqtSignal


class ControllerSignals(QObject):
    update = pyqtSignal(int, int)


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = ControllerSignals()
        self.filtered_date = [2024, 8]

        self.build_layout()

    def build_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Search...")
        self.month_selector = MonthSelector(self.filtered_date)
        self.year_selector = YearSelector(self.filtered_date)
        self.export_btn = QPushButton("Generate CSV")

        # Add widgets
        layout.addWidget(self.search_filter)
        layout.addWidget(self.month_selector)
        layout.addWidget(self.year_selector)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

        # Connect signals
        self.month_selector.currentIndexChanged.connect(self.month_selected)
        self.year_selector.currentIndexChanged.connect(self.year_selected)

    def year_selected(self, index):
        self.filtered_date[0] = int(self.year_selector.model.data(
            self.year_selector.model.index(index), Qt.DisplayRole))

        print(self.filtered_date)
        self.signals.update.emit(self.filtered_date[0], self.filtered_date[1])

    def month_selected(self, index):
        self.filtered_date[1] = index + 1
        print(self.filtered_date)
        self.signals.update.emit(self.filtered_date[0], self.filtered_date[1])

    def get_filtered_date(self):
        return self.filtered_date


class MonthSelector(QComboBox):
    def __init__(self, date):
        super().__init__()

        data = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "Nomvember", "December"]

        self.model = CustomListModel(data)
        self.setModel(self.model)


class YearSelector(QComboBox):
    def __init__(self, date):
        super().__init__()
        data = [str(year) for year in range(2020, 2030)]

        self.model = CustomListModel(data)
        self.setModel(self.model)


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
