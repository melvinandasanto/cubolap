from PyQt6.QtWidgets import QApplication
from FormConexiones import FormConexiones
import formlogin

if __name__ == "__main__":
    app = QApplication([])
    ventana = formlogin.FormularioOLAP()
    ventana.show()
    app.exec_()