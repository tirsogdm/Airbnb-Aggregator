from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys

from GUI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Madrid Rentals - Ingresos")
    app.setWindowIcon(QIcon('assets/LOGO_Madrid-Rentals.png'))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())