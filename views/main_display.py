import sqlite3
import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from views.support.paths import *
from views.support.check import *


class DialogConfirm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Confirmação')
        self.setWindowIcon(QIcon(path_icon_windows))
        self.resize(450, 220)

        label = QLabel('Deseja realmente sair?')
        font = label.font()
        font.setPointSize(16)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        yes_button = QPushButton(text='Sim', icon=QIcon(f'{path_icon_button}accept.ico'))
        yes_button.setFixedSize(120, 50)
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton(text='Não', icon=QIcon(f'{path_icon_button}not_accept.png'))
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
        self.setMinimumSize(1020, 720)
        # self.showMaximized()
        self.barraMenu()

        self.show()

    def barraMenu(self):
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('&Arquivo')
        # btn_new_connect_ssh = Btn(file)
        # file.addAction(btn_new_connect_ssh)
        bt_new_conn = QAction(
            QIcon(f'{path_icons}connect-ssh.png'),
            'Nova Conexão',
            self
        )
        bt_new_conn.triggered.connect(self.newConnect)
        file.addAction(bt_new_conn)

        file.addSeparator()

        file_sub_menu = QAction('Sair', self)
        file.addAction(file_sub_menu)
        file_sub_menu.triggered.connect(self.sair)

    def newConnect(self):
        new_connect = QDialog(self)
        new_connect.setWindowTitle('Nova Conexão')
        new_connect.setWindowIcon(QIcon(path_icon_windows))
        # new_connect.setMinimumSize(600, 720)
        new_connect.setFixedSize(300, 200)

        line_nome, line_host, line_port, line_usuario, line_senha = (QLineEdit() for _ in range(5))

        int_validator = QIntValidator()
        line_port.setValidator(int_validator)

        save_btn = QPushButton(text='Salvar', icon=QIcon(f'{path_icon_button}save.png'))
        save_btn.clicked.connect(lambda: self.save(
                {
                    "nome": line_nome.text(),
                    "host": line_host.text(),
                    "port": line_port.text(),
                    "usuario": line_usuario.text(),
                    "senha": line_senha.text()
                }
            )
        )
        save_btn.clicked.connect(new_connect.close)

        cancel_btn = QPushButton(text='Cancel', icon=QIcon(f'{path_icon_button}not_accept.png'))
        cancel_btn.clicked.connect(new_connect.close)

        layout = QGridLayout()
        new_connect.setLayout(layout)
        layout.addWidget(QLabel('Nome: '), 0, 0, 1, 2)
        layout.addWidget(line_nome, 1, 0, 1, 2)

        layout.addWidget(QLabel('Host: '), 2, 0)
        layout.addWidget(QLabel('Port: '), 2, 1)
        layout.addWidget(line_port, 3, 1)
        layout.addWidget(line_host, 3, 0)
        layout.addWidget(QLabel('Usuário: '), 4, 0)
        layout.addWidget(line_usuario, 5, 0)
        layout.addWidget(QLabel('Senha: '), 4, 1)
        layout.addWidget(line_senha, 5, 1)

        layout.addWidget(QLabel(), 6, 0)
        layout.addWidget(save_btn, 7, 0)
        layout.addWidget(cancel_btn, 7, 1)

        new_connect.setTabOrder(line_nome, line_host)
        new_connect.setTabOrder(line_host, line_port)
        new_connect.setTabOrder(line_port, line_usuario)
        new_connect.setTabOrder(line_usuario, line_senha)
        new_connect.setTabOrder(line_senha, save_btn)
        new_connect.setTabOrder(save_btn, cancel_btn)

        new_connect.exec()

    def save(self, *args, **kwargs):
        check_sqlite_exist()
        conn = sqlite3.connect(f'{path_sqlite}')
        cursor = conn.cursor()

        query = f'''
        INSERT INTO conexoes (nome, host, port, usuario, senha)
        VALUES ('{args[0]['nome']}', '{args[0]['host']}', '{args[0]['port']}', '{args[0]['usuario']}', '{args[0]['senha']}')
        '''

        cursor.execute(query)

        conn.commit()
        conn.close()




    def sair(self):
        confirm = DialogConfirm()
        if confirm.exec() == 1:
            sys.exit()
        else:
            pass


qt = QApplication(sys.argv)
app = MainWindow()
# app.show()
# qt.exec()
sys.exit(qt.exec())
