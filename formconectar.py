import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QComboBox, QMessageBox
)

from claseconectar import Conexion
from menu import Menu


class FormConexion(QWidget):
    def __init__(self):
        super().__init__()

        # 🔹 Selector de gestor
        self.combo_gestor = QComboBox()
        self.combo_gestor.addItems(["mysql", "sqlserver"])

        # 🔹 Inputs
        self.txt_host = QLineEdit()
        self.txt_host.setPlaceholderText("Host / Server")

        self.txt_port = QLineEdit()
        self.txt_port.setPlaceholderText("Puerto (solo MySQL)")

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Usuario (solo MySQL)")

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Contraseña")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.txt_database = QLineEdit()
        self.txt_database.setPlaceholderText("Base de datos")

        # 🔹 Botón
        self.btn_probar = QPushButton("Conectar")
        self.btn_probar.clicked.connect(self.probar_conexion)

        # 🔹 Layout
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Gestor"))
        layout.addWidget(self.combo_gestor)

        layout.addWidget(QLabel("Host / Server"))
        layout.addWidget(self.txt_host)

        layout.addWidget(QLabel("Puerto"))
        layout.addWidget(self.txt_port)

        layout.addWidget(QLabel("Usuario"))
        layout.addWidget(self.txt_user)

        layout.addWidget(QLabel("Contraseña"))
        layout.addWidget(self.txt_password)

        layout.addWidget(QLabel("Base de datos"))
        layout.addWidget(self.txt_database)

        layout.addWidget(self.btn_probar)

        self.setLayout(layout)

        self.setWindowTitle("Conexión a Base de Datos")
        self.resize(300, 350)

    def probar_conexion(self):
        gestor = self.combo_gestor.currentText()
        host = self.txt_host.text()
        port = self.txt_port.text()
        user = self.txt_user.text()
        password = self.txt_password.text()
        database = self.txt_database.text()

        try:
            conexion = Conexion(
                gestor=gestor,
                host=host,
                database=database,
                user=user,
                password=password,
                port=port if gestor == "mysql" else None
            )

            if conexion.probar_conexion():
                QMessageBox.information(self, "Éxito", "Conexión exitosa ✅")
                self.abrir_menu()
            else:
                QMessageBox.critical(self, "Error", "No se pudo conectar ❌")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def abrir_menu(self):
        self.menu = Menu()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormConexion()
    ventana.show()
    sys.exit(app.exec())