import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLineEdit,
    QAbstractItemView
)
from PyQt6.QtCore import Qt
from claserutas import ClaseRutas
from claseusuario import Usuario


# Clase para gestionar rutas de archivos
class FormRutas(QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu
        self.setWindowTitle("Sistema OLAP - RUTAS")
        self.resize(1350, 780)

        self.ruta_modelo = ClaseRutas()
        self.id_ruta_seleccionada = None
        self.df_actual = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a2634;
            }

            QWidget {
                color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QFrame#Tarjeta {
                background-color: #243447;
                border-radius: 10px;
            }

            QLabel#Titulo {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }

            QLabel#Subtitulo {
                font-size: 15px;
                font-weight: bold;
                color: #d9e2ec;
                margin-top: 6px;
                margin-bottom: 6px;
            }

            QLineEdit {
                background-color: #071a2b;
                border: 1px solid #3d85c6;
                border-radius: 8px;
                padding: 8px;
                color: white;
            }

            QPushButton#BtnAzul {
                background-color: #4b8fd1;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
                color: white;
            }

            QPushButton#BtnAzul:hover {
                background-color: #63a3df;
            }

            QPushButton#BtnRojo {
                background-color: #c44757;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
                color: white;
            }

            QPushButton#BtnRojo:hover {
                background-color: #d85c6b;
            }

            QPushButton#BtnGris {
                background-color: #52657a;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
                color: white;
            }

            QPushButton#BtnGris:hover {
                background-color: #64798f;
            }

            QPushButton#BtnVolver {
                background-color: #e67e22;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
                color: white;
            }

            QPushButton#BtnVolver:hover {
                background-color: #f39c12;
            }

            QTableWidget {
                background-color: #071a2b;
                gridline-color: #243447;
                color: white;
                border: 1px solid #2f4154;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #1b2b45;
                color: #4ea3ff;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        self.init_ui()
        self.cargar_rutas_tabla()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(8, 8, 8, 8)
        layout_principal.setSpacing(10)

        lbl_tit = QLabel("4. RUTAS")
        lbl_tit.setObjectName("Titulo")
        layout_principal.addWidget(lbl_tit, 0)

        # TABLA SUPERIOR
        lbl_rutas = QLabel("Rutas guardadas")
        lbl_rutas.setObjectName("Subtitulo")
        layout_principal.addWidget(lbl_rutas, 0)

        self.tabla_rutas = QTableWidget()
        self.tabla_rutas.setColumnCount(2)
        self.tabla_rutas.setHorizontalHeaderLabels(["ID", "Ruta"])
        self.tabla_rutas.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_rutas.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_rutas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_rutas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_rutas.cellClicked.connect(self.seleccionar_ruta_guardada)
        layout_principal.addWidget(self.tabla_rutas, 1)

        # CAJA Y BOTONES
        tarjeta_ruta = QFrame()
        tarjeta_ruta.setObjectName("Tarjeta")
        layout_ruta = QVBoxLayout(tarjeta_ruta)
        layout_ruta.setContentsMargins(12, 12, 12, 12)

        lbl_gestion = QLabel("Gestión de rutas de archivos")
        lbl_gestion.setObjectName("Subtitulo")
        layout_ruta.addWidget(lbl_gestion)

        fila_ruta = QHBoxLayout()
        self.txt_ruta = QLineEdit()
        self.txt_ruta.setPlaceholderText("Ingrese o seleccione una ruta de archivo...")
        fila_ruta.addWidget(self.txt_ruta, 6)

        self.btn_examinar = QPushButton("Examinar")
        self.btn_examinar.setObjectName("BtnAzul")
        self.btn_examinar.clicked.connect(self.seleccionar_archivo)
        fila_ruta.addWidget(self.btn_examinar, 1)

        layout_ruta.addLayout(fila_ruta)

        fila_botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("BtnAzul")
        self.btn_guardar.clicked.connect(self.guardar_ruta)
        fila_botones.addWidget(self.btn_guardar)

        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("BtnGris")
        self.btn_editar.clicked.connect(self.editar_ruta)
        fila_botones.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnRojo")
        self.btn_eliminar.clicked.connect(self.eliminar_ruta)
        fila_botones.addWidget(self.btn_eliminar)

        self.btn_cargar_preview = QPushButton("Cargar vista previa")
        self.btn_cargar_preview.setObjectName("BtnAzul")
        self.btn_cargar_preview.clicked.connect(self.cargar_preview_desde_textbox)
        fila_botones.addWidget(self.btn_cargar_preview)

        self.btn_volver = QPushButton("Volver al Menú")
        self.btn_volver.setObjectName("BtnVolver")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        fila_botones.addWidget(self.btn_volver)

        layout_ruta.addLayout(fila_botones)
        layout_principal.addWidget(tarjeta_ruta, 0)

        # TABLA INFERIOR
        lbl_preview = QLabel("Vista previa de los datos")
        lbl_preview.setObjectName("Subtitulo")
        layout_principal.addWidget(lbl_preview, 0)

        self.tabla_preview = QTableWidget()
        self.tabla_preview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_preview.verticalHeader().setVisible(False)
        layout_principal.addWidget(self.tabla_preview, 1)

    def obtener_ruta_desde_tabla(self):
        if self.id_ruta_seleccionada is not None:
            for row in range(self.tabla_rutas.rowCount()):
                if int(self.tabla_rutas.item(row, 0).text()) == self.id_ruta_seleccionada:
                    return self.tabla_rutas.item(row, 1).text()
        return None
    
    def validar_campos(self):
        ruta = self.txt_ruta.text().strip()

        if not ruta:
            QMessageBox.warning(self, "Aviso", "La ruta no puede quedar vacía.")
            self.txt_ruta.setFocus()
            return False

        return True

    def guardar_ruta(self):
        if not self.validar_campos():
            return

        try:
            self.ruta_modelo.nombre_ruta = self.txt_ruta.text().strip()
            resultado = self.ruta_modelo.Guardar()

            if resultado:
                QMessageBox.information(self, "Éxito", "Ruta guardada correctamente")
                self.cargar_rutas_tabla()
                self.limpiar_campos()
            else:
                mensaje = getattr(self.ruta_modelo, "ultimo_error", "")
                QMessageBox.warning(self, "Error", "No se pudo guardar la ruta")

        except Exception as e:
            mensaje = str(e)
            if "duplicate key" in mensaje.lower() or "unique key" in mensaje.lower():
                QMessageBox.warning(self, "Aviso", "Esa ruta ya está guardada.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la ruta:\n{mensaje}")

    def editar_ruta(self):
        if not self.validar_campos():
            return

        if self.id_ruta_seleccionada is None:
            QMessageBox.warning(self, "Aviso", "Seleccione una ruta de la tabla.")
            return

        try:
            self.ruta_modelo.nombre_ruta = self.txt_ruta.text().strip()
            resultado = self.ruta_modelo.Editar(self.id_ruta_seleccionada)

            if resultado:
                QMessageBox.information(self, "Éxito", "Ruta actualizada correctamente")
                self.cargar_rutas_tabla()
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la ruta")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la ruta:\n{str(e)}")

    def eliminar_ruta(self):
        if self.id_ruta_seleccionada is None:
            QMessageBox.warning(self, "Error", "Seleccione una ruta válida para eliminar")
            return

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la ruta con ID {self.id_ruta_seleccionada}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                resultado = self.ruta_modelo.Eliminar(self.id_ruta_seleccionada)

                if resultado:
                    QMessageBox.information(self, "Éxito", "Ruta eliminada correctamente")
                    self.cargar_rutas_tabla()
                    self.limpiar_campos()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la ruta")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la ruta:\n{str(e)}")

    def limpiar_campos(self):
        self.txt_ruta.clear()
        self.id_ruta_seleccionada = None

    def cargar_rutas_tabla(self):
        try:
            self.tabla_rutas.setRowCount(0)
            lista = self.ruta_modelo.Listar()

            if lista:
                for fila_num, fila in enumerate(lista):
                    self.tabla_rutas.insertRow(fila_num)

                    idruta = fila[0]
                    nombreruta = fila[1]

                    item_id = QTableWidgetItem(str(idruta))
                    item_nombre = QTableWidgetItem(nombreruta)

                    for item_tabla in [item_id, item_nombre]:
                        item_tabla.setForeground(Qt.GlobalColor.white)

                    self.tabla_rutas.setItem(fila_num, 0, item_id)
                    self.tabla_rutas.setItem(fila_num, 1, item_nombre)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla:\n{str(e)}")

    def seleccionar_ruta_guardada(self, row, column):
        self.id_ruta_seleccionada = int(self.tabla_rutas.item(row, 0).text())
        ruta = self.tabla_rutas.item(row, 1).text()
        self.txt_ruta.setText(ruta)

    def seleccionar_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Dataset",
            "",
            "Archivos (*.csv *.xlsx *.xls *.txt)"
        )

        if ruta:
            self.txt_ruta.setText(ruta)
            self.cargar_preview(ruta)

    def cargar_preview_desde_textbox(self):
        ruta = self.txt_ruta.text().strip()

        if not ruta:
            QMessageBox.warning(self, "Aviso", "Debe escribir o seleccionar una ruta.")
            return

        self.cargar_preview(ruta)

    def cargar_preview(self, ruta):
        if not os.path.exists(ruta):
            QMessageBox.warning(self, "Ruta inválida", "La ruta especificada no existe.")
            return

        try:
            exito, datos = self.ruta_modelo.cargar_datos(ruta)

            if exito:
                self.df_actual = datos
                self.actualizar_tabla_preview(datos)
            else:
                QMessageBox.critical(self, "Error", str(datos))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def actualizar_tabla_preview(self, df):
        self.tabla_preview.clear()
        self.tabla_preview.setRowCount(len(df))
        self.tabla_preview.setColumnCount(len(df.columns))
        self.tabla_preview.setHorizontalHeaderLabels([str(col) for col in df.columns])

        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.tabla_preview.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def volver_al_menu(self):
        """Vuelve al menú principal"""
        if self.parent_menu:
            self.parent_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormRutas()
    ventana.show()
    sys.exit(app.exec())