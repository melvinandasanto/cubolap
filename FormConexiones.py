import re

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QMessageBox
)
from claseconectar import Conexion

class FormConexiones(QWidget):
    def __init__(self):
        super().__init__()
        self.iniciarGUI()
        self.conexion = Conexion()

    def iniciarGUI(self):
        self.setWindowTitle("CONEXIONES")
        self.resize(500, 500)
        self.label_codigobarra = QLabel("Nombre Conexion:")
        self.text_codigobarra = QLineEdit()
        self.label_nombre = QLineEdit("Gestor")
        self.text_nombre = QHBoxLayout()
        self.label_descripcion = QLabel("Descripcion:")
        self.text_descripcion = QLineEdit()
        self.label_existencia = QLabel("Existencia:")
        self.text_existencia = QLineEdit()
        self.label_precio = QLabel("Precio:")
        self.text_precio = QLineEdit()
        self.label_costo = QLabel("Costo:")
        self.text_costo = QLineEdit()
        self.label_idtipo = QLabel("Tipo:")
        self.text_idtipo = QLineEdit()
        self.label_idimpuesto = QLabel("Id Impuesto:")
        self.text_idimpuesto = QLineEdit()
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiarcampos)
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_producto)
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_producto)
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_probar = QPushButton("Probar Conexión")
        self.btn_probar.clicked.connect(self.probar_conexion)
        layout = QVBoxLayout()
        layout.addWidget(self.label_codigobarra)
        layout.addWidget(self.text_codigobarra)
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.text_nombre)
        layout.addWidget(self.label_descripcion)
        layout.addWidget(self.text_descripcion)
        layout.addWidget(self.label_existencia)
        layout.addWidget(self.text_existencia)
        layout.addWidget(self.label_precio)
        layout.addWidget(self.text_precio)
        layout.addWidget(self.label_costo)
        layout.addWidget(self.text_costo)
        layout.addWidget(self.label_idtipo)
        layout.addWidget(self.text_idtipo)
        layout.addWidget(self.label_idimpuesto)
        layout.addWidget(self.text_idimpuesto)
        botones = QHBoxLayout()
        botones.addWidget(self.btn_limpiar)
        botones.addWidget(self.btn_buscar)
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_eliminar)
        botones.addWidget(self.btn_editar)
        botones = QHBoxLayout()
        botones.addWidget(self.btn_limpiar)
        botones.addWidget(self.btn_buscar)
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_eliminar)
        botones.addWidget(self.btn_editar)
        layout.addLayout(botones)
        self.setLayout(layout)

    def guardar_producto(self):
        if not self.validar_campos():
            return
        self.obtenerproductodesdeformulario()
        self.producto.Guardar()
        QMessageBox.information(self, "Éxito", "Producto guardado correctamente")
        self.limpiarcampos()

    def editar_producto(self):
        if not self.validar_campos():
            return
        producto_id = self.text_id.text()
        if not producto_id.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número válido")
            return
        self.obtenerproductodesdeformulario()
        self.producto.Editar(int(producto_id))
        QMessageBox.information(self, "Éxito", "Producto editado correctamente")
        self.limpiarcampos()

    def eliminar_producto(self):
        producto_id = self.text_id.text()
        if not producto_id.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número válido")
            return

        confirmacion = QMessageBox.question(
            self, "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con ID {producto_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            self.producto.Eliminar(int(producto_id))
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
            self.limpiarcampos()

    def buscar_producto(self):
        producto_id = self.text_id.text()
        if not producto_id.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número válido")
            return

        if self.producto.Buscar(int(producto_id)):

            self.text_codigobarra.setText(self.producto.codigobarra)
            self.text_nombre.setText(self.producto.nombre)
            self.text_descripcion.setText(self.producto.descripcion)
            self.text_existencia.setText(str(self.producto.existencia))
            self.text_precio.setText(str(self.producto.precio))
            self.text_costo.setText(str(self.producto.costo))
            self.text_idtipo.setText(str(self.producto.idtipo))
            self.text_idimpuesto.setText(str(self.producto.idimpuesto))

        else:
            QMessageBox.information(
                self, "No encontrado",
                f"No se encontró un producto con ID {producto_id}"
            )
    
    def limpiarcampos(self):
        self.text_id.clear()
        self.text_codigobarra.clear()
        self.text_nombre.clear()
        self.text_descripcion.clear()
        self.text_existencia.clear()
        self.text_precio.clear()
        self.text_costo.clear()
        self.text_idtipo.clear()
        self.text_idimpuesto.clear()
    
    def obtenerproductodesdeformulario(self):
        codigobarra = self.text_codigobarra.text()
        nombre = self.text_nombre.text()
        descripcion = self.text_descripcion.text()
        existencia = int(self.text_existencia.text())
        precio = float(self.text_precio.text())
        costo = float(self.text_costo.text())
        idtipo = int(self.text_idtipo.text())
        idimpuesto = int(self.text_idimpuesto.text())

    def validar_campos(self):
            patroncodigobarra = r"^\d{13}$"
            patronnombre = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]{3,100}$"
            patrondescripcion = r"^.{10,500}$"
            patronexistencia = r"^\d+$"
            patronprecioycosto = r"^\d+(\.\d{1,2})?$"
            if not re.match(patroncodigobarra, self.text_codigobarra.text()):
                QMessageBox.warning(self, "Error", "El código de barra debe tener exactamente 13 dígitos")
                return False

            if not re.match(patronnombre, self.text_nombre.text()):
                QMessageBox.warning(self, "Error", "El nombre solo puede contener letras y espacios")
                return False

            if not re.match(patrondescripcion, self.text_descripcion.text()):
                QMessageBox.warning(self, "Error", "La descripción debe tener entre 10 y 500 caracteres")
                return False
                return False

            if not self.text_descripcion.text():
                QMessageBox.warning(self, "Error", "La descripción es obligatoria")
                return False

            if not re.match(patronexistencia, self.text_existencia.text()):
                QMessageBox.warning(self, "Error", "La existencia debe ser un número no negativo")
                return False

            if not re.match(patronprecioycosto, self.text_precio.text()):
                QMessageBox.warning(self, "Error", "El precio debe ser un número no negativo")
                return False

            if not re.match(patronprecioycosto, self.text_costo.text()):
                QMessageBox.warning(self, "Error", "El costo debe ser un número no negativo")
                return False

            if not self.text_idtipo.text().isdigit():
                QMessageBox.warning(self, "Error", "El ID del tipo de producto debe ser un número válido")
                return False

            if not self.text_idimpuesto.text().isdigit():
                QMessageBox.warning(self, "Error", "El ID del impuesto debe ser un número válido")
                return False
            return True