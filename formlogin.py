import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLineEdit, QPushButton, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from claseLogin import Autenticacion
from SesionGlobal import SesionUsuario


# Clase para el formulario de login
class FormLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Análisis OLAP")
        self.setGeometry(100, 100, 500, 500)
        
        self.bg_color = "#0d1b2a"
        self.card_color = "#1b263b"
        self.entry_bg = "#2a3b4d"
        self.btn_color = "#3d85c6"
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.bg_color};
            }}
            QLineEdit {{
                background-color: {self.entry_bg};
                color: white;
                border: 1px solid #3d85c6;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {self.btn_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #3374ad;
            }}
        """)
        self.init_ui()
        
    # Inicializa la interfaz de usuario
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Contenedor principal
        container = QFrame()
        container.setStyleSheet(f"background-color: {self.card_color}; border-radius: 10px;")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("SISTEMA DE ANÁLISIS OLAP")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        # Espaciador
        container_layout.addSpacing(10)
        
        # Usuario
        lbl_usuario = QLabel("Usuario")
        lbl_usuario.setStyleSheet("color: white; font-size: 11px;")
        container_layout.addWidget(lbl_usuario)
        self.user_entry = QLineEdit()
        container_layout.addWidget(self.user_entry)
        
        # Contraseña
        lbl_pass = QLabel("Contraseña")
        lbl_pass.setStyleSheet("color: white; font-size: 11px;")
        container_layout.addWidget(lbl_pass)
        self.pass_entry = QLineEdit()
        self.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)
        container_layout.addWidget(self.pass_entry)
        
        # Espaciador
        container_layout.addSpacing(20)
        
        # Botón Iniciar Sesión
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #3d85c6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3374ad;
            }
        """)
        self.btn_login.clicked.connect(self.iniciar_sesion)
        container_layout.addWidget(self.btn_login)
        
        layout.addWidget(container)
        layout.addStretch()
    
    # Inicia la sesión del usuario
    def iniciar_sesion(self):
        usuario = self.user_entry.text()
        contrasena = self.pass_entry.text()
        
        if not usuario or not contrasena:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese usuario y contraseña")
            return
        
        auth = Autenticacion(
            gestor="sqlserver",
            host="localhost",
            database="cubolap"
        )

        resultado_login = auth.login(usuario, contrasena)
        
        if resultado_login:
            # Login exitoso - registrar en sesión global
            sesion = SesionUsuario()
            sesion.iniciar_sesion(
                id_usuario=resultado_login['id'],
                nombre_usuario=resultado_login['nombre'],
                id_rol=resultado_login['id_rol'],
                nombre_rol=resultado_login['nombre_rol'],
                activo=resultado_login.get('activo', True)
            )
            
            QMessageBox.information(self, "Éxito", "Inicio de sesión correcto ✅")
            
            # Verificar si es el usuario default
            if usuario == "default":
                # Si solo existe default, abrir formulario de usuarios
                if auth.solo_existe_default():
                    self.abrir_gestion_usuarios()
                else:
                    # Si hay otros usuarios, ir al menú
                    self.abrir_menu_principal()
            else:
                # Si es otro usuario, abrir menú
                self.abrir_menu_principal()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos ❌")
    
    def abrir_menu_principal(self):
        """Abre el menú principal del sistema"""
        try:
            from formMenu import MenuPrincipalOLAP
            self.menu = MenuPrincipalOLAP()
            self.menu.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el menú: {str(e)}")
    
    def abrir_gestion_usuarios(self):
        """Abre el formulario de gestión de usuarios para crear el primer usuario"""
        try:
            from formusuario import GestionUsuariosApp
            self.gestion_usuarios = GestionUsuariosApp(parent_menu=None, es_primera_inicializacion=True)
            self.gestion_usuarios.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir gestión de usuarios: {str(e)}")

