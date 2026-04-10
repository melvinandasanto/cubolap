import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class MenuPrincipalOLAP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Panel de Control")
        self.resize(500, 600)
        
        # Estilo general del menú
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
            QWidget {
                font-family: 'Segoe UI';
                color: white;
            }
            QFrame#ContenedorPrincipal {
                background-color: #1b263b;
                border-radius: 15px;
                border: 1px solid #3d85c6;
            }
            QLabel#TituloMenu {
                font-size: 22px;
                font-weight: bold;
                color: #3d85c6;
                margin-bottom: 20px;
            }
            /* Estilo para los botones del menú */
            QPushButton {
                background-color: #415a77;
                border: 1px solid #3d85c6;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3d85c6;
                border: 1px solid #e0e1dd;
            }
            QPushButton#BtnCerrar {
                background-color: #c63d3d;
                border: none;
                text-align: center;
                margin-top: 20px;
            }
            QPushButton#BtnCerrar:hover {
                background-color: #e63946;
            }
        """)

        self.init_ui()

    def init_ui(self):
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Marco contenedor para el diseño
        self.frame_menu = QFrame()
        self.frame_menu.setObjectName("ContenedorPrincipal")
        layout_menu = QVBoxLayout(self.frame_menu)
        layout_menu.setContentsMargins(30, 30, 30, 30)

        # Título
        lbl_titulo = QLabel("MENÚ PRINCIPAL")
        lbl_titulo.setObjectName("TituloMenu")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_menu.addWidget(lbl_titulo)

        # --- BOTONES DEL MENÚ ---
        
        # 1. Cargar un archivo
        self.btn_cargar = QPushButton("📁  Cargar un archivo")
        layout_menu.addWidget(self.btn_cargar)

        # 2. Añadir nueva conexión
        self.btn_conexion = QPushButton("🌐  Añadir una nueva conexión")
        layout_menu.addWidget(self.btn_conexion)

        # 3. Añadir usuarios
        self.btn_usuarios = QPushButton("👥  Añadir usuarios")
        layout_menu.addWidget(self.btn_usuarios)

        # 4. Creación de cubo
        self.btn_cubo = QPushButton("🧊  Creación de cubo")
        layout_menu.addWidget(self.btn_cubo)

        # Espacio flexible
        layout_menu.addStretch()

        # Botón de Salir
        self.btn_salir = QPushButton("Cerrar Sistema")
        self.btn_salir.setObjectName("BtnCerrar")
        self.btn_salir.clicked.connect(self.close)
        layout_menu.addWidget(self.btn_salir)

        main_layout.addWidget(self.frame_menu)

        # --- COMENTARIO PARA CONEXIÓN FUTURA ---
        # Para conectar usa: self.btn_cargar.clicked.connect(self.tu_funcion)
        # --------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_menu = MenuPrincipalOLAP()
    ventana_menu.show()
    sys.exit(app.exec())