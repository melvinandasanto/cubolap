import pyodbc
import mysql.connector


class Conectar:
    DEFAULT_GESTOR = "sqlserver"
    DEFAULT_HOST = "localhost"
    DEFAULT_DATABASE = "cubolap"
    DEFAULT_TIMEOUT = 5

    def __init__(self, gestor=None, host=None, database=None, user=None, password=None, port=None, timeout=None):
        self.gestor = (gestor or self.DEFAULT_GESTOR).lower().strip()
        self.host = host or self.DEFAULT_HOST
        self.database = database or self.DEFAULT_DATABASE
        self.user = user
        self.password = password
        self.port = port
        self.timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT

        self.conexion = None
        self.cursor = None
        self.ultimo_error = None

    def conectar(self, gestor=None, host=None, database=None, user=None, password=None, port=None, timeout=None):
        if gestor is None:
            gestor = self.gestor
        if host is None:
            host = self.host
        if database is None:
            database = self.database
        if user is None:
            user = self.user
        if password is None:
            password = self.password
        if port is None:
            port = self.port
        if timeout is None:
            timeout = self.timeout

        gestor = (gestor or "").lower().strip()
        host = host or ""
        database = database or ""

        if not gestor or not host or not database:
            raise Exception(
                "Faltan parámetros de conexión. Configure gestor, host y base de datos."
            )

        if self.conexion is not None and self.cursor is not None:
            return self.conexion

        try:
            if gestor == "mysql":
                self.conexion = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=int(port) if port else 3306,
                    connection_timeout=timeout
                )

            elif gestor == "sqlserver":
                servidores = [host]
                if "\\" not in host and not port:
                    servidores += [
                        f"{host}\\SQLEXPRESS",
                        f"{host}\\MSSQLSERVER",
                        f"{host}\\SQL2022"
                    ]

                conectado = False
                ultimo_error = None

                for servidor in servidores:
                    try:
                        if port:
                            servidor_conexion = f"{servidor},{port}"
                        else:
                            servidor_conexion = servidor

                        connection_string = (
                            "DRIVER={ODBC Driver 17 for SQL Server};"
                            f"SERVER={servidor_conexion};"
                            f"DATABASE={database};"
                            f"Connect Timeout={timeout};"
                            "TrustServerCertificate=yes;"
                        )

                        if user and password:
                            connection_string += f"UID={user};PWD={password};"
                        else:
                            connection_string += "Trusted_Connection=yes;"

                        self.conexion = pyodbc.connect(connection_string)
                        conectado = True
                        break

                    except Exception as e:
                        ultimo_error = e
                        continue

                if not conectado:
                    raise Exception(
                        "No se pudo conectar a SQL Server. "
                        f"Último error: {ultimo_error}"
                    )

            else:
                raise Exception("Gestor no soportado. Use 'sqlserver' o 'mysql'.")

            self.cursor = self.conexion.cursor()
            return self.conexion

        except Exception as e:
            self.ultimo_error = str(e)
            print("Error al conectar:", e)
            self.conexion = None
            self.cursor = None
            raise

    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Exception:
            pass

        try:
            if self.conexion:
                self.conexion.close()
        except Exception:
            pass

        self.cursor = None
        self.conexion = None

    def ejecutar_sql(self, sql, params=None, uno=False):
        try:
            if self.conexion is None or self.cursor is None:
                self.conectar()

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