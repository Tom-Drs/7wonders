from ui import MainWindow
from PySide6 import QtWidgets
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(450, 350)
    widget.show()

    sys.exit(app.exec())