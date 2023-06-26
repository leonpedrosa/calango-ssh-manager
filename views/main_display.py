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

        yes_button = QPushButton(text='Sim', icon=QIcon(f'{path_icons}accept.ico'))
        yes_button.setFixedSize(120, 50)
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton(text='Não', icon=QIcon(f'{path_icons}not_accept.png'))
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
        self.barra_menu()

        self.show()

    def barra_menu(self):
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('&Arquivo')

        bt_new_conn = QAction(QIcon(f'{path_icons}connect.png'), 'Nova Conexão', self )
        bt_new_conn.triggered.connect(self.new_connect_ssh)
        file.addAction(bt_new_conn)

        bt_conn = QAction('Conexão Direta', self)
        bt_conn.triggered.connect(self.direct_connect)
        file.addAction(bt_conn)

        # bt_del_conn = QAction(QIcon(f'{path_icons}desconect.png'), 'Deletar Conexão', self )
        # file.addAction(bt_del_conn)

        file.addSeparator()

        file_sub_menu = QAction('Sair', self)
        file.addAction(file_sub_menu)
        file_sub_menu.triggered.connect(self.sair)

    def new_connect_ssh(self):
        new_connect = QDialog(self)
        new_connect.setWindowTitle('Nova Conexão')
        new_connect.setWindowIcon(QIcon(path_icon_windows))
        # new_connect.setMinimumSize(600, 720)
        new_connect.setFixedSize(400, 280)

        line_nome, line_host, line_port, line_usuario, line_senha = (QLineEdit() for _ in range(5))

        int_validator = QIntValidator()
        line_port.setValidator(int_validator)

        line_senha.setEchoMode(QLineEdit.EchoMode.Password)
        line_senha.setMaximumWidth(120)

        line_port.setMaximumWidth(120)

        save_btn = QPushButton(text='Salvar', icon=QIcon(f'{path_icons}save.png'))
        save_btn.setMaximumWidth(80)
        save_btn.clicked.connect(lambda: self.save(
                {
                    "nome": line_nome.text(),
                    "host": line_host.text(),
                    "port": line_port.text(),
                    "usuario": line_usuario.text(),
                    "senha": line_senha.text()
                },
                new_connect
            )
        )
        # save_btn.clicked.connect(new_connect.close)

        cancel_btn = QPushButton(text='Cancel', icon=QIcon(f'{path_icons}not_accept.png'))
        cancel_btn.setMaximumWidth(80)
        cancel_btn.clicked.connect(new_connect.close)

        v_pass_btn = QPushButton(icon=QIcon(f'{path_icons}show-password.png'))
        v_pass_btn.setMaximumWidth(30)
        v_pass_btn.setCheckable(True)

        def hide_show_password():
            if v_pass_btn.isChecked():
                line_senha.setEchoMode(QLineEdit.EchoMode.Password)
                v_pass_btn.setIcon(QIcon(f'{path_icons}hide-password.png'))
            else:
                line_senha.setEchoMode(QLineEdit.EchoMode.Normal)
                v_pass_btn.setIcon(QIcon(f'{path_icons}show-password.png'))

        v_pass_btn.clicked.connect(hide_show_password)

        layout = QGridLayout()
        new_connect.setLayout(layout)
        layout.addWidget(QLabel('Nome: '), 0, 0, 1, 3)
        layout.addWidget(line_nome, 1, 0, 1, 4)

        layout.addWidget(QLabel('Host: '), 2, 0)
        layout.addWidget(QLabel('Port: '), 2, 3)
        layout.addWidget(line_port, 3, 3)
        layout.addWidget(line_host, 3, 0, 1, 3)
        layout.addWidget(QLabel('Usuário: '), 4, 0)
        layout.addWidget(line_usuario, 5, 0, 1, 3)
        layout.addWidget(QLabel('Senha: '), 4, 3)
        layout.addWidget(line_senha, 5, 3)

        layout.addWidget(QLabel(), 6, 0)
        layout.addWidget(v_pass_btn, 6, 3)
        layout.addWidget(QLabel(), 7, 0)
        layout.addWidget(save_btn, 8, 1, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(cancel_btn, 8, 3)

        new_connect.setTabOrder(line_nome, line_host)
        new_connect.setTabOrder(line_host, line_port)
        new_connect.setTabOrder(line_port, line_usuario)
        new_connect.setTabOrder(line_usuario, line_senha)
        new_connect.setTabOrder(line_senha, save_btn)
        new_connect.setTabOrder(save_btn, cancel_btn)

        new_connect.exec()

    def direct_connect(self):
        print('Direto')

    def validate_fields(self, fields):
        for field_name, field_value in fields.items():
            if not field_value:
                QMessageBox.warning(self, 'Campo Vazio', f'O campo "{field_name}" não pode ficar vazio.')
                return False
        return True

    def save(self, fields, new_connect, *args, **kwargs):
        check_sqlite_exist()
        if self.validate_fields(fields):
            conn = sqlite3.connect(f'{path_sqlite}')
            cursor = conn.cursor()

            query = f'''INSERT INTO conexoes (nome, host, port, usuario, senha) 
            VALUES ('{fields['nome']}', '{fields['host']}', '{fields['port']}', '{fields['usuario']}', '{fields['senha']}')'''
            cursor.execute(query)

            conn.commit()
            conn.close()
            new_connect.close()
        else:
            return False

    def sair(self):
        confirm = DialogConfirm()
        if confirm.exec() == 1:
            sys.exit()
        else:
            pass


qt = QApplication(sys.argv)
app = MainWindow()
sys.exit(qt.exec())
