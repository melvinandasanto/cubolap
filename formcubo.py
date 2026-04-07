import sys
import os

# Compatibilidad con PyQt6 para Matplotlib
os.environ["QT_API"] = "pyqt6"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QScrollArea, QComboBox, QMessageBox,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

class PantallaAnalisisDinamico(QMainWindow):
    def __init__(self, df_entrada=None):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Dashboard Adaptativo")
        self.resize(1400, 900)
        
        self.df = df_entrada 
        self.dimensiones = []
        self.medidas = []

        self.setStyleSheet("""
            QMainWindow { background-color: #0d1b2a; }
            QWidget { color: white; font-family: 'Segoe UI'; }
            
            /* Panel Lateral */
            QFrame#PanelControl { 
                background-color: #1b263b; border-right: 2px solid #3d85c6; 
            }
            
            QLabel#TituloSeccion { 
                font-weight: bold; color: #3d85c6; font-size: 14px; 
                text-transform: uppercase; margin-bottom: 5px;
            }
            
            /* Tabla de Resumen Superior */
            QTableWidget#TablaPivot { 
                background-color: #1b263b; border: 1px solid #3d85c6;
                gridline-color: #243447; color: #ffffff;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #243447; color: #3d85c6;
                font-weight: bold; border: 1px solid #0d1b2a;
            }

            QFrame#GraficoCard { 
                background-color: #1b263b; border-radius: 12px; border: 1px solid #243447; 
            }
            
            QComboBox { 
                background-color: #415a77; border: 1px solid #3d85c6; 
                border-radius: 5px; padding: 8px; color: white; 
            }
            
            QPushButton#BtnAplicar { 
                background-color: #2ecc71; color: white; font-weight: bold; 
                padding: 15px; border-radius: 5px;
            }
            
            QPushButton#BtnSalir { 
                background-color: #c63d3d; font-weight: bold; padding: 10px; border-radius: 5px; 
            }
        """)

        self.init_ui()

        if self.df is not None:
            self.detectar_estructura()

    def detectar_estructura(self):
        self.dimensiones = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.medidas = self.df.select_dtypes(include=['number']).columns.tolist()

        self.combo_dim.clear()
        self.combo_dim.addItems(self.dimensiones)
        self.combo_medida.clear()
        self.combo_medida.addItems(self.medidas)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setSpacing(0)
        layout_principal.setContentsMargins(0,0,0,0)

        # --- PANEL LATERAL DE SELECCIÓN ---
        self.panel_config = QFrame()
        self.panel_config.setObjectName("PanelControl")
        self.panel_config.setFixedWidth(300)
        ly_config = QVBoxLayout(self.panel_config)
        ly_config.setContentsMargins(20, 20, 20, 20)

        lbl_campos = QLabel("CONFIGURACIÓN OLAP")
        lbl_campos.setObjectName("TituloSeccion")
        ly_config.addWidget(lbl_campos)
        
        ly_config.addSpacing(20)
        ly_config.addWidget(QLabel("SELECCIONAR DIMENSIÓN:"))
        self.combo_dim = QComboBox()
        ly_config.addWidget(self.combo_dim)

        ly_config.addSpacing(15)
        ly_config.addWidget(QLabel("SELECCIONAR MEDIDA:"))
        self.combo_medida = QComboBox()
        ly_config.addWidget(self.combo_medida)

        ly_config.addSpacing(30)
        self.btn_aplicar = QPushButton("ACTUALIZAR VISTA")
        self.btn_aplicar.setObjectName("BtnAplicar")
        self.btn_aplicar.clicked.connect(self.refrescar_analisis)
        ly_config.addWidget(self.btn_aplicar)

        ly_config.addStretch()
        self.btn_salir = QPushButton("Cerrar Dashboard")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)
        ly_config.addWidget(self.btn_salir)

        layout_principal.addWidget(self.panel_config)

        # --- ÁREA CENTRAL (RESUMEN + GRÁFICOS) ---
        container_central = QWidget()
        self.layout_central = QVBoxLayout(container_central)
        
        # 1. Título y Tabla de Resumen Superior
        lbl_resumen_tit = QLabel("VISTA DE RESUMEN (TABLA DINÁMICA)")
        lbl_resumen_tit.setObjectName("TituloSeccion")
        self.layout_central.addWidget(lbl_resumen_tit)

        self.tabla_resumen = QTableWidget()
        self.tabla_resumen.setObjectName("TablaPivot")
        self.tabla_resumen.setColumnCount(2)
        self.tabla_resumen.setFixedHeight(200) # Altura fija para el resumen superior
        self.tabla_resumen.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_central.addWidget(self.tabla_resumen)

        self.layout_central.addSpacing(20)

        # 2. Área de Gráficos con Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.widget_graficos = QWidget()
        self.layout_grid = QVBoxLayout(self.widget_graficos)
        
        self.lbl_info = QLabel("Presione 'Actualizar' para generar el análisis.")
        self.lbl_info.setStyleSheet("font-size: 16px; color: #3d85c6;")
        self.layout_grid.addWidget(self.lbl_info, alignment=Qt.AlignmentFlag.AlignCenter)

        self.scroll.setWidget(self.widget_graficos)
        self.layout_central.addWidget(self.scroll)

        layout_principal.addWidget(container_central)

    def refrescar_analisis(self):
        if self.df is None or self.df.empty:
            return

        self.lbl_info.hide()
        dim = self.combo_dim.currentText()
        med = self.combo_medida.currentText()

        # --- LÓGICA DE TABLA ADAPTATIVA ---
        resumen = self.df.groupby(dim)[med].sum().reset_index()
        self.tabla_resumen.setRowCount(len(resumen))
        self.tabla_resumen.setHorizontalHeaderLabels([f"ETIQUETA: {dim}", f"SUMA DE {med}"])
        
        for i, row in resumen.iterrows():
            self.tabla_resumen.setItem(i, 0, QTableWidgetItem(str(row[dim])))
            # Formato de moneda/número intuitivo
            item_valor = QTableWidgetItem(f"{row[med]:,.2f}")
            item_valor.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tabla_resumen.setItem(i, 1, item_valor)

        # --- REGENERAR GRÁFICOS ---
        for i in reversed(range(self.layout_grid.count())): 
            item = self.layout_grid.itemAt(i)
            if item.widget(): item.widget().deleteLater()

        f1 = QHBoxLayout(); f2 = QHBoxLayout()
        f1.addWidget(self.crear_canvas(f"Comparativo de {med}", "bar", dim, med))
        f1.addWidget(self.crear_canvas(f"Distribución %", "pie", dim, med))
        f2.addWidget(self.crear_canvas(f"Evolución", "line", dim, med))
        f2.addWidget(self.crear_canvas(f"Análisis de Puntos", "scatter", dim, med))

        self.layout_grid.addLayout(f1)
        self.layout_grid.addLayout(f2)

    def crear_canvas(self, titulo, tipo, eje_x, eje_y):
        card = QFrame()
        card.setObjectName("GraficoCard")
        ly = QVBoxLayout(card)
        ly.addWidget(QLabel(titulo))

        plt.rcParams.update({"text.color": "white", "axes.labelcolor": "white", 
                             "xtick.color": "#a0aeba", "ytick.color": "#a0aeba",
                             "axes.facecolor": "#1b263b", "figure.facecolor": "#1b263b"})

        fig, ax = plt.subplots(figsize=(5, 3), dpi=85)
        resumen = self.df.groupby(eje_x)[eje_y].sum()

        if tipo == "bar":
            resumen.plot(kind='bar', ax=ax, color='#3d85c6')
        elif tipo == "line":
            resumen.plot(kind='line', ax=ax, marker='o', color='#2ecc71')
        elif tipo == "pie":
            resumen.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        elif tipo == "scatter":
            ax.scatter(range(len(resumen)), resumen.values, color='#e67e22')

        plt.tight_layout()
        ly.addWidget(FigureCanvas(fig))
        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Datos de prueba
    df_ejemplo = pd.DataFrame({
        'Categoría': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro'],
        'Ventas': [45000, 32000, 51000, 28000, 60000]
    })
    win = PantallaAnalisisDinamico(df_ejemplo)
    win.show()
    sys.exit(app.exec())