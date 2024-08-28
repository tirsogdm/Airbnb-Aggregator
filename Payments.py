from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QColor


class Payments(QTableView):
    def __init__(self, data):
        super().__init__()

        # Table options
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.verticalHeader().setVisible(True)

        self.model = PaymentsModel(data)
        self.setModel(self.model)


class PaymentsModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()]
            idx_col = index.column()

            if idx_col == 0:
                return value.date
            elif idx_col == 1:
                return f'{value.amount} €'
            elif idx_col == 2:
                return value.building
            elif idx_col == 3:
                return len(value.reservations)
            else:
                return

        elif role == Qt.DecorationRole:
            published = self._data[index.row()].published

            if index.column() == 0:
                if published:
                    return QColor('green')
                else:
                    return QColor('red')

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Set custom horizontal headers
            headers = ["Date Time", "Amount", "Building",
                       "Reservations"]
            return headers[section]

        return super().headerData(section, orientation, role)
