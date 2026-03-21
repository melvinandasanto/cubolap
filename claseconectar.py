import os
import pyodbc
import mysql.connector


class Conectar:
    def __init__(self):
        self.gestor = "sqlserver"
        self.host = "localhost"
        self.instancia = "SQLEXPRESS"
        self.database = "cubolap"
        self.user = None
        self.password = None
        self.port = None
        self.trusted_connection = True
        self.driver = "ODBC Driver 17 for SQL Server"
        self.timeout = 5

        self.conexion = None
        self.cursor = None
        self.ultimo_error = None

    def _hosts_posibles_sqlserver(self):
        nombre_pc = os.environ.get("COMPUTERNAME", "").strip()

        hosts_base = [self.host, ".", "localhost", "127.0.0.1"]
        if nombre_pc:
            hosts_base.append(nombre_pc)

        vistos = set()
        hosts_base = [h for h in hosts_base if h and not (h in vistos or vistos.add(h))]

        servidores = []

        if self.port:
            for h in hosts_base:
                servidores.append(f"{h},{self.port}")

        if self.instancia:
            for h in hosts_base:
                servidores.append(f"{h}\\{self.instancia}")

        for h in hosts_base:
            servidores.append(h)

        vistos = set()
        servidores = [s for s in servidores if not (s in vistos or vistos.add(s))]
        return servidores

    def _cadenas_sqlserver(self):
        cadenas = []
        for servidor in self._hosts_posibles_sqlserver():
            cadena = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={servidor};"
                f"DATABASE={self.database};"
                f"Connection Timeout={self.timeout};"
            )

            if self.trusted_connection:
                cadena += "Trusted_Connection=yes;"
            else:
                cadena += f"UID={self.user};PWD={self.password};"

            cadenas.append(cadena)

        return cadenas

    def conectar(self):
        if self.gestor != "sqlserver":
            raise ValueError("Solo está configurado SQL Server en esta versión")

        errores = []

        for cadena in self._cadenas_sqlserver():
            try:
                self.conexion = pyodbc.connect(cadena)
                self.cursor = self.conexion.cursor()
                self.ultimo_error = None
                return
            except Exception as e:
                errores.append(str(e))

        self.ultimo_error = "\n\n".join(errores)
        raise Exception(f"No se pudo conectar a SQL Server.\n\n{self.ultimo_error}")

    def probar_conexion(self):
        try:
            self.conectar()
            return True
        except Exception as e:
            self.ultimo_error = str(e)
            print("Error:", e)
            return False
        finally:
            self.cerrar()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conexion:
            self.conexion.close()
            self.conexion = None

    def ejecutar_sql(self, sql, params=None, uno=False):
        self.conectar()
        try:
            if params is not None:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            if sql.strip().upper().startswith("SELECT"):
                return self.cursor.fetchone() if uno else self.cursor.fetchall()

            self.conexion.commit()
            return True

        except Exception as e:
            self.ultimo_error = str(e)
            print("Error al ejecutar SQL:", e)
            return None
        finally:
            self.cerrar()