import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QHeaderView, QFrame, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from claseusuario import Usuario
from claseconectar import Conectar


class GestionUsuariosApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema OLAP - Control de Accesos")
        self.resize(1100, 650)

        self.usuario = Usuario()

        self.iniciar_estilos()
        self.iniciar_gui()

        self.cargar_roles()
        self.cargar_estados()
        self.cargar_usuarios_tabla()
        self.limpiar_formulario()

    def iniciar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1a2634; }
            QWidget { color: white; font-family: 'Segoe UI'; }

            QMessageBox { background-color: #243447; }
            QMessageBox QLabel { color: white; font-size: 14px; }
            QMessageBox QPushButton {
                background-color: #3d85c6; color: white;
                border-radius: 4px; padding: 5px 15px;
            }

            QFrame#PanelLateral {
                background-color: #243447; border-radius: 15px; border: 1px solid #3a4a5e;
            }

            QLabel#TituloSeccion {
                font-size: 18px; font-weight: bold; color: #3d85c6; margin-bottom: 15px;
            }

            QLineEdit {
                background-color: #304156; border: 1px solid #455a73;
                border-radius: 5px; padding: 10px; color: white; margin-bottom: 12px;
            }
            QLineEdit:read-only { background-color: #1b263b; color: #8ea1b4; }

            QComboBox {
                background-color: #304156; border: 1px solid #455a73;
                border-radius: 5px; padding: 8px; margin-bottom: 12px; color: white;
            }

            QPushButton { font-weight: bold; border-radius: 5px; padding: 12px; }
            QPushButton#BtnPrincipal { background-color: #3d85c6; color: white; }
            QPushButton#BtnAccion { background-color: #3e5169; color: white; border: 1px solid #455a73; }
            QPushButton#BtnEliminar { background-color: #c63d3d; color: white; }

            QTableWidget {
                background-color: #0d1b2a; border: none; gridline-color: #243447;
                selection-background-color: #3d85c6; color: white;
            }
            QHeaderView::section {
                background-color: #1b263b; padding: 12px; border: none; font-weight: bold; color: #3d85c6;
            }
        """)

    def iniciar_gui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # -------- TABLA --------
        left_layout = QVBoxLayout()

        lbl_lista = QLabel("Listado de Usuarios")
        lbl_lista.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(lbl_lista)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre Usuario", "Rol", "Estado", "Contraseña"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.cargar_datos_al_formulario)

        left_layout.addWidget(self.table)
        main_layout.addLayout(left_layout, stretch=2)

        # -------- PANEL DERECHO --------
        self.panel = QFrame()
        self.panel.setObjectName("PanelLateral")
        self.panel.setFixedWidth(320)

        form_layout = QVBoxLayout(self.panel)
        form_layout.setContentsMargins(20, 20, 20, 20)

        lbl_tit = QLabel("GESTIÓN DE PERFIL")
        lbl_tit.setObjectName("TituloSeccion")
        lbl_tit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(lbl_tit)

        form_layout.addWidget(QLabel("ID de Usuario (Auto):"))
        self.txt_id = QLineEdit()
        self.txt_id.setReadOnly(True)
        form_layout.addWidget(self.txt_id)

        form_layout.addWidget(QLabel("Nombre de Usuario:"))
        self.txt_nombre = QLineEdit()
        form_layout.addWidget(self.txt_nombre)

        form_layout.addWidget(QLabel("Rol:"))
        self.cb_rol = QComboBox()
        form_layout.addWidget(self.cb_rol)

        form_layout.addWidget(QLabel("Contraseña:"))
        self.txt_contrasenia = QLineEdit()
        self.txt_contrasenia.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.txt_contrasenia)

        form_layout.addWidget(QLabel("Estado de Cuenta:"))
        self.cb_estado = QComboBox()
        self.cb_estado.setStyleSheet(
            "color: #81c784; font-weight: bold; background-color: #304156;"
        )
        form_layout.addWidget(self.cb_estado)

        form_layout.addSpacing(15)

        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_guardar.setObjectName("BtnPrincipal")
        self.btn_guardar.clicked.connect(self.guardar_usuario)
        form_layout.addWidget(self.btn_guardar)

        self.btn_editar = QPushButton("Actualizar")
        self.btn_editar.setObjectName("BtnAccion")
        self.btn_editar.clicked.connect(self.editar_usuario)
        form_layout.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        form_layout.addWidget(self.btn_eliminar)

        self.btn_limpiar = QPushButton("Limpiar Formulario")
        self.btn_limpiar.setObjectName("BtnAccion")
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        form_layout.addWidget(self.btn_limpiar)

        form_layout.addStretch()
        main_layout.addWidget(self.panel)

    def mostrar_mensaje(self, titulo, texto, icono=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.setIcon(icono)
        msg.exec()

    def validar_campos(self):
        nombre = self.txt_nombre.text().strip()
        contrasenia = self.txt_contrasenia.text().strip()
        es_edicion = self.txt_id.text().strip() != ""
        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre de usuario es obligatorio.")
            self.txt_nombre.setFocus()
            return False
        # En nuevo registro, contraseña obligatoria
        if not es_edicion and not contrasenia:
            QMessageBox.warning(self, "Validación", "La contraseña es obligatoria.")
            self.txt_contrasenia.setFocus()
            return False

        # En edición, puede quedar vacía para no cambiarla
        return True

    def cargar_roles(self):
        try:
            self.cb_rol.clear()
            lista_roles = self.usuario.ListarRoles()

            if lista_roles:
                for fila in lista_roles:
                    idrol = fila[0]
                    nombrerol = fila[1]
                    self.cb_rol.addItem(nombrerol, idrol)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los roles:\n{str(e)}")

    def cargar_estados(self):
        self.cb_estado.clear()
        self.cb_estado.addItem("Activo", 1)
        self.cb_estado.addItem("Inactivo", 0)

    def obtener_usuario_desde_formulario(self):
        texto_id = self.txt_id.text().strip()

        self.usuario.IdUsuario = int(texto_id) if texto_id.isdigit() else None
        self.usuario.Nombre = self.txt_nombre.text().strip()

        # Solo asignar contraseña si el usuario escribió algo
        contrasenia = self.txt_contrasenia.text().strip()
        self.usuario.Contrasenia = contrasenia if contrasenia else None

        self.usuario.IdRol = self.cb_rol.currentData()
        self.usuario.Activo = self.cb_estado.currentData()

    def limpiar_formulario(self):
        self.txt_id.clear()
        self.txt_nombre.clear()
        self.txt_contrasenia.clear()
        self.txt_contrasenia.setPlaceholderText("")

        if self.cb_rol.count() > 0:
            self.cb_rol.setCurrentIndex(0)

        if self.cb_estado.count() > 0:
            self.cb_estado.setCurrentIndex(0)

        self.table.clearSelection()

    def cargar_datos_al_formulario(self, item):
        row = item.row()

        self.txt_id.setText(self.table.item(row, 0).text())
        self.txt_nombre.setText(self.table.item(row, 1).text())

        idrol = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)
        activo = self.table.item(row, 3).data(Qt.ItemDataRole.UserRole)

        indice_rol = self.cb_rol.findData(idrol)
        if indice_rol >= 0:
            self.cb_rol.setCurrentIndex(indice_rol)

        indice_estado = self.cb_estado.findData(activo)
        if indice_estado >= 0:
            self.cb_estado.setCurrentIndex(indice_estado)

        self.txt_contrasenia.clear()
        self.txt_contrasenia.setPlaceholderText("Dejar vacío para no cambiar")

    def cargar_usuarios_tabla(self):
        try:
            self.table.setRowCount(0)
            lista = self.usuario.Listar()

            if lista:
                for fila_num, fila in enumerate(lista):
                    self.table.insertRow(fila_num)

                    idusuario = fila[0]
                    nombre = fila[1]
                    idrol = fila[2]
                    nombrerol = fila[3]
                    activo = fila[4]

                    estado_texto = "Activo" if activo else "Inactivo"

                    item_id = QTableWidgetItem(str(idusuario))
                    item_nombre = QTableWidgetItem(nombre)

                    item_rol = QTableWidgetItem(nombrerol)
                    item_rol.setData(Qt.ItemDataRole.UserRole, idrol)

                    item_estado = QTableWidgetItem(estado_texto)
                    item_estado.setData(Qt.ItemDataRole.UserRole, 1 if activo else 0)

                    item_pass = QTableWidgetItem("********")

                    for item_tabla in [item_id, item_nombre, item_rol, item_estado, item_pass]:
                        item_tabla.setForeground(Qt.GlobalColor.white)

                    self.table.setItem(fila_num, 0, item_id)
                    self.table.setItem(fila_num, 1, item_nombre)
                    self.table.setItem(fila_num, 2, item_rol)
                    self.table.setItem(fila_num, 3, item_estado)
                    self.table.setItem(fila_num, 4, item_pass)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla:\n{str(e)}")

    def guardar_usuario(self):
        if not self.validar_campos():
            return

        try:
            self.obtener_usuario_desde_formulario()

            if not self.usuario.Contrasenia:
                QMessageBox.warning(self, "Validación", "La contraseña es obligatoria.")
                self.txt_contrasenia.setFocus()
                return

            resultado = self.usuario.Guardar()

            if resultado:
                QMessageBox.information(self, "Éxito", "Usuario guardado correctamente")
                self.cargar_usuarios_tabla()
                self.limpiar_formulario()
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el usuario")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el usuario:\n{str(e)}")

    def editar_usuario(self):
        if not self.txt_id.text().strip().isdigit():
            QMessageBox.warning(self, "Error", "Seleccione un usuario válido")
            return

        if not self.validar_campos():
            return

        try:
            self.obtener_usuario_desde_formulario()

            # Si no escribió contraseña nueva, conservar la actual de la BD
            if not self.usuario.Contrasenia:
                usuario_aux = Usuario()
                encontrado = usuario_aux.Buscar(int(self.txt_id.text().strip()))
                if encontrado:
                    self.usuario.Contrasenia = usuario_aux.Contrasenia
                else:
                    QMessageBox.warning(self, "Error", "No se encontró el usuario a editar")
                    return

            resultado = self.usuario.Editar()

            if resultado:
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
                self.cargar_usuarios_tabla()
                self.limpiar_formulario()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el usuario")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el usuario:\n{str(e)}")

    def eliminar_usuario(self):
        usuario_id = self.txt_id.text().strip()

        if not usuario_id.isdigit():
            QMessageBox.warning(self, "Error", "Seleccione un usuario válido para eliminar")
            return

        confirmacion = QMessageBox.question(            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el usuario con ID {usuario_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                resultado = self.usuario.Eliminar(int(usuario_id))

                if resultado:
                    QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                    self.cargar_usuarios_tabla()
                    self.limpiar_formulario()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestionUsuariosApp()
    ventana.show()
    sys.exit(app.exec())