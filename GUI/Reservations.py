from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QDate, QDateTime

from Representations import Amount


class Reservations(QTableView):
    def __init__(self, data):
        super().__init__()

        # Table options
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(False)
        self.verticalHeader().setVisible(True)

        self.model = ReservationsModel(data, None)

        # The current implementation of this proxy model results in segmentation fault errors.
        # Another perhaps related error that arises in this context is something like "Wrong index sent to mapFromSource".
        """
        self.proxy_sort_model = ReservationsSortProxyModel()
        self.proxy_sort_model.setSourceModel(self.model)
        self.proxy_sort_model.setFilterKeyColumn(-1)
        
        self.setModel(self.proxy_sort_model)  # Test !!!
        """

        self.setModel(self.model)

    def update(self, current_row):
        self.model.update(current_row)


class ReservationsModel(QAbstractTableModel):
    def __init__(self, data, current_idx):
        super().__init__()
        self._data = data
        self.current_idx = current_idx

    def data(self, index, role):
        value = self._data[self.current_idx].reservations[index.row()]
        idx_col = index.column()

        if role == Qt.DisplayRole:
            if idx_col == 0:
                return value.id
            elif idx_col == 1:
                return value.date_in.toString()
            elif idx_col == 2:
                return value.date_out.toString()
            elif idx_col == 3:
                return value.guest_name
            elif idx_col == 4:
                return value.apartment
            elif idx_col == 5:
                return value.listing_id
            elif idx_col == 6:
                return value.amount.toString()

        if role == Qt.EditRole or role == Qt.UserRole:
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
                return value.amount

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


class ReservationsSortProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(ReservationsSortProxyModel, self).__init__()

    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left, Qt.EditRole)
        right_data = self.sourceModel().data(right, Qt.EditRole)

        if isinstance(left_data, QDate) and isinstance(right_data, QDate):
            return left_data < right_data

        if isinstance(left_data, Amount) and isinstance(right_data, Amount):
            return left_data < right_data

        return super(ReservationsSortProxyModel, self).lessThan(left, right)
