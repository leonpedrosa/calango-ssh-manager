import sys
from PyQt6.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 480, 320)

        self.show()

qt = QApplication(sys.argv)
app = MainWindow()
sys.exit(qt.exec())
