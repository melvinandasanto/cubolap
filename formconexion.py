import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Asumiendo que tu clase está en un archivo llamado logica_conexion.py
# from logica_conexion import Conectar 

class AdministradorConexiones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrador de Conexiones")
        self.resize(1000, 600)
        
        # Estilo Global (Basado en tus imágenes)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI', sans-serif; }
            
            QFrame#MainCard { 
                background-color: #243447; 
                border-radius: 15px; 
                border: 1px solid #3a4a5e;
            }
            
            QLabel#MainTitle { font-size: 28px; font-weight: bold; color: #ffffff; }
            QLabel#SubTitle { font-size: 16px; color: #a0aeba; }
            
            QLineEdit, QComboBox, QSpinBox {
                background-color: #304156;
                border: 1px solid #455a73;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            
            QPushButton#BtnProbar {
                background-color: #3d85c6;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton#BtnGuardar {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px;
            }
            QPushButton#BtnCancelar {
                background-color: transparent;
                border: 1px solid #455a73;
                color: #a0aeba;
                padding: 12px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout(central_widget)
        layout_principal.setContentsMargins(40, 40, 40, 40)

        # --- CABECERA ---
        lbl_titulo = QLabel("Administrador de Conexiones")
        lbl_titulo.setObjectName("MainTitle")
        lbl_sub = QLabel(" ")
        lbl_sub.setObjectName("SubTitle")
        
        layout_principal.addWidget(lbl_titulo)
        layout_principal.addWidget(lbl_sub)
        layout_principal.addSpacing(30)

        # --- CUERPO (TARJETA CENTRAL) ---
        self.card = QFrame()
        self.card.setObjectName("MainCard")
        card_layout = QHBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(40)

        # Columna Izquierda (Parámetros)
        col_izq = QVBoxLayout()
        
        col_izq.addWidget(QLabel("Alias (Nombre):"))
        self.txt_alias = QLineEdit()
        self.txt_alias.setPlaceholderText("Ej. Ventas Producción")
        col_izq.addWidget(self.txt_alias)

        col_izq.addWidget(QLabel("Tipo de Gestor:"))
        self.cb_gestor = QComboBox()
        self.cb_gestor.addItems(["MySQL", "SQL Server"])
        self.cb_gestor.currentTextChanged.connect(self.actualizar_puerto_default)
        col_izq.addWidget(self.cb_gestor)

        col_izq.addWidget(QLabel("Host / Servidor:"))
        self.txt_host = QLineEdit()
        self.txt_host.setText("localhost")
        col_izq.addWidget(self.txt_host)

        col_izq.addWidget(QLabel("Puerto:"))
        self.txt_puerto = QSpinBox()
        self.txt_puerto.setRange(1, 65535)
        self.txt_puerto.setValue(3306)
        col_izq.addWidget(self.txt_puerto)

        # Columna Derecha (Credenciales)
        col_der = QVBoxLayout()

        col_der.addWidget(QLabel("Nombre de Base de Datos:"))
        self.txt_db = QLineEdit()
        col_der.addWidget(self.txt_db)

        col_der.addWidget(QLabel("Usuario:"))
        self.txt_usuario = QLineEdit()
        col_der.addWidget(self.txt_usuario)

        col_der.addWidget(QLabel("Contraseña:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        col_der.addWidget(self.txt_pass)

        col_der.addSpacing(20)
        self.btn_probar = QPushButton("Probar Conexión")
        self.btn_probar.setObjectName("BtnProbar")
        self.btn_probar.clicked.connect(self.probar_logica)
        col_der.addWidget(self.btn_probar)

        card_layout.addLayout(col_izq)
        card_layout.addLayout(col_der)
        layout_principal.addWidget(self.card)

        # --- BOTONERA INFERIOR ---
        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("BtnCancelar")
        btn_cancelar.setFixedWidth(150)
        
        btn_guardar = QPushButton("Guardar Conexión")
        btn_guardar.setObjectName("BtnGuardar")
        btn_guardar.setFixedWidth(200)
        
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)
        layout_principal.addLayout(layout_botones)

    def actualizar_puerto_default(self, gestor):
        if gestor == "MySQL":
            self.txt_puerto.setValue(3306)
        else:
            self.txt_puerto.setValue(1433)

    def probar_logica(self):
        # Mapeo para tu clase
        gestor_map = "mysql" if self.cb_gestor.currentText() == "MySQL" else "sqlserver"
        
        # Aquí instanciamos tu clase 'Conectar'
        # conn = Conectar(
        #     gestor=gestor_map,
        #     host=self.txt_host.text(),
        #     database=self.txt_db.text(),
        #     user=self.txt_usuario.text(),
        #     password=self.txt_pass.text(),
        #     port=str(self.txt_puerto.value())
        # )

        # Simulando la prueba
        # if conn.probar_conexion():
        if self.txt_db.text() != "": # Simulación rápida
            QMessageBox.information(self, "Éxito", "¡Conexión establecida correctamente!")
        else:
            QMessageBox.critical(self, "Error", "No se pudo conectar al servidor.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AdministradorConexiones()
    ventana.show()
    sys.exit(app.exec())