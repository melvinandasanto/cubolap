import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QMessageBox, 
    QTableWidget, QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt

class AdministradorConexiones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Administrador de Conexiones")
        self.setMinimumSize(1200, 700)

        # Estilo basado en la identidad visual de la aplicación
        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }
            
            /* Tabla con scrollbars estilizados */
            QTableWidget {
                background-color: #0d1b2a; border: none; gridline-color: #243447;
                selection-background-color: #3d85c6; font-size: 13px; color: white;
            }
            QHeaderView::section {
                background-color: #1b263b; padding: 12px; border: none; 
                font-weight: bold; color: #3d85c6;
            }

            /* Panel Lateral Derecho Responsivo */
            QFrame#PanelLateral { 
                background-color: #243447; 
                border-radius: 15px; 
                border: 1px solid #3a4a5e;
            }
            
            QLabel#TituloSeccion { font-size: 18px; font-weight: bold; color: #3d85c6; margin-bottom: 10px; }
            
            QLineEdit, QComboBox { 
                background-color: #304156; border: 1px solid #455a73; 
                border-radius: 5px; padding: 8px; color: white;
            }

            /* Botones estilizados */
            QPushButton { font-weight: bold; border-radius: 5px; padding: 10px; min-height: 20px; }
            QPushButton#BtnProbar { background-color: #2ecc71; color: white; border: none; }
            QPushButton#BtnGuardar { background-color: #3d85c6; color: white; }
            QPushButton#BtnActualizar { background-color: #3e5169; color: white; border: 1px solid #455a73; }
            QPushButton#BtnEliminar { background-color: #c63d3d; color: white; }
            
            QMessageBox { background-color: #243447; }
            QMessageBox QLabel { color: white; }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal que permite expansión
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- SECCIÓN IZQUIERDA: TABLA ---
        left_container = QVBoxLayout()
        lbl_lista = QLabel("Listado de Conexiones")
        lbl_lista.setStyleSheet("font-size: 22px; font-weight: bold;")
        left_container.addWidget(lbl_lista)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Gestor", "Host", "Base de Datos"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left_container.addWidget(self.table)
        #hentai


        # Ajustar el stretch para que la tabla use más espacio al expandir
        main_layout.addLayout(left_container, stretch=3)

        # --- SECCIÓN DERECHA: FORMULARIO ---
        self.panel = QFrame()
        self.panel.setObjectName("PanelLateral")
        self.panel.setFixedWidth(350)
        # Política de tamaño para mantener el ancho pero permitir expansión vertical
        self.panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        form_layout = QVBoxLayout(self.panel)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        lbl_tit = QLabel("GESTIÓN DE CONEXIÓN")
        lbl_tit.setObjectName("TituloSeccion")
        lbl_tit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(lbl_tit)

        # Campos del formulario (ID eliminado como solicitaste)
        form_layout.addWidget(QLabel("Nombre:"))
        self.txt_alias = QLineEdit()
        form_layout.addWidget(self.txt_alias)

        form_layout.addWidget(QLabel("Tipo de Gestor:"))
        self.cb_gestor = QComboBox()
        self.cb_gestor.addItems(["SQL Server", "MySQL"])
        form_layout.addWidget(self.cb_gestor)

        form_layout.addWidget(QLabel("Host / Servidor:"))
        self.txt_host = QLineEdit()
        form_layout.addWidget(self.txt_host)

        form_layout.addWidget(QLabel("Base de Datos:"))
        self.txt_db = QLineEdit()
        form_layout.addWidget(self.txt_db)

        form_layout.addWidget(QLabel("Usuario:"))
        self.txt_user = QLineEdit()
        form_layout.addWidget(self.txt_user)

        form_layout.addWidget(QLabel("Contraseña:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.txt_pass)

        form_layout.addSpacing(10)

        #POrno

        
        # Botones de Acción
        self.btn_probar = QPushButton("Probar Conexión")
        self.btn_probar.setObjectName("BtnProbar")
        self.btn_probar.clicked.connect(self.probar_conexion_logica)
        form_layout.addWidget(self.btn_probar)

        self.btn_guardar = QPushButton("Guardar Conexión")
        self.btn_guardar.setObjectName("BtnGuardar")
        form_layout.addWidget(self.btn_guardar)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setObjectName("BtnActualizar")
        form_layout.addWidget(self.btn_actualizar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        form_layout.addWidget(self.btn_eliminar)

        # Espaciador para empujar todo hacia arriba si la ventana crece mucho
        form_layout.addStretch()

        main_layout.addWidget(self.panel)

    def probar_conexion_logica(self):
        if not self.txt_host.text() or not self.txt_db.text():
            QMessageBox.warning(self, "Validación", "Por favor ingrese el Host y la Base de Datos.")
            return
        
        # Simulación de éxito de conexión
        QMessageBox.information(self, "Estado", " Conexión exitosa al servidor.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AdministradorConexiones()
    win.show()
    sys.exit(app.exec())