import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QLabel
from PyQt5.QtCore import Qt

from PaymentView import PaymentView
from Payments import Payments
from ExtractPayments import extract_payments
from FetchDialog import FetchDialog
from EmailFetchThread import EmailFetchThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ingresos - Madrid Rentals")
        self.setGeometry(500, 500, 600, 400)

        self.show_fetch_dialog()

    def show_fetch_dialog(self):
        self.dialog = FetchDialog()

        self.thread = EmailFetchThread()
        self.thread.finished.connect(self.on_data_fetched)
        self.thread.start()

        self.dialog.exec()

    def on_data_fetched(self):
        email_data = self.load_email_data()
        payments = extract_payments(email_data)

        self.dialog.accept()
        self.launch_main_window(payments)

    def launch_main_window(self, data):
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

        self.payments.controller.signals.update.connect(
            self.handle_date_change)

        self.setCentralWidget(splitter)

    def handle_date_change(self, x, y):
        self.payments_view.reservations.model.update(None)

    def selection_changed(self, selected):
        indexes = selected.indexes()

        if indexes:
            proxy_index = indexes[0]
            source_index = self.payments.payments_table.proxy_filter_model.mapToSource(
                proxy_index)
            self.payments_view.signals.update.emit(source_index.row())

    def load_email_data(self, filename="email_data.json"):
        with open(filename, 'r', encoding='utf-8') as file:
            email_data_list = json.load(file)
        print(f"Email data loaded from {filename}")
        return email_data_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    """
    # Get data
    email_data = load_email_data()
    payments = extract_payments(email_data)

    window = MainWindow(payments)
    window.show()

    app.exec_()
    """
