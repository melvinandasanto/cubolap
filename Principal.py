import sys

from PyQt6.QtWidgets import QApplication
import formlogin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_login = formlogin.FormLogin()
    ventana_login.show()
    sys.exit(app.exec())