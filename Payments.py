from PyQt5.QtWidgets import QTableView, QHeaderView, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QDateTime
from PyQt5.QtGui import QColor
from FilterControls import FilterControls


class Payments(QWidget):
    def __init__(self, data):
        super().__init__()

        layout = QVBoxLayout()
        self.filter_controls = FilterControls()
        self.payments_table = PaymentsTable(data)

        layout.addWidget(self.filter_controls)
        layout.addWidget(self.payments_table)

        self.setLayout(layout)

        # Connections
        self.filter_controls.search_filter.textChanged.connect(
            self.payments_table.proxy_filter_model.setFilterFixedString)


class PaymentsTable(QTableView):
    def __init__(self, data):
        super().__init__()

        # Table options
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)

        self.model = PaymentsModel(data)

        self.proxy_filter_model = PaymentsFilterProxyModel()
        self.proxy_filter_model.setSourceModel(self.model)
        self.proxy_filter_model.setFilterKeyColumn(-1)

        self.setModel(self.proxy_filter_model)

        """
        self.proxy_filter_model.set_building_filter("CH7")
        self.proxy_filter_model.set_date_range(
            QDateTime.fromString('Tue, 23 Jul 2024 14:00:00',
                                 'ddd, dd MMM yyyy HH:mm:ss'),
            QDateTime.fromString('Sun, 28 Jul 2024 14:00:00', 'ddd, dd MMM yyyy HH:mm:ss'))
        """


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
                return value.amount
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


class PaymentsFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(PaymentsFilterProxyModel, self).__init__()
        self.building_filter = None
        self.min_amount = None
        self.max_amount = None
        self.min_reservations = None
        self.max_reservations = None
        self.min_date = None
        self.max_date = None

    def set_building_filter(self, building):
        self.building_filter = building
        self.invalidateFilter()

    def set_amount_range(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.invalidateFilter()

    def set_reservations_range(self, min_reservations, max_reservations):
        self.min_reservations = min_reservations
        self.max_reservations = max_reservations
        self.invalidateFilter()

    def set_date_range(self, min_date, max_date):
        self.min_date = min_date
        self.max_date = max_date
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()

        # Filter by building
        if self.building_filter:
            # Assuming the building is in column 2
            building_index = model.index(source_row, 2)
            building_value = model.data(building_index, Qt.DisplayRole)
            if self.building_filter not in building_value:
                return False

        # Filter by amount range
        if self.min_amount is not None or self.max_amount is not None:
            # Assuming the amount is in column 1
            amount_index = model.index(source_row, 1)
            amount_value = int(model.data(amount_index, Qt.DisplayRole)[:-2])
            if (self.min_amount is not None and amount_value < self.min_amount) or \
               (self.max_amount is not None and amount_value > self.max_amount):
                return False

        # Filter by reservations range
        if self.min_reservations is not None or self.max_reservations is not None:
            # Assuming reservations are in column 3
            reservations_index = model.index(source_row, 3)
            reservations_value = int(model.data(
                reservations_index, Qt.DisplayRole))
            if (self.min_reservations is not None and reservations_value < self.min_reservations) or \
               (self.max_reservations is not None and reservations_value > self.max_reservations):
                return False

        if self.min_date is not None or self.max_date is not None:
            date_index = model.index(source_row, 0)
            date_value = model.data(date_index, Qt.DisplayRole)
            date_time = QDateTime.fromString(
                date_value, 'ddd, dd MMM yyyy HH:mm:ss')

            if (self.min_date is not None and date_time < self.min_date) or \
                    (self.max_date is not None and date_time > self.max_date):
                return False

        return super(PaymentsFilterProxyModel, self).filterAcceptsRow(source_row, source_parent)
