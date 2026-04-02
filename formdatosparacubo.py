import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt

from formvistacubo import VistaPreviaDinamica
from claserutas import ClaseRutas

# Ajusta este import al nombre real de tu clase CRUD de conexiones
# Debe tener al menos Listar()
from claseconexiones import ClaseConexiones


class SeleccionOrigenOLAP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Seleccionar Origen de Datos")
        self.resize(1350, 700)

        self.tipo_origen_actual = "conexion"
        self.id_seleccionado = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a2634;
            }

            QWidget {
                color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QLabel#TituloPrincipal {
                font-size: 22px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
            }

            QLabel#Subtitulo {
                font-size: 15px;
                color: #b8c7d9;
                margin-bottom: 8px;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }

            QPushButton#BtnTab {
                background-color: #243447;
                color: white;
                border: 1px solid #3a4a5e;
                min-width: 150px;
            }

            QPushButton#BtnTabActivo {
                background-color: #3d85c6;
                color: white;
                border: 1px solid #5fa2dd;
                min-width: 150px;
            }

            QPushButton#BtnVistaPrevia {
                background-color: #3d85c6;
                color: white;
                font-size: 15px;
            }

            QPushButton#BtnSalir {
                background-color: #3e5169;
                color: white;
                border: 1px solid #455a73;
                font-size: 14px;
            }

            QTableWidget {
                background-color: #0d1b2a;
                border: none;
                gridline-color: #243447;
                selection-background-color: #3d85c6;
                color: white;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #1b263b;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #3d85c6;
            }

            QFrame#PanelDetalles {
                background-color: #243447;
                border-radius: 15px;
                border: 1px solid #3a4a5e;
            }

            QLabel#LabelSeleccion {
                color: #2ecc71;
                font-weight: bold;
                font-size: 15px;
            }

            QLabel#LabelTipo {
                color: #7fb3ff;
                font-weight: bold;
                font-size: 14px;
            }
        """)

        self.init_ui()
        self.mostrar_conexiones()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # =========================
        # PANEL IZQUIERDO
        # =========================
        panel_izquierdo = QVBoxLayout()
        panel_izquierdo.setSpacing(15)

        self.lbl_titulo = QLabel("Seleccione el origen de datos para generar el Cubo OLAP")
        self.lbl_titulo.setObjectName("TituloPrincipal")
        panel_izquierdo.addWidget(self.lbl_titulo)

        self.lbl_subtitulo = QLabel("Puede elegir una conexión guardada o una ruta de archivo")
        self.lbl_subtitulo.setObjectName("Subtitulo")
        panel_izquierdo.addWidget(self.lbl_subtitulo)

        # Botones tipo pestaña
        layout_tabs = QHBoxLayout()
        layout_tabs.setSpacing(10)

        self.btn_conexiones = QPushButton("Conexiones")
        self.btn_conexiones.setObjectName("BtnTabActivo")
        self.btn_conexiones.clicked.connect(self.mostrar_conexiones)

        self.btn_rutas = QPushButton("Rutas")
        self.btn_rutas.setObjectName("BtnTab")
        self.btn_rutas.clicked.connect(self.mostrar_rutas)

        layout_tabs.addWidget(self.btn_conexiones)
        layout_tabs.addWidget(self.btn_rutas)
        layout_tabs.addStretch()

        panel_izquierdo.addLayout(layout_tabs)

        # Tabla principal
        self.tabla_origenes = QTableWidget()
        self.tabla_origenes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_origenes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla_origenes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_origenes.setAlternatingRowColors(False)
        self.tabla_origenes.verticalHeader().setVisible(False)
        self.tabla_origenes.itemSelectionChanged.connect(self.actualizar_info_seleccion)

        panel_izquierdo.addWidget(self.tabla_origenes)

        main_layout.addLayout(panel_izquierdo, stretch=4)

        # =========================
        # PANEL DERECHO
        # =========================
        self.panel_derecho = QFrame()
        self.panel_derecho.setObjectName("PanelDetalles")
        self.panel_derecho.setFixedWidth(340)

        layout_detalles = QVBoxLayout(self.panel_derecho)
        layout_detalles.setContentsMargins(20, 30, 20, 20)
        layout_detalles.setSpacing(18)

        titulo_detalle = QLabel("DETALLES DE SELECCIÓN")
        titulo_detalle.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout_detalles.addWidget(titulo_detalle)

        self.lbl_tipo = QLabel("Tipo actual: Conexiones")
        self.lbl_tipo.setObjectName("LabelTipo")
        self.lbl_tipo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_detalles.addWidget(self.lbl_tipo)

        self.lbl_info_db = QLabel("Ningún origen seleccionado")
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

    # =========================================================
    # CAMBIO DE PESTAÑA
    # =========================================================
    def mostrar_conexiones(self):
        self.tipo_origen_actual = "conexion"
        self.id_seleccionado = None

        self.btn_conexiones.setObjectName("BtnTabActivo")
        self.btn_rutas.setObjectName("BtnTab")
        self.actualizar_estilo_tabs()

        self.lbl_tipo.setText("Tipo actual: Conexiones")
        self.lbl_info_db.setText("Ninguna conexión seleccionada")

        self.cargar_tabla_conexiones()

    def mostrar_rutas(self):
        self.tipo_origen_actual = "ruta"
        self.id_seleccionado = None

        self.btn_conexiones.setObjectName("BtnTab")
        self.btn_rutas.setObjectName("BtnTabActivo")
        self.actualizar_estilo_tabs()

        self.lbl_tipo.setText("Tipo actual: Rutas")
        self.lbl_info_db.setText("Ninguna ruta seleccionada")

        self.cargar_tabla_rutas()

    def actualizar_estilo_tabs(self):
        # Reaplicar estilos para refrescar objectName
        self.btn_conexiones.style().unpolish(self.btn_conexiones)
        self.btn_conexiones.style().polish(self.btn_conexiones)

        self.btn_rutas.style().unpolish(self.btn_rutas)
        self.btn_rutas.style().polish(self.btn_rutas)

    # =========================================================
    # CARGA DE DATOS EN TABLA
    # =========================================================
    def cargar_tabla_conexiones(self):
        self.tabla_origenes.clear()

        encabezados = [
            "ID", "Gestor", "Host", "Puerto", "Usuario", "Contraseña", "Base de Datos"
        ]
        self.tabla_origenes.setColumnCount(len(encabezados))
        self.tabla_origenes.setHorizontalHeaderLabels(encabezados)

        try:
            datos = ClaseConexiones().Listar()

            if not datos:
                self.tabla_origenes.setRowCount(0)
                self.tabla_origenes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                return

            self.tabla_origenes.setRowCount(len(datos))

            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    texto = "" if valor is None else str(valor)
                    item = QTableWidgetItem(texto)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tabla_origenes.setItem(fila, columna, item)

            self.tabla_origenes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las conexiones.\n\n{str(e)}")

    def cargar_tabla_rutas(self):
        self.tabla_origenes.clear()

        encabezados = ["ID", "Ruta"]
        self.tabla_origenes.setColumnCount(len(encabezados))
        self.tabla_origenes.setHorizontalHeaderLabels(encabezados)

        try:
            datos = ClaseRutas().Listar()

            if not datos:
                self.tabla_origenes.setRowCount(0)
                self.tabla_origenes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                return

            self.tabla_origenes.setRowCount(len(datos))

            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    texto = "" if valor is None else str(valor)
                    item = QTableWidgetItem(texto)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tabla_origenes.setItem(fila, columna, item)

            self.tabla_origenes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las rutas.\n\n{str(e)}")

    # =========================================================
    # SELECCIÓN
    # =========================================================
    def actualizar_info_seleccion(self):
        fila = self.tabla_origenes.currentRow()

        if fila == -1:
            self.id_seleccionado = None
            if self.tipo_origen_actual == "conexion":
                self.lbl_info_db.setText("Ninguna conexión seleccionada")
            else:
                self.lbl_info_db.setText("Ninguna ruta seleccionada")
            return

        item_id = self.tabla_origenes.item(fila, 0)
        self.id_seleccionado = item_id.text() if item_id else None

        if self.tipo_origen_actual == "conexion":
            gestor_item = self.tabla_origenes.item(fila, 1)
            host_item = self.tabla_origenes.item(fila, 2)
            bd_item = self.tabla_origenes.item(fila, 6)

            gestor = gestor_item.text() if gestor_item else "N/A"
            host = host_item.text() if host_item else "N/A"
            bd = bd_item.text() if bd_item else "N/A"

            self.lbl_info_db.setText(
                f"Conexión seleccionada:\n\n"
                f"Gestor: {gestor}\n"
                f"Host: {host}\n"
                f"Base de datos: {bd}"
            )

        else:
            ruta_item = self.tabla_origenes.item(fila, 1)
            ruta = ruta_item.text() if ruta_item else "N/A"

            self.lbl_info_db.setText(
                f"Ruta seleccionada:\n\n{ruta}"
            )

    # =========================================================
    # NAVEGAR A VISTA PREVIA
    # =========================================================
    def abrir_vista_previa(self):
        fila = self.tabla_origenes.currentRow()

        if fila == -1 or not self.id_seleccionado:
            QMessageBox.warning(self, "Aviso", "Debe seleccionar una fila de la tabla primero.")
            return

        try:
            self.nueva_ventana = VistaPreviaDinamica(
                tipo_origen=self.tipo_origen_actual,
                id_origen=int(self.id_seleccionado)
            )
            self.nueva_ventana.show()
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la vista previa.\n\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SeleccionOrigenOLAP()
    ventana.show()
    sys.exit(app.exec())