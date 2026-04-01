import sys
import os

# Compatibilidad con PyQt6
os.environ["QT_API"] = "pyqt6"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QScrollArea, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt

class PantallaAnalisisDinamico(QMainWindow):
    def __init__(self, df_entrada=None):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Análisis Multidimensional")
        self.resize(1300, 850)
        
        # Guardamos el DataFrame (ahora vendrá vacío o con datos de tu DB)
        self.df = df_entrada 
        
        # Listas para identificar qué hay en la tabla
        self.dimensiones = []
        self.medidas = []

        self.setStyleSheet("""
            QMainWindow { background-color: #0d1b2a; }
            QWidget { color: white; font-family: 'Segoe UI'; }
            QFrame#PanelControl { background-color: #1b263b; border-radius: 10px; border: 1px solid #3d85c6; }
            QFrame#GraficoCard { background-color: #1b263b; border-radius: 12px; border: 1px solid #243447; }
            QComboBox { background-color: #415a77; border: 1px solid #3d85c6; border-radius: 5px; padding: 8px; color: white; }
            QPushButton#BtnAplicar { background-color: #2ecc71; color: white; font-weight: bold; padding: 12px; border-radius: 5px; }
            QPushButton#BtnSalir { background-color: #c63d3d; font-weight: bold; padding: 10px; border-radius: 5px; }
        """)

        self.init_ui()

        # Si recibimos datos al iniciar, configuramos las opciones
        if self.df is not None:
            self.detectar_estructura()

    def detectar_estructura(self):
        """Identifica qué columnas son texto (dimensiones) y cuáles números (medidas)."""
        self.dimensiones = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.medidas = self.df.select_dtypes(include=['number']).columns.tolist()

        # Llenar los selectores dinámicamente
        self.combo_dim.clear()
        self.combo_dim.addItems(self.dimensiones)
        
        self.combo_medida.clear()
        self.combo_medida.addItems(self.medidas)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)

        # --- PANEL DE CONFIGURACIÓN (IZQUIERDA) ---
        self.panel_config = QFrame()
        self.panel_config.setObjectName("PanelControl")
        self.panel_config.setFixedWidth(300)
        ly_config = QVBoxLayout(self.panel_config)

        ly_config.addWidget(QLabel("⚙️ CONFIGURACIÓN DEL CUBO"))
        
        ly_config.addWidget(QLabel("Seleccionar Dimensión:"))
        self.combo_dim = QComboBox()
        ly_config.addWidget(self.combo_dim)

        ly_config.addWidget(QLabel("Seleccionar Medida:"))
        self.combo_medida = QComboBox()
        ly_config.addWidget(self.combo_medida)

        ly_config.addSpacing(20)
        
        self.btn_aplicar = QPushButton("Aplicar y Graficar")
        self.btn_aplicar.setObjectName("BtnAplicar")
        self.btn_aplicar.clicked.connect(self.refrescar_analisis)
        ly_config.addWidget(self.btn_aplicar)

        ly_config.addStretch()
        
        self.btn_salir = QPushButton("Cerrar")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)
        ly_config.addWidget(self.btn_salir)

        layout_principal.addWidget(self.panel_config)

        # --- CONTENEDOR DE GRÁFICOS (DERECHA) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.widget_graficos = QWidget()
        self.layout_grid = QVBoxLayout(self.widget_graficos)
        
        self.lbl_info = QLabel("Cargue una conexión para visualizar el análisis dinámico.")
        self.lbl_info.setStyleSheet("font-size: 18px; color: #3d85c6;")
        self.layout_grid.addWidget(self.lbl_info, alignment=Qt.AlignmentFlag.AlignCenter)

        self.scroll.setWidget(self.widget_graficos)
        layout_principal.addWidget(self.scroll)

    def refrescar_analisis(self):
        """Limpia y genera gráficos basados en las columnas elegidas por el usuario."""
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "Aviso", "No hay datos cargados para analizar.")
            return

        # 1. Limpiar el área de gráficos
        self.lbl_info.hide()
        for i in reversed(range(self.layout_grid.count())): 
            widget = self.layout_grid.itemAt(i).widget()
            if widget is not None: widget.deleteLater()

        # 2. Obtener lo que el usuario quiere ver
        dim = self.combo_dim.currentText()
        med = self.combo_medida.currentText()

        # 3. Crear contenedor de gráficos (2x2)
        grid = QVBoxLayout()
        fila1 = QHBoxLayout()
        fila2 = QHBoxLayout()

        # Generar 4 vistas distintas de los mismos datos seleccionados
        fila1.addWidget(self.crear_canvas(f"Suma de {med} por {dim}", "bar", dim, med))
        fila1.addWidget(self.crear_canvas(f"Distribución Porcentual ({med})", "pie", dim, med))
        fila2.addWidget(self.crear_canvas(f"Tendencia de {med}", "line", dim, med))
        fila2.addWidget(self.crear_canvas(f"Análisis de Dispersión", "scatter", med, med)) # Comparativa consigo mismo o índice

        grid.addLayout(fila1)
        grid.addLayout(fila2)
        self.layout_grid.addLayout(grid)

    def crear_canvas(self, titulo, tipo, eje_x, eje_y):
        card = QFrame()
        card.setObjectName("GraficoCard")
        ly = QVBoxLayout(card)
        ly.addWidget(QLabel(titulo))

        # Estilo Matplotlib
        plt.rcParams.update({"text.color": "white", "axes.labelcolor": "white", 
                             "xtick.color": "#a0aeba", "ytick.color": "#a0aeba",
                             "axes.facecolor": "#1b263b", "figure.facecolor": "#1b263b"})

        fig, ax = plt.subplots(figsize=(5, 4), dpi=80)
        
        # Lógica de agrupación OLAP
        resumen = self.df.groupby(eje_x)[eje_y].sum()

        if tipo == "bar":
            resumen.plot(kind='bar', ax=ax, color='#3d85c6')
        elif tipo == "line":
            resumen.plot(kind='line', ax=ax, marker='s', color='#2ecc71')
        elif tipo == "pie":
            resumen.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        elif tipo == "scatter":
            ax.scatter(range(len(self.df)), self.df[eje_y], color='#e67e22', alpha=0.5)

        canvas = FigureCanvas(fig)
        ly.addWidget(canvas)
        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ejemplo: Al final, aquí pasarás el DataFrame que venga de tu SQL/Excel
    # win = PantallaAnalisisDinamico(tu_dataframe_real)
    win = PantallaAnalisisDinamico() 
    win.show()
    sys.exit(app.exec())