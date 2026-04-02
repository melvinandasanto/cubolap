import pyodbc
import mysql.connector


class Conectar:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.ultimo_error = None

    def conectar(self, gestor, host, database, user=None, password=None, port=None):
        try:
            gestor = (gestor or "").lower().strip()

            if gestor == "mysql":
                self.conexion = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=int(port) if port else 3306
                )

            elif gestor == "sqlserver":
                server = f"{host},{port}" if port else host

                if user and password:
                    self.conexion = pyodbc.connect(
                        "DRIVER={ODBC Driver 17 for SQL Server};"
                        f"SERVER={server};"
                        f"DATABASE={database};"
                        f"UID={user};"
                        f"PWD={password};"
                    )
                else:
                    self.conexion = pyodbc.connect(
                        "DRIVER={ODBC Driver 17 for SQL Server};"
                        f"SERVER={server};"
                        f"DATABASE={database};"
                        "Trusted_Connection=yes;"
                    )
            else:
                raise Exception("Gestor no soportado. Use mysql o sqlserver")

            self.cursor = self.conexion.cursor()
            return self.conexion

        except Exception as e:
            self.ultimo_error = str(e)
            print("Error al conectar:", e)
            raise

    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
        except:
            pass

        try:
            if self.conexion:
                self.conexion.close()
        except:
            pass

        self.cursor = None
        self.conexion = None

    def ejecutar_sql(self, sql, params=None, uno=False):
        self.conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=cubolap;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conexion.cursor()

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