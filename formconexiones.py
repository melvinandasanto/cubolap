import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt

from claseconexiones import ClaseConexiones


class AdministradorConexiones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Administrador de Conexiones")
        self.setMinimumSize(1200, 700)
        self.id_seleccionado = None

        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }

            QTableWidget {
                background-color: #0d1b2a;
                border: none;
                gridline-color: #243447;
                selection-background-color: #3d85c6;
                font-size: 13px;
                color: white;
            }

            QHeaderView::section {
                background-color: #1b263b;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #3d85c6;
            }

            QFrame#PanelLateral {
                background-color: #243447;
                border-radius: 15px;
                border: 1px solid #3a4a5e;
            }

            QLabel#TituloSeccion {
                font-size: 18px;
                font-weight: bold;
                color: #3d85c6;
                margin-bottom: 10px;
            }

            QLabel#LblAyuda {
                color: #9fb3c8;
                font-size: 11px;
            }

            QLineEdit, QComboBox {
                background-color: #304156;
                border: 1px solid #455a73;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                min-height: 20px;
            }

            QPushButton#BtnProbar {
                background-color: #2ecc71;
                color: white;
                border: none;
            }

            QPushButton#BtnGuardar {
                background-color: #3d85c6;
                color: white;
            }

            QPushButton#BtnActualizar {
                background-color: #3e5169;
                color: white;
                border: 1px solid #455a73;
            }

            QPushButton#BtnEliminar {
                background-color: #c63d3d;
                color: white;
            }

            QMessageBox {
                background-color: #243447;
            }

            QMessageBox QLabel {
                color: white;
            }
        """)

        self.init_ui()
        self.actualizar_placeholders()
        self.cargar_datos()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # IZQUIERDA
        left_container = QVBoxLayout()

        lbl_lista = QLabel("Listado de Conexiones")
        lbl_lista.setStyleSheet("font-size: 22px; font-weight: bold;")
        left_container.addWidget(lbl_lista)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Gestor", "Host", "Puerto", "Base de Datos", "Tabla"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.cellClicked.connect(self.seleccionar_fila)
        left_container.addWidget(self.table)

        main_layout.addLayout(left_container, stretch=3)

        # DERECHA
        self.panel = QFrame()
        self.panel.setObjectName("PanelLateral")
        self.panel.setFixedWidth(350)
        self.panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        form_layout = QVBoxLayout(self.panel)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        lbl_tit = QLabel("GESTIÓN DE CONEXIÓN")
        lbl_tit.setObjectName("TituloSeccion")
        lbl_tit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(lbl_tit)

        form_layout.addWidget(QLabel("Tipo de Gestor:"))
        self.cb_gestor = QComboBox()
        self.cb_gestor.addItems(["mysql", "sqlserver"])
        self.cb_gestor.currentTextChanged.connect(self.actualizar_placeholders)
        form_layout.addWidget(self.cb_gestor)

        form_layout.addWidget(QLabel("Host / Servidor:"))
        self.txt_host = QLineEdit()
        form_layout.addWidget(self.txt_host)

        form_layout.addWidget(QLabel("Puerto:"))
        self.txt_puerto = QLineEdit()
        form_layout.addWidget(self.txt_puerto)

        form_layout.addWidget(QLabel("Usuario:"))
        self.txt_user = QLineEdit()
        form_layout.addWidget(self.txt_user)

        form_layout.addWidget(QLabel("Contraseña:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.txt_pass)

        form_layout.addWidget(QLabel("Base de Datos:"))
        self.txt_db = QLineEdit()
        form_layout.addWidget(self.txt_db)

        form_layout.addWidget(QLabel("Tabla:"))
        self.txt_tabla = QLineEdit()
        form_layout.addWidget(self.txt_tabla)

        self.lbl_ayuda = QLabel("")
        self.lbl_ayuda.setObjectName("LblAyuda")
        self.lbl_ayuda.setWordWrap(True)
        form_layout.addWidget(self.lbl_ayuda)

        self.btn_probar = QPushButton("Probar Conexión")
        self.btn_probar.setObjectName("BtnProbar")
        self.btn_probar.clicked.connect(self.probar_conexion_logica)
        form_layout.addWidget(self.btn_probar)

        self.btn_guardar = QPushButton("Guardar Conexión")
        self.btn_guardar.setObjectName("BtnGuardar")
        self.btn_guardar.clicked.connect(self.guardar_conexion)
        form_layout.addWidget(self.btn_guardar)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setObjectName("BtnActualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_conexion)
        form_layout.addWidget(self.btn_actualizar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_conexion)
        form_layout.addWidget(self.btn_eliminar)

        form_layout.addStretch()
        main_layout.addWidget(self.panel)

    def actualizar_placeholders(self):
        gestor = self.cb_gestor.currentText().lower()

        self.txt_host.setPlaceholderText("Ej: localhost o .\\SQLEXPRESS")

        if gestor == "mysql":
            self.txt_puerto.setPlaceholderText("Obligatorio en MySQL. Ej: 3306")
            self.txt_user.setPlaceholderText("Obligatorio en MySQL")
            self.txt_pass.setPlaceholderText("Obligatoria en MySQL")
            self.lbl_ayuda.setText(
                "MySQL: normalmente requiere host, puerto, usuario, contraseña, "
                "base de datos y tabla."
            )
        else:
            self.txt_puerto.setPlaceholderText("Opcional en SQL Server. Ej: 1433")
            self.txt_user.setPlaceholderText("Opcional en SQL Server")
            self.txt_pass.setPlaceholderText("Opcional en SQL Server")
            self.lbl_ayuda.setText(
                "SQL Server: puerto, usuario y contraseña pueden ser opcionales "
                "si usás autenticación integrada."
            )

        self.txt_db.setPlaceholderText("Nombre de la base de datos")
        self.txt_tabla.setPlaceholderText("Tabla a consultar para el cubo")

    def validar_campos(self):
        gestor = self.cb_gestor.currentText().lower()
        host = self.txt_host.text().strip()
        puerto = self.txt_puerto.text().strip()
        usuario = self.txt_user.text().strip()
        contrasenia = self.txt_pass.text().strip()
        basedatos = self.txt_db.text().strip()
        tabla = self.txt_tabla.text().strip()

        if not host or not basedatos or not tabla:
            QMessageBox.warning(
                self, "Validación",
                "Host, Base de Datos y Tabla son obligatorios."
            )
            return False

        if gestor == "mysql":
            if not puerto or not usuario or not contrasenia:
                QMessageBox.warning(
                    self, "Validación",
                    "En MySQL, Puerto, Usuario y Contraseña son obligatorios."
                )
                return False

        return True

    def obtener_objeto_conexion(self):
        return ClaseConexiones(
            gestor=self.cb_gestor.currentText().strip().lower(),
            host=self.txt_host.text().strip(),
            puerto=self.txt_puerto.text().strip() or None,
            usuario=self.txt_user.text().strip() or None,
            contrasenia=self.txt_pass.text().strip() or None,
            basedatos=self.txt_db.text().strip(),
            tabla=self.txt_tabla.text().strip()
        )

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.cb_gestor.setCurrentIndex(0)
        self.txt_host.clear()
        self.txt_puerto.clear()
        self.txt_user.clear()
        self.txt_pass.clear()
        self.txt_db.clear()
        self.txt_tabla.clear()
        self.actualizar_placeholders()

    def probar_conexion_logica(self):
        if not self.validar_campos():
            return

        obj = self.obtener_objeto_conexion()

        try:
            if obj.probarconexion():
                QMessageBox.information(self, "Estado", "Conexión exitosa al servidor.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo establecer la conexión.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al conectar:\n{str(e)}")

    def guardar_conexion(self):
        if not self.validar_campos():
            return

        obj = self.obtener_objeto_conexion()

        try:
            resultado = obj.Guardar()
            if resultado:
                QMessageBox.information(self, "Éxito", "Conexión guardada correctamente.")
                self.cargar_datos()
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar la conexión.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{str(e)}")

    def actualizar_conexion(self):
        if self.id_seleccionado is None:
            QMessageBox.warning(self, "Validación", "Seleccione una conexión de la tabla.")
            return

        if not self.validar_campos():
            return

        obj = self.obtener_objeto_conexion()

        try:
            resultado = obj.Editar(self.id_seleccionado)
            if resultado:
                QMessageBox.information(self, "Éxito", "Conexión actualizada correctamente.")
                self.cargar_datos()
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la conexión.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{str(e)}")

    def eliminar_conexion(self):
        if self.id_seleccionado is None:
            QMessageBox.warning(self, "Validación", "Seleccione una conexión de la tabla.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar",
            "¿Desea eliminar la conexión seleccionada?"
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                obj = ClaseConexiones()
                resultado = obj.Eliminar(self.id_seleccionado)
                if resultado:
                    QMessageBox.information(self, "Éxito", "Conexión eliminada correctamente.")
                    self.cargar_datos()
                    self.limpiar_formulario()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar la conexión.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{str(e)}")

    def cargar_datos(self):
        try:
            obj = ClaseConexiones()
            datos = obj.Listar() or []

            self.table.setRowCount(len(datos))

            for fila, registro in enumerate(datos):
                # registro = idconexion, gestor, host, puerto, usuario, contrasenia, basedatos, tabla
                self.table.setItem(fila, 0, QTableWidgetItem(str(registro[1] or "")))
                self.table.setItem(fila, 1, QTableWidgetItem(str(registro[2] or "")))
                self.table.setItem(fila, 2, QTableWidgetItem(str(registro[3] or "")))
                self.table.setItem(fila, 3, QTableWidgetItem(str(registro[6] or "")))
                self.table.setItem(fila, 4, QTableWidgetItem(str(registro[7] or "")))

                # guardar el id oculto en la primera columna
                self.table.item(fila, 0).setData(Qt.ItemDataRole.UserRole, registro[0])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla:\n{str(e)}")

    def seleccionar_fila(self, fila, columna):
        try:
            item = self.table.item(fila, 0)
            if not item:
                return

            conexion_id = item.data(Qt.ItemDataRole.UserRole)
            obj = ClaseConexiones()

            if obj.Buscar(conexion_id):
                self.id_seleccionado = obj.idconexion
                gestor = (obj.gestor or "").lower()

                index = self.cb_gestor.findText(gestor)
                if index >= 0:
                    self.cb_gestor.setCurrentIndex(index)

                self.txt_host.setText(obj.host or "")
                self.txt_puerto.setText("" if obj.puerto is None else str(obj.puerto))
                self.txt_user.setText(obj.usuario or "")
                self.txt_pass.setText(obj.contrasenia or "")
                self.txt_db.setText(obj.basedatos or "")
                self.txt_tabla.setText(obj.tabla or "")
                self.actualizar_placeholders()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el registro:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AdministradorConexiones()
    win.show()
    sys.exit(app.exec())