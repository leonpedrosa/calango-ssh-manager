import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

path_icon_windows = 'assets/icon/calango32x32.png'
path_icon_accept_button = 'assets/icon/aceept.ico'
path_icon_not_accept_button = 'assets/icon/not_aceept.png'


class DialogConfirm(QDialog):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle('Confirmação')
        self.setWindowIcon(QIcon(path_icon_windows))
        self.resize(450, 220)

        label = QLabel('Deseja realmente sair?')
        font = label.font()
        font.setPointSize(16)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        yes_button = QPushButton(
            'Sim',
            icon=QIcon(path_icon_accept_button)
        )
        yes_button.setFixedSize(120, 50)
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton(
            'Não',
            icon=QIcon(path_icon_not_accept_button)
        )
        no_button.setFixedSize(120, 50)
        no_button.clicked.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calango | Manager SSH')
        self.setWindowIcon(QIcon(path_icon_windows))
        self.showMaximized()
        self.barraMenu()

        self.show()

    def barraMenu(self):
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('Arquivo')
        file_sub_menu = QAction('Sair', self)
        file.addAction(file_sub_menu)
        file_sub_menu.triggered.connect(self.sair)

    def sair(self):
        confirm = DialogConfirm()
        if confirm.exec() == 1:
            sys.exit()
        else:
            pass


qt = QApplication(sys.argv)
app =  MainWindow()
sys.exit(qt.exec())
