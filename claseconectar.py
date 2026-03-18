import pyodbc
import mysql.connector


class Conexion:
    def __init__(self, gestor, host, database, user=None, password=None, port=None):
        self.gestor = gestor.lower()
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conexion = None
        self.cursor = None

    def conectar(self):
        if self.gestor == "mysql":
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=int(self.port) if self.port else 3306
            )

        elif self.gestor == "sqlserver":
            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.host};'
                f'DATABASE={self.database};'
                'Trusted_Connection=yes;'
            )

        else:
            raise ValueError("Gestor no soportado")

        self.cursor = self.conexion.cursor()

    def probar_conexion(self):
        try:
            self.conectar()
            return True
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            self.cerrar()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()