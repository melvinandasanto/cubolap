import pandas as pd
import pyodbc
import mysql.connector


class ConexionOrigen:
    def __init__(self, gestor, host, database, user=None, password=None, port=None, instancia=None):
        self.gestor = str(gestor).lower()
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.instancia = instancia
        self.conexion = None

    def conectar(self):
        if self.gestor == "sqlserver":
            servidor = self.host

            if self.instancia:
                servidor = f"{self.host}\\{self.instancia}"
            elif self.port:
                servidor = f"{self.host},{self.port}"

            cadena = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={servidor};"
                f"DATABASE={self.database};"
            )

            if self.user and self.password:
                cadena += f"UID={self.user};PWD={self.password};"
            else:
                cadena += "Trusted_Connection=yes;"

            self.conexion = pyodbc.connect(cadena)

        elif self.gestor == "mysql":
            self.conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=int(self.port) if self.port else 3306
            )
        else:
            raise ValueError("Gestor no soportado. Use 'sqlserver' o 'mysql'.")

        return self.conexion

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None

    def obtener_tablas(self):
        conn = self.conectar()
        try:
            if self.gestor == "sqlserver":
                sql = """
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """
                df = pd.read_sql(sql, conn)
            else:
                sql = """
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    ORDER BY TABLE_NAME
                """
                df = pd.read_sql(sql, conn, params=[self.database])

            return df["TABLE_NAME"].tolist()
        finally:
            self.cerrar()

    def cargar_tabla(self, nombre_tabla, limite=100):
        conn = self.conectar()
        try:
            if self.gestor == "sqlserver":
                sql = f"SELECT TOP {int(limite)} * FROM {nombre_tabla}"
            else:
                sql = f"SELECT * FROM {nombre_tabla} LIMIT {int(limite)}"

            df = pd.read_sql(sql, conn)
            return df
        finally:
            self.cerrar()