import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QFrame, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from claserol import ClaseRol


class FormRol(QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu
        self.setWindowTitle("Sistema de Roles")
        self.resize(1050, 620)

        self.rol = ClaseRol()
        self.id_rol_seleccionado = None

        self.iniciar_estilos()

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout_principal = QHBoxLayout()
        self.layout_principal.setContentsMargins(24, 24, 24, 24)
        self.layout_principal.setSpacing(20)
        self.central.setLayout(self.layout_principal)

        self.crear_interfaz()
        self.cargar_roles()

    def iniciar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a2634;
            }

            QWidget {
                color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QFrame#PanelTabla {
                background-color: #142131;
                border: 1px solid #24384f;
                border-radius: 18px;
            }

            QFrame#PanelLateral {
                background-color: #243447;
                border-radius: 18px;
                border: 1px solid #3a4a5e;
            }

            QLabel#TituloPrincipal {
                font-size: 24px;
                font-weight: 700;
                color: white;
            }

            QLabel#Subtitulo {
                font-size: 13px;
                color: #a8bfd6;
                margin-bottom: 10px;
            }

            QLabel#TituloSeccion {
                font-size: 18px;
                font-weight: bold;
                color: #3d85c6;
                margin-bottom: 10px;
            }

            QLabel#Etiqueta {
                font-size: 13px;
                color: #dce8f5;
                margin-top: 2px;
            }

            QLineEdit {
                background-color: #304156;
                color: white;
                border: 1px solid #455a73;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }

            QPushButton {
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                border: none;
            }

            QPushButton#BtnPrincipal {
                background-color: #3d85c6;
                color: white;
            }

            QPushButton#BtnPrincipal:hover {
                background-color: #3374ad;
            }

            QPushButton#BtnAccion {
                background-color: #3e5169;
                color: white;
                border: 1px solid #455a73;
            }

            QPushButton#BtnAccion:hover {
                background-color: #4a607c;
            }

            QPushButton#BtnEliminar {
                background-color: #c63d3d;
                color: white;
            }

            QPushButton#BtnEliminar:hover {
                background-color: #aa3333;
            }

            QTableWidget {
                background-color: #0d1b2a;
                color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #243447;
                selection-background-color: #3d85c6;
                font-size: 12px;
            }

            QHeaderView::section {
                background-color: #1b263b;
                color: #3d85c6;
                padding: 12px;
                border: none;
                font-weight: bold;
            }

            QMessageBox {
                background-color: #243447;
            }

            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                background-color: #3d85c6;
                color: white;
                border-radius: 5px;
                padding: 6px 14px;
                min-width: 80px;
            }
        """)

    def crear_interfaz(self):
        panel_tabla = QFrame()
        panel_tabla.setObjectName("PanelTabla")
        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(22, 22, 22, 22)
        layout_tabla.setSpacing(12)

        titulo = QLabel("GESTIÓN DE ROLES")
        titulo.setObjectName("TituloPrincipal")
        layout_tabla.addWidget(titulo)

        subtitulo = QLabel("Crea, edita o elimina roles como Aseadora, Supervisor, Cajero o similares.")
        subtitulo.setObjectName("Subtitulo")
        layout_tabla.addWidget(subtitulo)

        lbl_tabla = QLabel("Roles registrados")
        lbl_tabla.setObjectName("Etiqueta")
        layout_tabla.addWidget(lbl_tabla)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre del Rol"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.cellClicked.connect(self.seleccionar_rol)
        layout_tabla.addWidget(self.tabla)

        self.layout_principal.addWidget(panel_tabla, stretch=2)

        panel_lateral = QFrame()
        panel_lateral.setObjectName("PanelLateral")
        panel_lateral.setFixedWidth(340)

        layout_lateral = QVBoxLayout(panel_lateral)
        layout_lateral.setContentsMargins(22, 22, 22, 22)
        layout_lateral.setSpacing(12)

        titulo_panel = QLabel("ACCIONES DEL ROL")
        titulo_panel.setObjectName("TituloSeccion")
        titulo_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_lateral.addWidget(titulo_panel)

        lbl_id = QLabel("ID del rol seleccionado")
        lbl_id.setObjectName("Etiqueta")
        layout_lateral.addWidget(lbl_id)

        self.txt_idrol = QLineEdit()
        self.txt_idrol.setReadOnly(True)
        layout_lateral.addWidget(self.txt_idrol)

        lbl_nombre = QLabel("Nombre del rol")
        lbl_nombre.setObjectName("Etiqueta")
        layout_lateral.addWidget(lbl_nombre)

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ejemplo: Aseadora")
        layout_lateral.addWidget(self.txt_nombre)

        layout_lateral.addSpacing(8)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("BtnPrincipal")
        self.btn_guardar.clicked.connect(self.guardar_rol)
        layout_lateral.addWidget(self.btn_guardar)

        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("BtnAccion")
        self.btn_editar.clicked.connect(self.editar_rol)
        layout_lateral.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_rol)
        layout_lateral.addWidget(self.btn_eliminar)

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setObjectName("BtnAccion")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        layout_lateral.addWidget(self.btn_limpiar)

        self.btn_volver = QPushButton("Volver al Menú")
        self.btn_volver.setObjectName("BtnAccion")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        layout_lateral.addWidget(self.btn_volver)

        layout_lateral.addStretch()

        self.layout_principal.addWidget(panel_lateral)

    def guardar_rol(self):
        nombre = self.txt_nombre.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "Debe ingresar un nombre de rol.")
            return

        try:
            nuevo = ClaseRol(nombrerol=nombre)
            if nuevo.Guardar():
                QMessageBox.information(self, "Éxito", "Rol guardado correctamente.")
                self.cargar_roles()
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el rol.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def editar_rol(self):
        if not self.id_rol_seleccionado:
            QMessageBox.warning(self, "Error", "Seleccione un rol para editar.")
            return

        nombre = self.txt_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Debe ingresar un nombre de rol.")
            return

        try:
            rol = ClaseRol(nombrerol=nombre)
            if rol.Editar(self.id_rol_seleccionado):
                QMessageBox.information(self, "Éxito", "Rol editado correctamente.")
                self.cargar_roles()
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo editar el rol.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_rol(self):
        if not self.id_rol_seleccionado:
            QMessageBox.warning(self, "Error", "Seleccione un rol para eliminar.")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Desea eliminar este rol?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                rol = ClaseRol()
                if rol.Eliminar(self.id_rol_seleccionado):
                    QMessageBox.information(self, "Éxito", "Rol eliminado correctamente.")
                    self.cargar_roles()
                    self.limpiar_campos()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el rol.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def cargar_roles(self):
        registros = self.rol.Listar()
        self.tabla.setRowCount(len(registros))

        for fila, registro in enumerate(registros):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(registro[0])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(registro[1])))

    def seleccionar_rol(self, fila, columna):
        self.id_rol_seleccionado = int(self.tabla.item(fila, 0).text())
        self.txt_idrol.setText(self.tabla.item(fila, 0).text())
        self.txt_nombre.setText(self.tabla.item(fila, 1).text())

    def limpiar_campos(self):
        self.txt_idrol.clear()
        self.txt_nombre.clear()
        self.id_rol_seleccionado = None
        self.tabla.clearSelection()

    def volver_al_menu(self):
        """Vuelve al menú principal"""
        if self.parent_menu:
            self.parent_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormRol()
    ventana.show()
    sys.exit(app.exec())