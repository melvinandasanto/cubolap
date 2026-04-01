import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
# Importamos la clase desde tu archivo fronVistaCubo.py
from fronVistaCubo import VistaPreviaDinamica

class SeleccionConexionOLAP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Seleccionar Origen de Datos")
        self.resize(1100, 600)
        
        # Estilo coherente con tus pantallas anteriores
        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }
            
            /* Tabla de Conexiones */
            QTableWidget {
                background-color: #0d1b2a; border: none; gridline-color: #243447;
                selection-background-color: #3d85c6; color: white; font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1b263b; padding: 12px; border: none; 
                font-weight: bold; color: #3d85c6;
            }

            /* Panel de Detalles (Derecha) */
            QFrame#PanelDetalles { 
                background-color: #243447; border-radius: 15px; border: 1px solid #3a4a5e;
            }
            
            QLabel#LabelSeleccion { color: #2ecc71; font-weight: bold; font-size: 14px; }
            
            /* Botones */
            QPushButton { font-weight: bold; border-radius: 5px; padding: 12px; }
            QPushButton#BtnVistaPrevia { background-color: #3d85c6; color: white; font-size: 14px; }
            QPushButton#BtnSalir { background-color: #3e5169; color: white; border: 1px solid #455a73; }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # --- SECCIÓN IZQUIERDA: TABLA DE CONEXIONES ---
        left_layout = QVBoxLayout()
        lbl_instruccion = QLabel("Seleccione la conexión para generar el Cubo OLAP:")
        lbl_instruccion.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(lbl_instruccion)

        self.tabla_conexiones = QTableWidget()
        self.tabla_conexiones.setColumnCount(6)
        self.tabla_conexiones.setHorizontalHeaderLabels([
            "Gestor", "Host", "Puerto", "Usuario", "Contraseña", "Base de Datos"
        ])
        
        self.tabla_conexiones.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_conexiones.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_conexiones.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.tabla_conexiones.itemSelectionChanged.connect(self.actualizar_info_seleccion)
        
        left_layout.addWidget(self.tabla_conexiones)
        main_layout.addLayout(left_layout, stretch=3)

        # --- SECCIÓN DERECHA: PANEL DE ACCIÓN ---
        self.panel_derecho = QFrame()
        self.panel_derecho.setObjectName("PanelDetalles")
        self.panel_derecho.setFixedWidth(320)
        
        layout_detalles = QVBoxLayout(self.panel_derecho)
        layout_detalles.setContentsMargins(20, 30, 20, 20)
        layout_detalles.setSpacing(15)

        layout_detalles.addWidget(QLabel("DETALLES DE SELECCIÓN"))
        
        self.lbl_info_db = QLabel("Ninguna conexión seleccionada")
        self.lbl_info_db.setObjectName("LabelSeleccion")
        self.lbl_info_db.setWordWrap(True)
        self.lbl_info_db.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_detalles.addWidget(self.lbl_info_db)

        layout_detalles.addSpacing(20)

        self.btn_vista_previa = QPushButton("Ir a Vista Previa")
        self.btn_vista_previa.setObjectName("BtnVistaPrevia")
        self.btn_vista_previa.clicked.connect(self.abrir_vista_previa)
        layout_detalles.addWidget(self.btn_vista_previa)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)
        layout_detalles.addWidget(self.btn_salir)

        layout_detalles.addStretch()
        main_layout.addWidget(self.panel_derecho)

    def actualizar_info_seleccion(self):
        seleccion = self.tabla_conexiones.currentRow()
        if seleccion != -1:
            # Validamos que el item exista antes de pedir el texto para evitar errores
            item_host = self.tabla_conexiones.item(seleccion, 1)
            item_db = self.tabla_conexiones.item(seleccion, 5)
            
            host = item_host.text() if item_host else "N/A"
            db_name = item_db.text() if item_db else "N/A"
            
            self.lbl_info_db.setText(f"Seleccionado:\n{db_name} en {host}")
        else:
            self.lbl_info_db.setText("Ninguna conexión seleccionada")

    def abrir_vista_previa(self):
        """Lógica para abrir la ventana fronVistaCubo pasando la ruta seleccionada."""
        fila = self.tabla_conexiones.currentRow()
        
        if fila != -1:
            # Extraemos los datos para armar el mensaje de la ruta activa
            # Columna 0: Gestor, Columna 1: Host, Columna 5: DB
            gestor = self.tabla_conexiones.item(fila, 0).text()
            host = self.tabla_conexiones.item(fila, 1).text()
            db = self.tabla_conexiones.item(fila, 5).text()
            
            info_ruta = f"{gestor} // {host} // {db}"

            # Creamos la instancia de la otra pantalla (fromVistaCubo)
            self.nueva_ventana = VistaPreviaDinamica(ruta_info=info_ruta)
            self.nueva_ventana.show()
            
            # Ocultamos la ventana actual de selección
            self.hide() 
        else:
            QMessageBox.warning(self, "Aviso", "Debe seleccionar una fila de la tabla primero.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SeleccionConexionOLAP()
    ventana.show()
    sys.exit(app.exec())