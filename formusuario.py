import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QFrame, QLineEdit, QMessageBox, QComboBox,
    QScrollArea
)
from PyQt6.QtCore import Qt

from formrol import FormRol
from claseusuario import Usuario
from claseLogin import Autenticacion
from claserol import ClaseRol
from SesionGlobal import SesionUsuario

class GestionUsuariosApp(QMainWindow):
    def __init__(self, parent_menu=None, es_primera_inicializacion=False):
        super().__init__()
        self.parent_menu = parent_menu
        self.es_primera_inicializacion = es_primera_inicializacion

        self.setWindowTitle("Sistema OLAP - Control de Accesos")
        self.resize(1100, 650)
        
        # Verificar permisos (solo si NO es primera inicialización)
        if not es_primera_inicializacion:
            sesion = SesionUsuario()
            if not sesion.es_administrador():
                QMessageBox.critical(
                    self,
                    "Acceso Denegado",
                    "Solo los administradores pueden acceder a la gestión de usuarios."
                )
                self.close()
                return
        
        # Variable para controlar el ID (puedes obtener el último de tu BD)
        self.proximo_id = 1 
        
        # Diccionario para mapear nombres de rol a IDs
        self.rol_map = {}
        
        # Instancia de tu clase de conexión/lógica
        # self.logica = ClaseUsuarios()

        self.iniciar_estilos()
        self.iniciar_gui()
        self.cargar_roles_desde_bd()

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

            QPushButton {
                min-height: 44px;
                padding: 6px 10px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                color: white;
            }

            QPushButton#BtnPrincipal {
                background-color: #3d85c6;
            }

            QPushButton#BtnAccion {
                background-color: #3e5169;
                border: 1px solid #455a73;
            }

            QPushButton#BtnEliminar {
                background-color: #c63d3d;
            }

            QPushButton#BtnVolver {
                background-color: #5c6b88;
                border: 1px solid #4a5a74;
            }

            QPushButton:hover {
                background-color: #5589c9;
            }

            QPushButton:pressed {
                background-color: #2e5e9b;
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
        self.panel.setMinimumWidth(360)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(self.panel)

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
        main_layout.addWidget(scroll_area, stretch=1)

    def cargar_roles_desde_bd(self):
        """Carga los roles desde la tabla rol de la BD y llena el ComboBox"""
        try:
            clase_rol = ClaseRol()
            roles = clase_rol.Listar()
            
            if roles:
                # Limpiar ComboBox
                self.cb_rol.clear()
                
                # Agregar roles y crear mapeo
                for idrol, nombrerol in roles:
                    self.cb_rol.addItem(nombrerol)
                    self.rol_map[nombrerol] = idrol
            else:
                QMessageBox.warning(self, "Aviso", "No hay roles disponibles en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar roles: {str(e)}")
        
        # Cargar usuarios después de cargar roles
        self.cargar_usuarios_desde_bd()

    def cargar_usuarios_desde_bd(self):
        """Carga los usuarios desde la BD y muestra en la tabla. Respeta permisos."""
        try:
            sesion = SesionUsuario()
            es_admin = sesion.es_administrador()
            
            usuario_obj = Usuario()
            usuarios = usuario_obj.Listar()
            
            self.table.setRowCount(0)
            
            if usuarios:
                for idusuario, nombre, idrol, nombrerol, activo in usuarios:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    
                    # ID
                    self.table.setItem(row, 0, QTableWidgetItem(str(idusuario)))
                    
                    # Nombre
                    self.table.setItem(row, 1, QTableWidgetItem(nombre))
                    
                    # Rol
                    self.table.setItem(row, 2, QTableWidgetItem(nombrerol or "Sin Rol"))
                    
                    # Estado
                    estado_texto = "Activo" if activo else "Inactivo"
                    self.table.setItem(row, 3, QTableWidgetItem(estado_texto))
                    
                    # Contraseña - solo admin puede ver
                    if es_admin:
                        self.table.setItem(row, 4, QTableWidgetItem("*" * 5))
                    else:
                        self.table.setItem(row, 4, QTableWidgetItem("***"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar usuarios: {str(e)}")

    def nuevo_registro(self):
        self.txt_id.clear()
        self.txt_nombre.clear()
        self.txt_pass.clear()
        self.txt_pass.setPlaceholderText("")
        self.cb_rol.setCurrentIndex(0)
        self.cb_estado.setCurrentIndex(0)
        self.table.clearSelection()

    def cargar_datos_al_formulario(self, item):
        row = item.row()
        self.txt_id.setText(self.table.item(row, 0).text())
        self.txt_nombre.setText(self.table.item(row, 1).text())
        self.cb_rol.setCurrentText(self.table.item(row, 2).text())
        self.cb_estado.setCurrentText(self.table.item(row, 3).text())
        self.txt_pass.setPlaceholderText("Dejar vacío para no cambiar")

    def validar_campos(self):
        nombre = self.txt_nombre.text().strip()
        contrasenia = self.txt_pass.text().strip()
        es_edicion = self.txt_id.text().strip() != ""

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre de usuario es obligatorio.")
            self.txt_nombre.setFocus()
            return False

        if not es_edicion and not contrasenia:
            QMessageBox.warning(self, "Validación", "La contraseña es obligatoria.")
            self.txt_pass.setFocus()
            return False

        return True

    # --- Métodos para conectar con tu Clase ---
    def guardar_usuario(self):
        """Guarda un nuevo usuario en la base de datos"""
        nombre = self.txt_nombre.text().strip()
        contrasenia = self.txt_pass.text().strip()
        rol_texto = self.cb_rol.currentText()
        activo = 1 if self.cb_estado.currentText() == "Activo" else 0
        
        # Validar campos
        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre de usuario es obligatorio.")
            self.txt_nombre.setFocus()
            return
        
        if not contrasenia:
            QMessageBox.warning(self, "Validación", "La contraseña es obligatoria.")
            self.txt_pass.setFocus()
            return
        
        try:
            # Obtener el nombre del rol seleccionado
            rol_texto = self.cb_rol.currentText()
            
            # Buscar el ID del rol en el diccionario
            idrol = self.rol_map.get(rol_texto, 1)
            
            # Crear instancia de Usuario y guardar
            nuevo_usuario = Usuario(
                nombre=nombre,
                contrasenia=contrasenia,
                idrol=idrol,
                activo=activo
            )
            
            if nuevo_usuario.Guardar():
                QMessageBox.information(self, "Éxito", f"Usuario '{nombre}' guardado correctamente.")
                
                # SOLO mostrar mensaje de primera inicialización si estamos en modo inicial
                if self.es_primera_inicializacion:
                    # Verificar si el usuario creado es admin y si solo existía default
                    auth = Autenticacion(
                        gestor="sqlserver",
                        host="localhost",
                        database="cubolap"
                    )
                    
                    # Si ya no solo existe default, abrir el menú principal
                    if not auth.solo_existe_default():
                        QMessageBox.information(
                            self,
                            "Primer Usuario Creado",
                            "El usuario default ha sido desactivado automáticamente.\n\nBienvenido al sistema."
                        )
                        self.abrir_menu_principal()
                    else:
                        # Recargar tabla y limpiar formulario
                        self.cargar_usuarios_desde_bd()
                        self.nuevo_registro()
                else:
                    # Modo normal: solo recargar tabla
                    self.cargar_usuarios_desde_bd()
                    self.nuevo_registro()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar el usuario en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar usuario: {str(e)}")

    def abrir_menu_principal(self):
        """Abre el menú principal del sistema"""
        try:
            from formMenu import MenuPrincipalOLAP
            self.menu = MenuPrincipalOLAP()
            self.menu.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el menú: {str(e)}")

    def editar_usuario(self):
        """Actualiza un usuario en la base de datos"""
        selected = self.table.currentRow()
        
        if selected < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un usuario de la lista para editar.")
            return
        
        try:
            # Obtener ID del usuario seleccionado
            idusuario = int(self.txt_id.text())
            nombre = self.txt_nombre.text().strip()
            contrasenia = self.txt_pass.text().strip()
            rol_texto = self.cb_rol.currentText()
            activo = 1 if self.cb_estado.currentText() == "Activo" else 0
            
            # Validar campos
            if not nombre:
                QMessageBox.warning(self, "Validación", "El nombre de usuario es obligatorio.")
                self.txt_nombre.setFocus()
                return
            
            # Debug: mostrar datos
            print(f"DEBUG - ID: {idusuario}, Nombre: {nombre}, Rol: {rol_texto}, Activo: {activo}, Contraseña vacía: {not contrasenia}")
            
            # Crear instancia de Usuario y buscarlo para obtener datos actuales
            usuario = Usuario()
            
            # Buscar usuario actual para obtener la contraseña (si no se está cambiando)
            if usuario.Buscar(idusuario):
                print(f"DEBUG - Usuario encontrado: {usuario.nombre}")
                
                # Si no se ingresó contraseña nueva, mantener la actual
                if not contrasenia:
                    contrasenia = usuario.contrasenia
                    print(f"DEBUG - Usando contraseña actual")
                
                # Actualizar datos
                usuario.nombre = nombre
                usuario.contrasenia = contrasenia
                
                # Obtener ID del rol
                idrol = self.rol_map.get(rol_texto, 1)
                usuario.idrol = idrol
                usuario.activo = activo
                
                print(f"DEBUG - Datos a actualizar: Nombre={usuario.nombre}, Rol={idrol}, Activo={usuario.activo}")
                
                # Guardar cambios en la BD
                resultado = usuario.Editar()
                print(f"DEBUG - Resultado de Editar(): {resultado}")
                
                if resultado:
                    QMessageBox.information(self, "Éxito", f"Usuario '{nombre}' actualizado correctamente.")
                    # Recargar tabla y limpiar formulario
                    self.cargar_usuarios_desde_bd()
                    self.nuevo_registro()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo actualizar el usuario en la base de datos.")
            else:
                print(f"DEBUG - Usuario NO encontrado con ID: {idusuario}")
                QMessageBox.critical(self, "Error", "No se encontró el usuario en la base de datos.")
                
        except ValueError:
            QMessageBox.critical(self, "Error", "ID de usuario inválido.")
        except Exception as e:
            print(f"DEBUG - Excepción: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")

    def eliminar_usuario(self):
        """Elimina un usuario de la base de datos"""
        selected = self.table.currentRow()
        
        if selected < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un usuario de la lista para eliminar.")
            return
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al usuario '{self.txt_nombre.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta != QMessageBox.StandardButton.Yes:
            return
        
        try:
            idusuario = int(self.txt_id.text())
            
            # Eliminar usuario de la BD
            usuario = Usuario()
            if usuario.Eliminar(idusuario):
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                # Recargar tabla y limpiar formulario
                self.cargar_usuarios_desde_bd()
                self.nuevo_registro()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el usuario de la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {str(e)}")

    def focusInEvent(self, event):
        """Recarga la tabla de usuarios cuando la ventana gana el foco"""
        self.cargar_usuarios_desde_bd()
        super().focusInEvent(event)

    def volver_al_menu(self):
        """Vuelve al menú principal"""
        if self.parent_menu:
            self.parent_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestionUsuariosApp()
    ventana.show()
    sys.exit(app.exec())