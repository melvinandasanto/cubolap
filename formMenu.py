import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QFrame, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from SesionGlobal import SesionUsuario


# Clase para el menú principal del sistema OLAP
class MenuPrincipalOLAP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sesion = SesionUsuario()
        
        self.setWindowTitle("Sistema OLAP - Panel de Control")
        self.resize(500, 700)
        
        # Estilo general del menú
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
            QWidget {
                font-family: 'Segoe UI';
                color: white;
            }
            QFrame#ContenedorPrincipal {
                background-color: #1b263b;
                border-radius: 15px;
                border: 1px solid #3d85c6;
            }
            QLabel#TituloMenu {
                font-size: 22px;
                font-weight: bold;
                color: #3d85c6;
                margin-bottom: 10px;
            }
            QLabel#UsuarioInfo {
                font-size: 13px;
                color: #a0aeba;
                margin-bottom: 20px;
            }
            /* Estilo para los botones del menú */
            QPushButton {
                background-color: #415a77;
                border: 1px solid #3d85c6;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3d85c6;
                border: 1px solid #e0e1dd;
            }
            QPushButton#BtnCerrarSesion {
                background-color: #e67e22;
                border: none;
                text-align: center;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            QPushButton#BtnCerrarSesion:hover {
                background-color: #f39c12;
            }
            QPushButton#BtnCerrarSistema {
                background-color: #c63d3d;
                border: none;
                text-align: center;
            }
            QPushButton#BtnCerrarSistema:hover {
                background-color: #e63946;
            }
        """)

        self.init_ui()

    def init_ui(self):
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Marco contenedor para el diseño
        self.frame_menu = QFrame()
        self.frame_menu.setObjectName("ContenedorPrincipal")
        layout_menu = QVBoxLayout(self.frame_menu)
        layout_menu.setContentsMargins(30, 30, 30, 30)

        # Título
        lbl_titulo = QLabel("MENÚ PRINCIPAL")
        lbl_titulo.setObjectName("TituloMenu")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_menu.addWidget(lbl_titulo)

        # Información del usuario
        lbl_usuario = QLabel(f"Bienvenido: {self.sesion.nombre_usuario} ({self.sesion.nombre_rol})")
        lbl_usuario.setObjectName("UsuarioInfo")
        lbl_usuario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_menu.addWidget(lbl_usuario)

        # --- BOTONES DEL MENÚ ---
        
        # 1. Cargar un archivo
        self.btn_cargar = QPushButton("📁  Cargar un archivo")
        self.btn_cargar.clicked.connect(self.abrir_formrutas)
        layout_menu.addWidget(self.btn_cargar)

        # 2. Añadir nueva conexión
        self.btn_conexion = QPushButton("🌐  Añadir una nueva conexión")
        self.btn_conexion.clicked.connect(self.abrir_formconexiones)
        layout_menu.addWidget(self.btn_conexion)

        # 3. Añadir usuarios
        self.btn_usuarios = QPushButton("👥  Añadir usuarios")
        self.btn_usuarios.clicked.connect(self.abrir_formusuarios)
        layout_menu.addWidget(self.btn_usuarios)

        # 4. Añadir roles
        self.btn_rol = QPushButton("🏷️  Añadir roles")
        self.btn_rol.clicked.connect(self.abrir_formrol)
        layout_menu.addWidget(self.btn_rol)

        # 4. Creación de cubo
        self.btn_cubo = QPushButton("🧊  Creación de cubo")
        self.btn_cubo.clicked.connect(self.abrir_formdatosparacubo)
        layout_menu.addWidget(self.btn_cubo)

        # Espacio flexible
        layout_menu.addStretch()

        # Botón de Cerrar Sesión
        self.btn_cerrar_sesion = QPushButton("Cerrar Sesión")
        self.btn_cerrar_sesion.setObjectName("BtnCerrarSesion")
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        layout_menu.addWidget(self.btn_cerrar_sesion)

        # Botón de Salir del Sistema
        self.btn_salir = QPushButton("Cerrar Sistema")
        self.btn_salir.setObjectName("BtnCerrarSistema")
        self.btn_salir.clicked.connect(self.close)
        layout_menu.addWidget(self.btn_salir)

        main_layout.addWidget(self.frame_menu)

    def abrir_formrutas(self):
        """Abre el formulario de carga de archivos"""
        from formrutas import FormRutas
        self.form_rutas = FormRutas(self)
        self.form_rutas.show()
        self.hide()

    def abrir_formconexiones(self):
        """Abre el formulario de conexiones"""
        from formconexiones import AdministradorConexiones
        self.form_conexiones = AdministradorConexiones(self)
        self.form_conexiones.show()
        self.hide()

    def abrir_formusuarios(self):
        """Abre el formulario de usuarios"""
        if not self.sesion.es_administrador():
            QMessageBox.warning(self, "Acceso Denegado", "Solo administradores pueden acceder a esta sección")
            return
        
        from formusuario import GestionUsuariosApp
        self.form_usuarios = GestionUsuariosApp(self)
        self.form_usuarios.show()
        self.hide()

    def abrir_formdatosparacubo(self):
        """Abre el formulario de selección de datos para cubo"""
        from formdatosparacubo import SeleccionOrigenOLAP
        self.form_cubo = SeleccionOrigenOLAP(self)
        self.form_cubo.show()
        self.hide()

    def abrir_formrol(self):
        """Abre el formulario de carga de archivos"""
        from formrol import FormRol
        self.form_rol = FormRol(self)
        self.form_rol.show()
        self.hide()

    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        self.sesion.cerrar_sesion()
        
        from formlogin import FormLogin
        self.login_window = FormLogin()
        self.login_window.show()
        self.close()

    def volver_al_menu(self):
        """Método para que otros forms vuelvan a este menú"""
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_menu = MenuPrincipalOLAP()
    ventana_menu.show()
    sys.exit(app.exec())