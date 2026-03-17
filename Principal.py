from PyQt6.QtWidgets import QApplication
from FormConexiones import FormConexiones

if __name__ == "__main__":
    app = QApplication([])
    ventana = FormConexiones()
    ventana.show()
    app.exec_()