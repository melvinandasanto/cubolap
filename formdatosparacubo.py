import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt

from formvistacubo import VistaPreviaDinamica
from claserutas import ClaseRutas
from claseconexiones import ClaseConexiones


class SeleccionOrigenOLAP(QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu
        self.setWindowTitle("Sistema OLAP - Seleccionar Origen de Datos")
        self.resize(1350, 700)

        self.tipo_origen_actual = "conexion"
        self.id_seleccionado = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }

            QWidget {
                color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QLabel#TituloSeccion {
                font-weight: bold;
                color: #3d85c6;
                font-size: 14px;
                text-transform: uppercase;
                margin-bottom: 5px;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 14px;
            }

            QPushButton#BtnTab {
                background-color: #243447;
                color: white;
                border: 1px solid #3a4a5e;
                padding: 8px;
            }

            QPushButton#BtnTab:hover {
                background-color: #2f4a5a;
            }

            QPushButton#BtnTabActivo {
                background-color: #3d85c6;
                color: white;
                border: 1px solid #5fa2dd;
                padding: 8px;
            }

            QPushButton#BtnVistaPrevia {
                background-color: #3d85c6;
                color: white;
                font-size: 13px;
                padding: 12px;
            }

            QPushButton#BtnVistaPrevia:hover {
                background-color: #5fa2dd;
            }

            QPushButton#BtnVolver {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 12px;
            }

            QPushButton#BtnVolver:hover {
                background-color: #d35400;
            }

            QTableWidget {
                background-color: #0d1b2a;
                border: none;
                gridline-color: #243447;
                selection-background-color: #3d85c6;
                color: white;
                font-size: 12px;
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
        self.mostrar_conexiones()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # ========== PANEL IZQUIERDO ==========
        panel_izquierdo = QVBoxLayout()

        # Título
        lbl_titulo = QLabel("Seleccione el origen")
        lbl_titulo.setObjectName("TituloSeccion")
        panel_izquierdo.addWidget(lbl_titulo)

        # Botones tipo pestaña
        layout_tabs = QHBoxLayout()
        layout_tabs.setSpacing(6)

        self.btn_conexiones = QPushButton("Conexiones")
        self.btn_conexiones.setObjectName("BtnTabActivo")
        self.btn_conexiones.clicked.connect(self.mostrar_conexiones)
        layout_tabs.addWidget(self.btn_conexiones)

        self.btn_rutas = QPushButton("Rutas")
        self.btn_rutas.setObjectName("BtnTab")
        self.btn_rutas.clicked.connect(self.mostrar_rutas)
        layout_tabs.addWidget(self.btn_rutas)

        panel_izquierdo.addLayout(layout_tabs)

        # Tabla principal
        self.tabla_origenes = QTableWidget()
        self.tabla_origenes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_origenes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla_origenes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_origenes.verticalHeader().setVisible(False)
        self.tabla_origenes.itemSelectionChanged.connect(self.actualizar_info_seleccion)
        panel_izquierdo.addWidget(self.tabla_origenes)

        layout_principal.addLayout(panel_izquierdo, 3)

        # ========== PANEL DERECHO (DETALLES E INFORMACIÓN) ==========
        panel_derecho = QVBoxLayout()

        # Información
        lbl_info = QLabel("INFORMACIÓN")
        lbl_info.setObjectName("TituloSeccion")
        panel_derecho.addWidget(lbl_info)

        self.lbl_tipo = QLabel("Tipo: Conexiones")
        self.lbl_tipo.setStyleSheet("font-weight: bold; color: #7fb3ff; font-size: 13px;")
        self.lbl_tipo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_derecho.addWidget(self.lbl_tipo)

        self.lbl_info_db = QLabel("Ningún origen seleccionado")
        self.lbl_info_db.setStyleSheet("color: #a0aeba; font-size: 12px; margin-top: 10px;")
        self.lbl_info_db.setWordWrap(True)
        self.lbl_info_db.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_derecho.addWidget(self.lbl_info_db)

        panel_derecho.addSpacing(20)

        # Botones de acción
        self.btn_vista_previa = QPushButton("→ Ir a Vista Previa")
        self.btn_vista_previa.setObjectName("BtnVistaPrevia")
        self.btn_vista_previa.clicked.connect(self.abrir_vista_previa)
        panel_derecho.addWidget(self.btn_vista_previa)

        self.btn_volver = QPushButton("Volver al Menú")
        self.btn_volver.setObjectName("BtnVolver")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        panel_derecho.addWidget(self.btn_volver)

        panel_derecho.addStretch()

        layout_principal.addLayout(panel_derecho, 1)

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
                id_origen=int(self.id_seleccionado),
                parent_menu=self
            )
            self.nueva_ventana.show()
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la vista previa.\n\n{str(e)}")

    def volver_al_menu(self):
        """Vuelve al menú principal"""
        if self.parent_menu:
            self.parent_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SeleccionOrigenOLAP()
    ventana.show()
    sys.exit(app.exec())