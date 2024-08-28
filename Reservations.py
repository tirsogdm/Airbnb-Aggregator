from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel


class Reservations(QTableView):
    def __init__(self, data):
        super().__init__()

        # Table options
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.verticalHeader().setVisible(True)

        self.model = ReservationsModel(data, None)
        self.setModel(self.model)

    def update(self, current_row):
        self.model.update(current_row)


class ReservationsModel(QAbstractTableModel):
    def __init__(self, data, current_idx):
        super().__init__()
        self._data = data
        self.current_idx = current_idx

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[self.current_idx].reservations[index.row()]
            idx_col = index.column()

            if idx_col == 0:
                return value.id
            elif idx_col == 1:
                return value.date_in
            elif idx_col == 2:
                return value.date_out
            elif idx_col == 3:
                return value.guest_name
            elif idx_col == 4:
                return value.apartment
            elif idx_col == 5:
                return value.listing_id
            elif idx_col == 6:
                return f'{value.amount} €'

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, index):
        if self.current_idx != None:
            return len(self._data[self.current_idx].reservations)
        return 0

    def columnCount(self, index):
        return 7

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Set custom horizontal headers
            headers = ["Id", "Date in", "Date out", "Guest",
                       "Apartment", "Listing Id", "Amount"]
            return headers[section]

        return super().headerData(section, orientation, role)

    def update(self, current_idx):
        self.current_idx = current_idx
        self.layoutChanged.emit()
