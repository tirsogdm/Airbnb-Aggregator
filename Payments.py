from PyQt5.QtWidgets import QTableView, QHeaderView, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QDateTime, QDate, QTime
from Controller import Controller
from openpyxl import Workbook
from openpyxl.styles import PatternFill


class Payments(QWidget):
    def __init__(self, data):
        super().__init__()
        self._data = data

        layout = QVBoxLayout()
        self.controller = Controller()
        self.payments_table = PaymentsTable(data)

        layout.addWidget(self.controller)
        layout.addWidget(self.payments_table)

        self.setLayout(layout)

        # Connections
        self.controller.search_filter.textChanged.connect(
            self.payments_table.proxy_filter_model.setFilterFixedString)
        self.controller.signals.update.connect(self.handle_date_selection)
        self.controller.export_btn.clicked.connect(self.export_to_excel)

    def handle_date_selection(self, year, month):
        print("date:", year, month)
        min_date, max_date = self.get_min_max_dates(year, month)
        self.payments_table.proxy_filter_model.set_date_range(
            min_date, max_date)

    def get_min_max_dates(self, year, month):
        min_date = QDate(year, month, 1)
        min_date_time = QDateTime(min_date, QTime(0, 0, 0))

        days_in_month = min_date.daysInMonth()

        max_date_time = QDateTime(
            QDate(year, month, days_in_month), QTime(23, 59, 59))

        return min_date_time, max_date_time

    def get_visible_rows(self):
        row_count = self.payments_table.proxy_filter_model.rowCount()

        visible_rows = list()
        for row in range(row_count):
            proxy_index = self.payments_table.proxy_filter_model.index(
                row, 0)
            source_index = self.payments_table.proxy_filter_model.mapToSource(
                proxy_index)
            visible_rows.append(source_index.row())

        visible_rows.sort()  # set to ascending order by default
        return visible_rows

    def export_to_excel(self):
        visible_rows = self.get_visible_rows()
        date = self.controller.get_filtered_date()

        wb = Workbook()
        ws = wb.active
        ws.title = f"Pagos Madrid Rentals {date[1]}.{date[0]}"

        header_fill = PatternFill(
            start_color="FFFF00", end_color="FFFF00", fill_type="solid")

        headers = ["", "Platform", "Date", "Amount Transfered", "Building",
                   "Date in", "Date out", "ID", "Guest", "Apartment", "Amount"]

        ws.append(headers)

        for row in visible_rows:
            payment = self._data[row]
            for i, reservation in enumerate(payment.reservations):
                row = ["", "Airbnb", "", "", "", reservation.date_in, reservation.date_out, reservation.id,
                       reservation.guest_name, reservation.apartment, reservation.amount]

                if i == 0:
                    row[2] = payment.date.toString("dd/MM/yyyy")
                    row[3] = payment.amount
                    row[4] = payment.building

                    ws.append(row)
                    for cell in ws[ws.max_row]:
                        cell.fill = header_fill

                else:
                    ws.append(row)

        # Size columns
        for column in ws.columns:
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0 for cell in column)
            adjusted_width = max_length + 2
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        wb.save(f"pagos_madrid_rentals_{date[1]}.{date[0]}.xlsx")


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
        value = self._data[index.row()]
        idx_col = index.column()

        if role == Qt.DisplayRole:
            if idx_col == 0:
                return value.date.toString("dd/MM/yyyy")
            elif idx_col == 1:
                return value.amount
            elif idx_col == 2:
                return value.building
            elif idx_col == 3:
                return len(value.reservations)

        if role == Qt.EditRole or role == Qt.UserRole:
            if idx_col == 0:
                return value.date_time
            elif idx_col == 1:
                return value.amount
            elif idx_col == 2:
                return value.building
            elif idx_col == 3:
                return len(value.reservations)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Set custom horizontal headers
            headers = ["Date", "Amount", "Building",
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

    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left, Qt.EditRole)
        right_data = self.sourceModel().data(right, Qt.EditRole)

        if isinstance(left_data, QDateTime) and isinstance(right_data, QDateTime):
            return left_data < right_data

        return super(PaymentsFilterProxyModel, self).lessThan(left, right)

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()

        # Filter by building
        if self.building_filter:
            # Assuming the building is in column 2
            building_index = model.index(source_row, 2)
            building_value = model.data(building_index, Qt.EditRole)
            if self.building_filter not in building_value:
                return False

        # Filter by amount range
        if self.min_amount is not None or self.max_amount is not None:
            # Assuming the amount is in column 1
            amount_index = model.index(source_row, 1)
            amount_value = int(model.data(amount_index, Qt.EditRole)[:-2])
            if (self.min_amount is not None and amount_value < self.min_amount) or \
               (self.max_amount is not None and amount_value > self.max_amount):
                return False

        # Filter by reservations range
        if self.min_reservations is not None or self.max_reservations is not None:
            # Assuming reservations are in column 3
            reservations_index = model.index(source_row, 3)
            reservations_value = int(model.data(
                reservations_index, Qt.EditRole))
            if (self.min_reservations is not None and reservations_value < self.min_reservations) or \
               (self.max_reservations is not None and reservations_value > self.max_reservations):
                return False

        if self.min_date is not None or self.max_date is not None:
            date_index = model.index(source_row, 0)
            date_value = model.data(date_index, Qt.EditRole)

            if (self.min_date is not None and date_value < self.min_date) or \
                    (self.max_date is not None and date_value > self.max_date):
                return False

        return super(PaymentsFilterProxyModel, self).filterAcceptsRow(source_row, source_parent)
