import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt

from formcubo import PantallaAnalisisDinamico
from claserutas import ClaseRutas
from claseconexiones import ClaseConexiones
from conexionorigen import ConexionOrigen


class VistaPreviaDinamica(QMainWindow):
    def __init__(self, tipo_origen, id_origen):
        super().__init__()

        self.tipo_origen = tipo_origen
        self.id_origen = id_origen
        self.df_actual = pd.DataFrame()
        self.limite_default = 100

        self.gestor = None
        self.host = None
        self.puerto = None
        self.usuario = None
        self.contrasenia = None
        self.basedatos = None
        self.tabla_guardada = None
        self.ruta_activa = None

        self.setWindowTitle("Sistema OLAP - Vista Previa de Datos")
        self.resize(1300, 750)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a2634;
            }

            QWidget {
                color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QFrame#BannerRuta {
                background-color: #1b263b;
                border-bottom: 2px solid #3d85c6;
                padding: 12px;
            }

            QLabel#LblBanner {
                font-size: 15px;
                font-weight: bold;
                color: #3d85c6;
            }

            QLabel#LblSecundario {
                color: #a0aeba;
                font-size: 13px;
            }

            QLineEdit, QComboBox {
                background-color: #243447;
                border: 1px solid #3a4a5e;
                border-radius: 6px;
                padding: 8px;
                color: white;
                min-height: 18px;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 14px;
            }

            QPushButton#BtnCargar {
                background-color: #3d85c6;
                color: white;
            }

            QPushButton#BtnAnalizar {
                background-color: #2ecc71;
                color: white;
                min-width: 180px;
            }

            QPushButton#BtnSalir {
                background-color: #c63d3d;
                color: white;
                min-width: 100px;
            }

            QTableWidget {
                background-color: #0d1b2a;
                border: none;
                gridline-color: #243447;
                color: #e0e0e0;
                selection-background-color: #3d85c6;
            }

            QHeaderView::section {
                background-color: #243447;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: #3d85c6;
            }
        """)

        self.init_ui()
        self.cargar_configuracion_inicial()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.banner = QFrame()
        self.banner.setObjectName("BannerRuta")
        layout_banner = QVBoxLayout(self.banner)

        self.lbl_origen = QLabel("ORIGEN DE DATOS: Cargando...")
        self.lbl_origen.setObjectName("LblBanner")

        self.lbl_info = QLabel("Preparando vista previa")
        self.lbl_info.setObjectName("LblSecundario")

        layout_banner.addWidget(self.lbl_origen)
        layout_banner.addWidget(self.lbl_info)
        main_layout.addWidget(self.banner)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(25, 20, 25, 20)
        content_layout.setSpacing(15)

        lbl_msg = QLabel("Vista previa de la estructura de datos seleccionada:")
        lbl_msg.setStyleSheet("color: #a0aeba;")
        content_layout.addWidget(lbl_msg)

        controles_layout = QHBoxLayout()
        controles_layout.setSpacing(10)

        self.lbl_filas = QLabel("Filas a visualizar:")
        controles_layout.addWidget(self.lbl_filas)

        self.txt_limite = QLineEdit()
        self.txt_limite.setPlaceholderText("Ejemplo: 100")
        self.txt_limite.setText(str(self.limite_default))
        self.txt_limite.setFixedWidth(120)
        controles_layout.addWidget(self.txt_limite)

        self.lbl_tabla = QLabel("Tabla:")
        controles_layout.addWidget(self.lbl_tabla)

        self.combo_tablas = QComboBox()
        self.combo_tablas.setMinimumWidth(250)
        controles_layout.addWidget(self.combo_tablas)

        self.btn_cargar = QPushButton("Cargar vista previa")
        self.btn_cargar.setObjectName("BtnCargar")
        self.btn_cargar.clicked.connect(self.recargar_vista_previa)
        controles_layout.addWidget(self.btn_cargar)

        controles_layout.addStretch()
        content_layout.addLayout(controles_layout)

        self.tabla = QTableWidget()
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        content_layout.addWidget(self.tabla)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 15, 0, 10)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)

        self.btn_analizar = QPushButton("Analizar mis Datos")
        self.btn_analizar.setObjectName("BtnAnalizar")
        self.btn_analizar.clicked.connect(self.abrir_analisis)

        btn_layout.addWidget(self.btn_salir)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_analizar)

        content_layout.addLayout(btn_layout)
        main_layout.addLayout(content_layout)

    def obtener_limite(self):
        texto = self.txt_limite.text().strip()

        if not texto:
            return self.limite_default

        try:
            limite = int(texto)
            if limite <= 0:
                raise ValueError
            return limite
        except ValueError:
            QMessageBox.warning(
                self,
                "Aviso",
                f"El número de filas debe ser un entero mayor que 0. Se usará {self.limite_default}."
            )
            self.txt_limite.setText(str(self.limite_default))
            return self.limite_default

    def cargar_configuracion_inicial(self):
        try:
            if self.tipo_origen == "ruta":
                self.configurar_modo_ruta()
            elif self.tipo_origen == "conexion":
                self.configurar_modo_conexion()
            else:
                raise Exception("Tipo de origen no válido")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def configurar_modo_ruta(self):
        self.lbl_tabla.hide()
        self.combo_tablas.hide()

        clase_ruta = ClaseRutas()
        encontrado = clase_ruta.Buscar(self.id_origen)

        if not encontrado:
            raise Exception("No se encontró la ruta seleccionada")

        self.ruta_activa = clase_ruta.nombre_ruta

        self.lbl_origen.setText("ORIGEN DE DATOS: Ruta")
        self.lbl_info.setText(self.ruta_activa)

        self.cargar_desde_ruta()

    def configurar_modo_conexion(self):
        obj_conexion = ClaseConexiones()
        encontrado = obj_conexion.Buscar(self.id_origen)

        if not encontrado:
            raise Exception("No se encontró la conexión seleccionada")

        self.gestor = obj_conexion.gestor
        self.host = obj_conexion.host
        self.puerto = obj_conexion.puerto
        self.usuario = obj_conexion.usuario
        self.contrasenia = obj_conexion.contrasenia
        self.basedatos = obj_conexion.basedatos
        self.tabla_guardada = obj_conexion.tabla

        self.lbl_origen.setText(f"ORIGEN DE DATOS: {self.gestor} - {self.basedatos}")

        if self.tabla_guardada is not None and str(self.tabla_guardada).strip() != "":
            self.lbl_info.setText(f"Host: {self.host} | Tabla guardada: {self.tabla_guardada}")
            self.lbl_tabla.hide()
            self.combo_tablas.hide()
        else:
            self.lbl_info.setText(f"Host: {self.host} | Seleccione una tabla")
            self.lbl_tabla.show()
            self.combo_tablas.show()
            self.cargar_tablas_conexion()

        self.recargar_vista_previa()

    def crear_conexion_externa(self):
        return ConexionOrigen(
            gestor=self.gestor,
            host=self.host,
            database=self.basedatos,
            user=self.usuario,
            password=self.contrasenia,
            port=self.puerto
        )

    def cargar_tablas_conexion(self):
        conexion = self.crear_conexion_externa()
        tablas = conexion.obtener_tablas()

        self.combo_tablas.clear()

        if not tablas:
            raise Exception("No se encontraron tablas en la base de datos")

        self.combo_tablas.addItems(tablas)

    def recargar_vista_previa(self):
        try:
            if self.tipo_origen == "ruta":
                self.cargar_desde_ruta()
            else:
                self.cargar_desde_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def cargar_desde_ruta(self):
        limite = self.obtener_limite()

        clase_ruta = ClaseRutas()
        encontrado = clase_ruta.Buscar(self.id_origen)

        if not encontrado:
            raise Exception("No se encontró la ruta seleccionada")

        ok, resultado = clase_ruta.cargar_datos(clase_ruta.nombre_ruta)

        if not ok:
            raise Exception(f"No se pudo cargar el archivo.\n\n{resultado}")

        df = resultado.head(limite).copy()
        self.df_actual = df

        self.lbl_info.setText(f"{clase_ruta.nombre_ruta} | Mostrando {len(df)} filas")
        self.mostrar_dataframe(df)

    def cargar_desde_conexion(self):
        limite = self.obtener_limite()

        if self.tabla_guardada is not None and str(self.tabla_guardada).strip() != "":
            tabla_usar = self.tabla_guardada
        else:
            tabla_usar = self.combo_tablas.currentText().strip()

        if not tabla_usar:
            raise Exception("Debe seleccionar una tabla")

        conexion = self.crear_conexion_externa()
        df = conexion.cargar_tabla(tabla_usar, limite=limite)

        self.df_actual = df
        self.lbl_info.setText(
            f"Host: {self.host} | Tabla: {tabla_usar} | Mostrando {len(df)} filas"
        )
        self.mostrar_dataframe(df)

    def mostrar_dataframe(self, dataframe):
        if dataframe is None or dataframe.empty:
            self.tabla.clear()
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            QMessageBox.warning(self, "Aviso", "No hay datos para mostrar.")
            return

        columnas = [str(col) for col in dataframe.columns]

        self.tabla.clear()
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        self.tabla.setRowCount(len(dataframe))

        for i in range(len(dataframe)):
            for j in range(len(columnas)):
                valor = str(dataframe.iloc[i, j])
                self.tabla.setItem(i, j, QTableWidgetItem(valor))

        self.tabla.resizeColumnsToContents()

    def abrir_analisis(self):
        if self.df_actual is None or self.df_actual.empty:
            QMessageBox.warning(self, "Aviso", "No hay datos cargados para analizar.")
            return

        self.ventana_analisis = PantallaAnalisisDinamico(self.df_actual)
        self.ventana_analisis.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VistaPreviaDinamica(tipo_origen="ruta", id_origen=1)
    ventana.show()
    sys.exit(app.exec())