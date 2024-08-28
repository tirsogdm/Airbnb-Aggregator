from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal
from Reservations import Reservations


class PaymentViewSignals(QObject):
    update = pyqtSignal(int)


class PaymentView(QWidget):
    def __init__(self, data):
        super().__init__()
        self.signals = PaymentViewSignals()
        self.signals.update.connect(self.update)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        self.reservations = Reservations(data)
        self.frw_msg = ForwardedMessage(data)

        # Add to Layout
        layout.addWidget(self.reservations)
        layout.addWidget(self.frw_msg)

        self.setLayout(layout)

    def update(self, current_row):
        self.reservations.update(current_row)
        self.frw_msg.update(current_row)


class ForwardedMessage(QTextEdit):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def update(self, current_row):
        payment = self._data[current_row]
        self.setText(payment.raw)
