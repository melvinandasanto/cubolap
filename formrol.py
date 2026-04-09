import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QFrame, QLineEdit, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from claserol import Rol


class DialogoAgregarRol(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Rol")
        self.setFixedSize(360, 180)

        self.setStyleSheet("""
            QDialog {
                background-color: #243447;
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #304156;
                border: 1px solid #455a73;
                border-radius: 5px;
                padding: 10px;
                color: white;
            }
            QPushButton {
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton#BtnGuardar {
                background-color: #3d85c6;
                color: white;
            }
            QPushButton#BtnCancelar {
                background-color: #3e5169;
                color: white;
                border: 1px solid #455a73;
            }
        """)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Nombre del rol:"))

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ejemplo: Aseadora")
        layout.addWidget(self.txt_nombre)

        botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("BtnGuardar")
        self.btn_guardar.clicked.connect(self.accept)
        botones.addWidget(self.btn_guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("BtnCancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)

    def obtener_nombre_rol(self):
        return self.txt_nombre.text().strip()


class FormRol(QMainWindow):
    def __init__(self, idusuario=None, nombre_usuario="Usuario sin seleccionar"):
        super().__init__()

        self.idusuario = idusuario
        self.nombre_usuario = nombre_usuario
        self.rol = Rol()
        self.id_rol_seleccionado = None

        self.setWindowTitle("Gestión de Roles")
        self.resize(1000, 620)

        self.iniciar_estilos()
        self.iniciar_gui()

        self.rol.CrearRolesPredeterminados()
        self.cargar_roles_tabla()
        self.limpiar_formulario()

    def iniciar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }

            QMessageBox { background-color: #243447; }
            QMessageBox QLabel { color: white; font-size: 14px; }

            QFrame#PanelLateral {
                background-color: #243447;
                border-radius: 15px;
                border: 1px solid #3a4a5e;
            }

            QLabel#TituloSeccion {
                font-size: 18px;
                font-weight: bold;
                color: #3d85c6;
                margin-bottom: 15px;
            }

            QLineEdit {
                background-color: #304156;
                border: 1px solid #455a73;
                border-radius: 5px;
                padding: 10px;
                color: white;
                margin-bottom: 12px;
            }

            QLineEdit:read-only {
                background-color: #1b263b;
                color: #8ea1b4;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 5px;
                padding: 12px;
            }

            QPushButton#BtnPrincipal {
                background-color: #3d85c6;
                color: white;
            }

            QPushButton#BtnAccion {
                background-color: #3e5169;
                color: white;
                border: 1px solid #455a73;
            }

            QPushButton#BtnEliminar {
                background-color: #c63d3d;
                color: white;
            }

            QTableWidget {
                background-color: #0d1b2a;
                border: none;
                gridline-color: #243447;
                selection-background-color: #3d85c6;
                color: white;
            }

            QHeaderView::section {
                background-color: #1b263b;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #3d85c6;
            }
        """)

    def iniciar_gui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)

        left_layout = QVBoxLayout()

        lbl_lista = QLabel("Listado de Roles")
        lbl_lista.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(lbl_lista)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre del Rol"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.cargar_datos_al_formulario)
        left_layout.addWidget(self.table)

        main_layout.addLayout(left_layout, stretch=2)

        self.panel = QFrame()
        self.panel.setObjectName("PanelLateral")
        self.panel.setFixedWidth(340)

        form_layout = QVBoxLayout(self.panel)
        form_layout.setContentsMargins(20, 20, 20, 20)

        lbl_tit = QLabel("ASIGNACIÓN DE ROL")
        lbl_tit.setObjectName("TituloSeccion")
        lbl_tit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(lbl_tit)

        form_layout.addWidget(QLabel("Usuario seleccionado:"))
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setReadOnly(True)
        self.txt_usuario.setText(self.nombre_usuario)
        form_layout.addWidget(self.txt_usuario)

        form_layout.addWidget(QLabel("ID del rol:"))
        self.txt_idrol = QLineEdit()
        self.txt_idrol.setReadOnly(True)
        form_layout.addWidget(self.txt_idrol)

        form_layout.addWidget(QLabel("Nombre del rol:"))
        self.txt_nombre = QLineEdit()
        form_layout.addWidget(self.txt_nombre)

        form_layout.addSpacing(15)

        self.btn_agregar = QPushButton("Agregar Rol")
        self.btn_agregar.setObjectName("BtnPrincipal")
        self.btn_agregar.clicked.connect(self.abrir_dialogo_agregar_rol)
        form_layout.addWidget(self.btn_agregar)

        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("BtnAccion")
        self.btn_editar.clicked.connect(self.editar_rol)
        form_layout.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_rol)
        form_layout.addWidget(self.btn_eliminar)

        self.btn_asignar = QPushButton("Asignar al Usuario")
        self.btn_asignar.setObjectName("BtnPrincipal")
        self.btn_asignar.clicked.connect(self.asignar_rol_usuario)
        form_layout.addWidget(self.btn_asignar)

        self.btn_nuevo = QPushButton("Nuevo Registro")
        self.btn_nuevo.setObjectName("BtnAccion")
        self.btn_nuevo.clicked.connect(self.limpiar_formulario)
        form_layout.addWidget(self.btn_nuevo)

        form_layout.addStretch()
        main_layout.addWidget(self.panel)

    def abrir_dialogo_agregar_rol(self):
        dialogo = DialogoAgregarRol(self)

        if dialogo.exec():
            nombre = dialogo.obtener_nombre_rol()

            if not nombre:
                QMessageBox.warning(self, "Validación", "Debe ingresar el nombre del rol.")
                return

            rol = Rol(nombrerol=nombre)
            resultado = rol.Guardar()

            if resultado:
                QMessageBox.information(self, "Éxito", "Rol guardado correctamente.")
                self.cargar_roles_tabla()
                self.limpiar_formulario()
            else:
                detalle = rol.ultimo_error if rol.ultimo_error else "Error desconocido."
                QMessageBox.critical(self, "Error", f"No se pudo guardar el rol.\n\nDetalle:\n{detalle}")

    def cargar_roles_tabla(self):
        self.table.setRowCount(0)
        lista = self.rol.Listar()

        if lista:
            for fila_num, fila in enumerate(lista):
                self.table.insertRow(fila_num)

                item_id = QTableWidgetItem(str(fila[0]))
                item_nombre = QTableWidgetItem(str(fila[1]))

                item_id.setForeground(Qt.GlobalColor.white)
                item_nombre.setForeground(Qt.GlobalColor.white)

                self.table.setItem(fila_num, 0, item_id)
                self.table.setItem(fila_num, 1, item_nombre)

    def cargar_datos_al_formulario(self, item):
        fila = item.row()
        self.txt_idrol.setText(self.table.item(fila, 0).text())
        self.txt_nombre.setText(self.table.item(fila, 1).text())
        self.id_rol_seleccionado = int(self.table.item(fila, 0).text())

    def limpiar_formulario(self):
        self.txt_idrol.clear()
        self.txt_nombre.clear()
        self.id_rol_seleccionado = None
        self.table.clearSelection()

    def editar_rol(self):
        if not self.txt_idrol.text().strip().isdigit():
            QMessageBox.warning(self, "Error", "Seleccione un rol válido.")
            return

        nombre = self.txt_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "Debe ingresar el nombre del rol.")
            return

        rol = Rol(idrol=int(self.txt_idrol.text()), nombrerol=nombre)
        resultado = rol.Editar()

        if resultado:
            QMessageBox.information(self, "Éxito", "Rol editado correctamente.")
            self.cargar_roles_tabla()
            self.limpiar_formulario()
        else:
            detalle = rol.ultimo_error if rol.ultimo_error else "Error desconocido."
            QMessageBox.critical(self, "Error", f"No se pudo editar el rol.\n\nDetalle:\n{detalle}")

    def eliminar_rol(self):
        if not self.txt_idrol.text().strip().isdigit():
            QMessageBox.warning(self, "Error", "Seleccione un rol válido.")
            return

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Desea eliminar este rol?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            rol = Rol()
            resultado = rol.Eliminar(int(self.txt_idrol.text()))

            if resultado:
                QMessageBox.information(self, "Éxito", "Rol eliminado correctamente.")
                self.cargar_roles_tabla()
                self.limpiar_formulario()
            else:
                detalle = rol.ultimo_error if rol.ultimo_error else "Error desconocido."
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el rol.\n\nDetalle:\n{detalle}")

    def asignar_rol_usuario(self):
        if self.idusuario is None:
            QMessageBox.warning(self, "Error", "No hay un usuario seleccionado para asignar.")
            return

        if not self.txt_idrol.text().strip().isdigit():
            QMessageBox.warning(self, "Error", "Seleccione un rol para asignar.")
            return

        rol = Rol()
        resultado = rol.AsignarRolAUsuario(self.idusuario, int(self.txt_idrol.text()))

        if resultado:
            QMessageBox.information(
                self,
                "Éxito",
                f"Rol asignado correctamente a {self.nombre_usuario}."
            )
        else:
            detalle = rol.ultimo_error if rol.ultimo_error else "Error desconocido."
            QMessageBox.critical(self, "Error", f"No se pudo asignar el rol.\n\nDetalle:\n{detalle}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormRol(None, "Usuario sin seleccionar")
    ventana.show()
    sys.exit(app.exec())