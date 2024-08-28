import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QListView, QSplitter, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PaymentView import PaymentView
from Payments import Payments
from Reservations import Reservations
from ExtractPayments import extract_payments
import pandas as pd
from openpyxl import Workbook


class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Ingresos - Madrid Rentals")

        # Payments List Widget
        self.payments = Payments(data)
        # Payment View Widget
        self.payments_view = PaymentView(data)

        # Splitter View
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.payments)
        splitter.addWidget(self.payments_view)
        splitter.setSizes([1000, 700])

        self.payments.payments_table.selectionModel(
        ).selectionChanged.connect(self.selection_changed)

        self.setCentralWidget(splitter)

    def selection_changed(self, selected):
        indexes = selected.indexes()

        if indexes:
            proxy_index = indexes[0]
            source_index = self.payments.payments_table.proxy_filter_model.mapToSource(
                proxy_index)
            self.payments_view.signals.update.emit(source_index.row())


def load_email_data(filename="email_data.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        email_data_list = json.load(file)
    print(f"Email data loaded from {filename}")
    return email_data_list


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Get data
    email_data = load_email_data()
    payments = extract_payments(email_data)

    window = MainWindow(payments)
    window.show()
    # Start event loop
    app.exec_()
