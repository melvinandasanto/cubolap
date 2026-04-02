import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView
)
from PyQt6.QtCore import Qt

# --- IMPORTACIÓN DEL FORMULARIO DE ANÁLISIS ---
# Asegúrate de que el archivo se llame FromCubo.py y la clase PantallaAnalisisDinamico
from formcubo import PantallaAnalisisDinamico

class VistaPreviaDinamica(QMainWindow):
    def __init__(self, tipo_origen, id_origen):
        super().__init__()
        self.tipo_origen = tipo_origen
        self.id_origen = id_origen
        self.setWindowTitle("Sistema OLAP - Vista Previa de Datos")
        self.resize(1100, 700)

        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }
            
            QFrame#BannerRuta { 
                background-color: #1b263b; border-bottom: 2px solid #3d85c6;
                padding: 12px;
            }
            
            QTableWidget {
                background-color: #0d1b2a; border: none; gridline-color: #243447;
                color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #243447; padding: 10px; border: none; 
                font-weight: bold; color: #3d85c6; text-transform: uppercase;
            }

            QPushButton#BtnAnalizar { 
                background-color: #2ecc71; color: white; font-weight: bold; 
                border-radius: 5px; padding: 12px; min-width: 180px;
            }
            QPushButton#BtnSalir { 
                background-color: #c63d3d; color: white; font-weight: bold; 
                border-radius: 5px; padding: 12px; min-width: 100px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- BANNER DE RUTA ACTUAL ---
        self.banner = QFrame()
        self.banner.setObjectName("BannerRuta")
        layout_banner = QHBoxLayout(self.banner)
        self.lbl_ruta = QLabel(f"ORIGEN DE DATOS: {self.ruta_activa}")
        self.lbl_ruta.setStyleSheet("font-size: 14px; font-weight: bold; color: #3d85c6;")
        layout_banner.addWidget(self.lbl_ruta)
        main_layout.addWidget(self.banner)

        # --- CONTENIDO ---
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(25, 20, 25, 20)
        
        lbl_msg = QLabel("Vista previa de la estructura de datos seleccionada:")
        lbl_msg.setStyleSheet("color: #a0aeba; margin-bottom: 5px;")
        content_layout.addWidget(lbl_msg)

        self.tabla = QTableWidget()
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive) 
        self.tabla.horizontalHeader().setStretchLastSection(True)
        content_layout.addWidget(self.tabla)

        # --- BOTONES ---
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 20, 0, 10)
        
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)
        
        self.btn_analizar = QPushButton("Analizar mis Datos")
        self.btn_analizar.setObjectName("BtnAnalizar")
        
        # --- CONEXIÓN DEL BOTÓN ---
        self.btn_analizar.clicked.connect(self.abrir_analisis)

        btn_layout.addWidget(self.btn_salir)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_analizar)
        
        content_layout.addLayout(btn_layout)
        main_layout.addLayout(content_layout)

    def cargar_datos_externos(self, dataframe):
        """Llama a esta función desde tu clase de conexión para llenar la tabla."""
        if dataframe is not None and not dataframe.empty:
            self.df_actual = dataframe # Actualizamos el dataframe almacenado
            columnas = dataframe.columns
            self.tabla.setColumnCount(len(columnas))
            self.tabla.setHorizontalHeaderLabels(columnas)
            self.tabla.setRowCount(len(dataframe))
            
            for i in range(len(dataframe)):
                for j in range(len(columnas)):
                    valor = str(dataframe.iloc[i, j])
                    self.tabla.setItem(i, j, QTableWidgetItem(valor))
            
            self.tabla.resizeColumnsToContents()

    def abrir_analisis(self):
        """Abre el formulario de Cubo OLAP pasándole los datos cargados."""
        # Creamos la instancia de la pantalla de análisis
        # Pasamos self.df_actual para que el Dashboard tenga datos que procesar
        self.ventana_analisis = PantallaAnalisisDinamico(self.df_actual)
        self.ventana_analisis.show()
        
        # Cerramos o minimizamos la vista previa
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VistaPreviaDinamica()
    ventana.show()
    sys.exit(app.exec())