from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QDialog, QLabel, QSizePolicy, QProgressBar, QSpacerItem
from PyQt5.QtCore import Qt


class FetchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome - Ingresos Madrid Rentals")
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.label = QLabel("Emails are being fetched. Please wait...", self)
        layout.addWidget(self.label, alignment=Qt.AlignTop)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignTop)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignBottom)

    def cancel(self):  # Look over
        QApplication.instance().quit()
