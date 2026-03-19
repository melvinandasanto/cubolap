import sys
from PyQt6.QtWidgets import (
    QDialog, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QMessageBox, QApplication
)

class FormElegirBaseDatos(QDialog):
    def __init__(self, parent = ..., flags = ...):
        super().__init__(parent, flags)
        self.setWindowTitle("Elegir Base de Datos")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()
        self.label_titulo = QLabel("Seleccione el tipo de base de datos a usar:")
        self.radio_sqlserver = QRadioButton("SQL Server")
        self.radio_mysql = QRadioButton("MySQL")
        self.layout.addWidget(self.label_titulo)
        self.layout.addWidget(self.radio_sqlserver)
        self.layout.addWidget(self.radio_mysql)
        self.button_layout = QHBoxLayout()
        self.button_ok = QPushButton("OK")
        self.button_layout.addWidget(self.button_ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FormElegirBaseDatos()
    form.show()
    sys.exit(app.exec())