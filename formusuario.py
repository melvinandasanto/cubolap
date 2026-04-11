import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QFrame, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt

# Aquí deberías importar tu clase de lógica, por ejemplo:
# from datos.clase_usuarios import ClaseUsuarios

class GestionUsuariosApp(QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu

        self.setWindowTitle("Sistema OLAP - Control de Accesos")
        self.resize(1100, 650)
        
        # Variable para controlar el ID (puedes obtener el último de tu BD)
        self.proximo_id = 1 
        
        # Instancia de tu clase de conexión/lógica
        # self.logica = ClaseUsuarios()

        self.iniciar_estilos()
        self.iniciar_gui()

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
            
            QLabel#TituloSeccion { font-size: 18px; font-weight: bold; color: #3d85c6; margin-bottom: 15px; }
            
            QLineEdit { 
                background-color: #304156; border: 1px solid #455a73; 
                border-radius: 5px; padding: 10px; color: white; margin-bottom: 12px;
            }
            QLineEdit:read-only { background-color: #1b263b; color: #8ea1b4; }
            
            QComboBox { 
                background-color: #304156; border: 1px solid #455a73; 
                border-radius: 5px; padding: 8px; margin-bottom: 12px; color: white;
            }

            QPushButton#BtnPrincipal {
                background-color: #3d85c6; color: white;
            }

            QPushButton#BtnAccion {
                background-color: #3e5169; color: white; border: 1px solid #455a73;
            }

            QPushButton#BtnEliminar {
                background-color: #c63d3d; color: white;
            }

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

        # --- TABLA (IZQUIERDA) ---
        left_layout = QVBoxLayout()
        lbl_lista = QLabel("Listado de Usuarios")
        lbl_lista.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(lbl_lista)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre Usuario", "Rol", "Estado", "Contraseña"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemClicked.connect(self.cargar_datos_al_formulario)
        
        left_layout.addWidget(self.table)
        main_layout.addLayout(left_layout, stretch=2)

        # --- FORMULARIO (DERECHA) ---
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
        self.cb_rol.addItems(["Admin", "Analista", "Visualizadora"])
        form_layout.addWidget(self.cb_rol)

        form_layout.addWidget(QLabel("Contraseña:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.txt_pass)

        form_layout.addWidget(QLabel("Estado de Cuenta:"))
        self.cb_estado = QComboBox()
        self.cb_estado.addItems(["Activo", "Inactivo"])
        self.cb_estado.setStyleSheet("color: #81c784; font-weight: bold; background-color: #304156;") 
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

        self.btn_limpiar = QPushButton("Nuevo Registro")
        self.btn_limpiar.setObjectName("BtnAccion")
        self.btn_limpiar.clicked.connect(self.nuevo_registro)
        form_layout.addWidget(self.btn_limpiar)

        self.btn_volver = QPushButton("Volver al Menú")
        self.btn_volver.setObjectName("BtnVolver")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        form_layout.addWidget(self.btn_volver)

        form_layout.addStretch()
        main_layout.addWidget(self.panel)

    def validar_campos(self):
        nombre = self.txt_nombre.text().strip()
        contrasenia = self.txt_contrasenia.text().strip()
        es_edicion = self.txt_id.text().strip() != ""

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre de usuario es obligatorio.")
            self.txt_nombre.setFocus()
            return False

        if not es_edicion and not contrasenia:
            QMessageBox.warning(self, "Validación", "La contraseña es obligatoria.")
            self.txt_contrasenia.setFocus()
            return False

        return True

    def cargar_estados(self):
        self.estado_actual = 1

    def obtener_usuario_desde_formulario(self):
        texto_id = self.txt_id.text().strip()

        self.usuario.IdUsuario = int(texto_id) if texto_id.isdigit() else None
        self.usuario.Nombre = self.txt_nombre.text().strip()

        contrasenia = self.txt_contrasenia.text().strip()
        self.usuario.Contrasenia = contrasenia if contrasenia else None
        self.usuario.Activo = self.estado_actual

    def limpiar_formulario(self):
        self.txt_id.clear()
        self.txt_nombre.clear()
        self.txt_rol.clear()
        self.txt_contrasenia.clear()
        self.txt_contrasenia.setPlaceholderText("")
        self.txt_estado.setText("Activo")
        self.estado_actual = 1
        self.table.clearSelection()

    def cambiar_estado(self):
        if self.estado_actual == 1:
            self.estado_actual = 0
            self.txt_estado.setText("Inactivo")
        else:
            self.estado_actual = 1
            self.txt_estado.setText("Activo")

    def cargar_datos_al_formulario(self, item):
        row = item.row()
        self.txt_id.setText(self.table.item(row, 0).text())
        self.txt_nombre.setText(self.table.item(row, 1).text())
        self.cb_rol.setCurrentText(self.table.item(row, 2).text())
        self.cb_estado.setCurrentText(self.table.item(row, 3).text())
        self.txt_pass.setPlaceholderText("Dejar vacío para no cambiar")

    def nuevo_registro(self):
        self.txt_id.setText(str(self.proximo_id))
        self.txt_nombre.clear()
        self.txt_pass.clear()
        self.txt_pass.setPlaceholderText("")
        self.cb_rol.setCurrentIndex(0)
        self.cb_estado.setCurrentIndex(0)
        self.table.clearSelection()

    # --- Métodos para conectar con tu Clase ---
    def guardar_usuario(self):
        if not self.txt_nombre.text():
            self.mostrar_mensaje("Error", "El nombre es obligatorio.", QMessageBox.Icon.Warning)
            return
        
        # 1. Llamar a tu clase: self.logica.insertar(self.txt_nombre.text(), ...)
        # 2. Refrescar tabla o agregar localmente:
        self.agregar_fila_tabla(self.txt_id.text(), self.txt_nombre.text(), 
                               self.cb_rol.currentText(), self.cb_estado.currentText())
        
        self.proximo_id += 1
        self.mostrar_mensaje("Éxito", "Usuario guardado en el sistema.")
        self.nuevo_registro()

    def editar_usuario(self):
        selected = self.table.currentRow()
        if selected >= 0:
            # 1. Llamar a tu clase: self.logica.actualizar(self.txt_id.text(), ...)
            # 2. Actualizar tabla visual:
            self.table.setItem(selected, 1, QTableWidgetItem(self.txt_nombre.text()))
            self.table.setItem(selected, 2, QTableWidgetItem(self.cb_rol.currentText()))
            self.table.setItem(selected, 3, QTableWidgetItem(self.cb_estado.currentText()))
            self.mostrar_mensaje("Sistema", "Usuario actualizado correctamente.")
        else:
            self.mostrar_mensaje("Aviso", "Seleccione un usuario de la lista.", QMessageBox.Icon.Warning)

    def eliminar_usuario(self):
        selected = self.table.currentRow()
        if selected >= 0:
            # 1. Llamar a tu clase: self.logica.eliminar(self.txt_id.text())
            # 2. Quitar de la tabla visual:
            self.table.removeRow(selected)
            self.nuevo_registro()
            self.mostrar_mensaje("Sistema", "Usuario eliminado.")
        else:
            idusuario = None
            nombre_usuario = "Usuario sin seleccionar"

        self.ventana_roles = FormRol(idusuario, nombre_usuario)
        self.ventana_roles.show()

    def focusInEvent(self, event):
        self.cargar_usuarios_tabla()
        super().focusInEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestionUsuariosApp()
    ventana.show()
    sys.exit(app.exec())