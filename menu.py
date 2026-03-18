from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menú Principal")
        self.resize(400, 300)

        layout = QVBoxLayout()

        label = QLabel("Bienvenido al sistema 👋")
        layout.addWidget(label)

        btn_salir = QPushButton("Cerrar")
        btn_salir.clicked.connect(self.close)

        layout.addWidget(btn_salir)

        self.setLayout(layout)