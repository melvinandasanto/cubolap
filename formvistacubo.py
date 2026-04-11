import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt

from formcubo import PantallaAnalisisDinamico
from claserutas import ClaseRutas
from claseconexiones import ClaseConexiones
from constructormodelodatos import ConstructorModeloDatos


class VistaPreviaDinamica(QMainWindow):
    def __init__(self, tipo_origen, id_origen, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu

        self.tipo_origen = tipo_origen
        self.id_origen = id_origen
        self.limite_default = 100

        self.modelo_datos = None
        self.entidad_actual = None
        self.datos_cargados = False

        self.setWindowTitle("Sistema OLAP - Vista Previa Estructural")
        self.resize(1450, 800)

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
                font-size: 16px;
                font-weight: bold;
                color: #3d85c6;
            }

            QLabel#LblSecundario {
                color: #a0aeba;
                font-size: 13px;
            }

            QLabel#TituloSeccion {
                font-size: 14px;
                font-weight: bold;
                color: #7fb3ff;
                margin-bottom: 6px;
            }

            QLineEdit, QListWidget, QTableWidget {
                background-color: #0d1b2a;
                border: 1px solid #243447;
                color: #e0e0e0;
            }

            QLineEdit {
                border-radius: 6px;
                padding: 8px;
                background-color: #243447;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 14px;
            }

            QPushButton#BtnRecargar {
                background-color: #3d85c6;
                color: white;
            }

            QPushButton#BtnCargarDatos {
                background-color: #f39c12;
                color: white;
            }

            QPushButton#BtnAnalizar {
                background-color: #2ecc71;
                color: white;
                min-width: 180px;
            }

            QPushButton#BtnVolver {
                background-color: #e67e22;
                color: white;
                min-width: 100px;
            }

            QListWidget {
                padding: 6px;
            }

            QTableWidget {
                gridline-color: #243447;
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
        self.cargar_modelo_inicial()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # =========================
        # BANNER SUPERIOR
        # =========================
        self.banner = QFrame()
        self.banner.setObjectName("BannerRuta")
        layout_banner = QVBoxLayout(self.banner)

        self.lbl_origen = QLabel("ORIGEN DE DATOS: Cargando...")
        self.lbl_origen.setObjectName("LblBanner")

        self.lbl_info = QLabel("Preparando estructura del origen")
        self.lbl_info.setObjectName("LblSecundario")

        layout_banner.addWidget(self.lbl_origen)
        layout_banner.addWidget(self.lbl_info)

        main_layout.addWidget(self.banner)

        # =========================
        # CONTROLES SUPERIORES
        # =========================
        controles = QHBoxLayout()
        controles.setContentsMargins(20, 15, 20, 5)
        controles.setSpacing(10)

        controles.addWidget(QLabel("Filas de vista previa:"))

        self.txt_limite = QLineEdit()
        self.txt_limite.setText(str(self.limite_default))
        self.txt_limite.setFixedWidth(120)
        controles.addWidget(self.txt_limite)

        self.btn_recargar = QPushButton("Recargar estructura")
        self.btn_recargar.setObjectName("BtnRecargar")
        self.btn_recargar.clicked.connect(self.cargar_modelo_inicial)
        controles.addWidget(self.btn_recargar)

        self.btn_cargar_datos = QPushButton("Cargar datos")
        self.btn_cargar_datos.setObjectName("BtnCargarDatos")
        self.btn_cargar_datos.clicked.connect(self.cargar_datos_completos)
        controles.addWidget(self.btn_cargar_datos)

        controles.addStretch()
        main_layout.addLayout(controles)

        # =========================
        # PANEL CENTRAL
        # =========================
        paneles = QHBoxLayout()
        paneles.setContentsMargins(20, 10, 20, 10)
        paneles.setSpacing(15)

        # ----- Panel entidades -----
        panel_entidades = QVBoxLayout()
        lbl_entidades = QLabel("Entidades")
        lbl_entidades.setObjectName("TituloSeccion")
        panel_entidades.addWidget(lbl_entidades)

        self.lista_entidades = QListWidget()
        self.lista_entidades.itemSelectionChanged.connect(self.cambiar_entidad)
        panel_entidades.addWidget(self.lista_entidades)

        paneles.addLayout(panel_entidades, 2)

        # ----- Panel columnas -----
        panel_columnas = QVBoxLayout()
        lbl_columnas = QLabel("Columnas")
        lbl_columnas.setObjectName("TituloSeccion")
        panel_columnas.addWidget(lbl_columnas)

        self.tabla_columnas = QTableWidget()
        self.tabla_columnas.setColumnCount(4)
        self.tabla_columnas.setHorizontalHeaderLabels(["Nombre", "Tipo", "Nulo", "Longitud"])
        self.tabla_columnas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        panel_columnas.addWidget(self.tabla_columnas)

        paneles.addLayout(panel_columnas, 3)

        main_layout.addLayout(paneles, 3)

        # =========================
        # PREVIEW
        # =========================
        preview_layout = QVBoxLayout()
        preview_layout.setContentsMargins(20, 0, 20, 10)

        lbl_preview = QLabel("Vista previa de datos")
        lbl_preview.setObjectName("TituloSeccion")
        preview_layout.addWidget(lbl_preview)

        self.tabla_preview = QTableWidget()
        self.tabla_preview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.tabla_preview.horizontalHeader().setStretchLastSection(True)
        preview_layout.addWidget(self.tabla_preview)

        main_layout.addLayout(preview_layout, 4)

        # =========================
        # BOTONES INFERIORES
        # =========================
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(20, 10, 20, 15)

        self.btn_volver = QPushButton("Volver a Datos")
        self.btn_volver.setObjectName("BtnVolver")
        self.btn_volver.clicked.connect(self.volver_a_datos)

        self.btn_analizar = QPushButton("Ir al Cubo")
        self.btn_analizar.setObjectName("BtnAnalizar")
        self.btn_analizar.setEnabled(False)
        self.btn_analizar.clicked.connect(self.abrir_analisis)

        btn_layout.addWidget(self.btn_volver)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_analizar)

        main_layout.addLayout(btn_layout)

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
                f"El número de filas debe ser mayor que 0. Se usará {self.limite_default}."
            )
            self.txt_limite.setText(str(self.limite_default))
            return self.limite_default

    def cargar_modelo_inicial(self):
        try:
            limite = self.obtener_limite()
            constructor = ConstructorModeloDatos()

            if self.tipo_origen == "conexion":
                obj_conexion = ClaseConexiones()
                encontrado = obj_conexion.Buscar(self.id_origen)

                if not encontrado:
                    raise Exception("No se encontró la conexión seleccionada")

                self.modelo_datos = constructor.construir_desde_conexion(
                    gestor=obj_conexion.gestor,
                    host=obj_conexion.host,
                    database=obj_conexion.basedatos,
                    user=obj_conexion.usuario,
                    password=obj_conexion.contrasenia,
                    port=obj_conexion.puerto,
                    limite_preview=limite,
                    cargar_completa=False
                )

            elif self.tipo_origen == "ruta":
                obj_ruta = ClaseRutas()
                encontrado = obj_ruta.Buscar(self.id_origen)

                if not encontrado:
                    raise Exception("No se encontró la ruta seleccionada")

                self.modelo_datos = constructor.construir_desde_ruta(
                    ruta_archivo=obj_ruta.nombre_ruta,
                    limite_preview=limite,
                    cargar_completa=False
                )
            else:
                raise Exception("Tipo de origen no válido")

            self.datos_cargados = False
            self.btn_analizar.setEnabled(False)

            self.actualizar_encabezado()
            self.cargar_lista_entidades()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def cargar_datos_completos(self):
        try:
            limite = self.obtener_limite()
            constructor = ConstructorModeloDatos()

            if self.tipo_origen == "conexion":
                obj_conexion = ClaseConexiones()
                encontrado = obj_conexion.Buscar(self.id_origen)

                if not encontrado:
                    raise Exception("No se encontró la conexión seleccionada")

                self.modelo_datos = constructor.construir_desde_conexion(
                    gestor=obj_conexion.gestor,
                    host=obj_conexion.host,
                    database=obj_conexion.basedatos,
                    user=obj_conexion.usuario,
                    password=obj_conexion.contrasenia,
                    port=obj_conexion.puerto,
                    limite_preview=limite,
                    cargar_completa=True
                )

            elif self.tipo_origen == "ruta":
                obj_ruta = ClaseRutas()
                encontrado = obj_ruta.Buscar(self.id_origen)

                if not encontrado:
                    raise Exception("No se encontró la ruta seleccionada")

                self.modelo_datos = constructor.construir_desde_ruta(
                    ruta_archivo=obj_ruta.nombre_ruta,
                    limite_preview=limite,
                    cargar_completa=True
                )
            else:
                raise Exception("Tipo de origen no válido")

            self.datos_cargados = True
            self.btn_analizar.setEnabled(True)

            self.actualizar_encabezado()
            self.cargar_lista_entidades()

            total_entidades = len(self.modelo_datos["entidades"])

            # Verificación rápida en terminal
            for nombre, entidad in self.modelo_datos["entidades"].items():
                df = entidad.get("dataframe")
                print(nombre, "->", "CARGADO" if df is not None else "VACÍO")

            QMessageBox.information(
                self,
                "Carga completada",
                f"Los datos se cargaron correctamente.\n\nEntidades cargadas: {total_entidades}"
            )

        except Exception as e:
            self.datos_cargados = False
            self.btn_analizar.setEnabled(False)
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar los datos completos.\n\n{str(e)}"
            )

    def actualizar_encabezado(self):
        if not self.modelo_datos:
            return

        self.lbl_origen.setText(
            f"ORIGEN DE DATOS: {self.modelo_datos['nombre_origen']}"
        )

        total_entidades = len(self.modelo_datos["entidades"])
        total_relaciones = len(self.modelo_datos["relaciones"])
        estado = "Datos completos cargados" if self.datos_cargados else "Solo estructura cargada"

        self.lbl_info.setText(
            f"Tipo: {self.modelo_datos['tipo_origen']} | "
            f"Entidades: {total_entidades} | "
            f"Relaciones detectadas: {total_relaciones} | "
            f"Estado: {estado}"
        )

    def cargar_lista_entidades(self):
        self.lista_entidades.clear()
        self.tabla_columnas.clearContents()
        self.tabla_columnas.setRowCount(0)
        self.tabla_preview.clear()
        self.tabla_preview.setRowCount(0)
        self.tabla_preview.setColumnCount(0)
        self.entidad_actual = None

        if not self.modelo_datos or not self.modelo_datos["entidades"]:
            return

        for nombre, entidad in self.modelo_datos["entidades"].items():
            texto = f"{nombre}  |  {entidad['filas']} filas  |  {len(entidad['columnas'])} columnas"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, nombre)
            self.lista_entidades.addItem(item)

        if self.lista_entidades.count() > 0:
            self.lista_entidades.setCurrentRow(0)

    def cambiar_entidad(self):
        items = self.lista_entidades.selectedItems()
        if not items or not self.modelo_datos:
            return

        nombre_entidad = items[0].data(Qt.ItemDataRole.UserRole)
        self.entidad_actual = self.modelo_datos["entidades"][nombre_entidad]

        self.mostrar_columnas(self.entidad_actual["columnas"])
        self.mostrar_preview(self.entidad_actual["preview"])

    def mostrar_columnas(self, columnas):
        self.tabla_columnas.clearContents()
        self.tabla_columnas.setRowCount(len(columnas))

        for i, col in enumerate(columnas):
            self.tabla_columnas.setItem(i, 0, QTableWidgetItem(str(col.get("nombre", ""))))
            self.tabla_columnas.setItem(i, 1, QTableWidgetItem(str(col.get("tipo", ""))))
            self.tabla_columnas.setItem(i, 2, QTableWidgetItem("Sí" if col.get("nulo", False) else "No"))
            self.tabla_columnas.setItem(
                i,
                3,
                QTableWidgetItem("" if col.get("longitud") is None else str(col.get("longitud")))
            )

    def mostrar_preview(self, dataframe):
        if dataframe is None or dataframe.empty:
            self.tabla_preview.clear()
            self.tabla_preview.setRowCount(0)
            self.tabla_preview.setColumnCount(0)
            return

        columnas = [str(c) for c in dataframe.columns]

        self.tabla_preview.clear()
        self.tabla_preview.setColumnCount(len(columnas))
        self.tabla_preview.setHorizontalHeaderLabels(columnas)
        self.tabla_preview.setRowCount(len(dataframe))

        for i in range(len(dataframe)):
            for j in range(len(columnas)):
                self.tabla_preview.setItem(i, j, QTableWidgetItem(str(dataframe.iloc[i, j])))

        self.tabla_preview.resizeColumnsToContents()

    def abrir_analisis(self):
        if not self.modelo_datos or not self.modelo_datos["entidades"]:
            QMessageBox.warning(self, "Aviso", "No hay modelo cargado para analizar.")
            return

        if not self.datos_cargados:
            QMessageBox.warning(
                self,
                "Aviso",
                "Primero debe cargar los datos antes de ir al cubo."
            )
            return

        self.ventana_analisis = PantallaAnalisisDinamico(self.modelo_datos, self)
        self.ventana_analisis.show()
        self.hide()

    def volver_a_datos(self):
        """Vuelve a SeleccionOrigenOLAP"""
        if self.parent_menu:
            self.parent_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VistaPreviaDinamica(tipo_origen="ruta", id_origen=1)
    ventana.show()
    sys.exit(app.exec())