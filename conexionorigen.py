import pandas as pd
import pyodbc
import mysql.connector


class ConexionOrigen:
    def __init__(self, gestor, host, database, user=None, password=None, port=None, instancia=None, timeout=5):
        self.gestor = str(gestor).lower().strip()
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.instancia = instancia
        self.timeout = timeout
        self.conexion = None
        self.ultimo_error = None

    def conectar(self):
        try:
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
                    f"Connection Timeout={self.timeout};"
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
                    port=int(self.port) if self.port else 3306,
                    connection_timeout=self.timeout
                )
            else:
                raise ValueError("Gestor no soportado. Use 'sqlserver' o 'mysql'.")

            self.ultimo_error = None
            return self.conexion

        except Exception as e:
            self.ultimo_error = str(e)
            raise

    def cerrar(self):
        if self.conexion:
            try:
                self.conexion.close()
            except Exception:
                pass
            self.conexion = None

    def _ejecutar_query_df(self, sql, params=None):
        conn = self.conectar()
        try:
            if params is not None:
                return pd.read_sql(sql, conn, params=params)
            return pd.read_sql(sql, conn)
        finally:
            self.cerrar()

    def _formatear_nombre_tabla(self, nombre_tabla):
        nombre_tabla = str(nombre_tabla).strip()

        if self.gestor == "sqlserver":
            if "." in nombre_tabla:
                partes = nombre_tabla.split(".")
                return ".".join(f"[{p}]" for p in partes)
            return f"[{nombre_tabla}]"

        elif self.gestor == "mysql":
            if "." in nombre_tabla:
                partes = nombre_tabla.split(".")
                return ".".join(f"`{p}`" for p in partes)
            return f"`{nombre_tabla}`"

        return nombre_tabla

    def obtener_tablas(self):
        if self.gestor == "sqlserver":
            sql = """
                SELECT TABLE_SCHEMA, TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """
            df = self._ejecutar_query_df(sql)
            return [
                f"{fila['TABLE_SCHEMA']}.{fila['TABLE_NAME']}"
                for _, fila in df.iterrows()
            ]

        elif self.gestor == "mysql":
            sql = """
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = %s
                AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """
            df = self._ejecutar_query_df(sql, params=[self.database])
            return df["TABLE_NAME"].tolist()

    def obtener_columnas(self, nombre_tabla):
        if self.gestor == "sqlserver":
            if "." in nombre_tabla:
                esquema, tabla = nombre_tabla.split(".", 1)
            else:
                esquema, tabla = "dbo", nombre_tabla

            sql = """
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = ?
                AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """
            df = self._ejecutar_query_df(sql, params=[esquema, tabla])

        elif self.gestor == "mysql":
            sql = """
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """
            df = self._ejecutar_query_df(sql, params=[self.database, nombre_tabla])

        columnas = []
        for _, fila in df.iterrows():
            columnas.append({
                "nombre": str(fila["COLUMN_NAME"]),
                "tipo": str(fila["DATA_TYPE"]),
                "nulo": str(fila["IS_NULLABLE"]) == "YES",
                "longitud": None if pd.isna(fila["CHARACTER_MAXIMUM_LENGTH"]) else int(fila["CHARACTER_MAXIMUM_LENGTH"])
            })

        return columnas

    def contar_filas(self, nombre_tabla):
        tabla_sql = self._formatear_nombre_tabla(nombre_tabla)
        sql = f"SELECT COUNT(*) AS total FROM {tabla_sql}"
        df = self._ejecutar_query_df(sql)

        if df.empty:
            return 0

        return int(df.iloc[0]["total"])

    def cargar_preview(self, nombre_tabla, limite=100):
        tabla_sql = self._formatear_nombre_tabla(nombre_tabla)
        limite = int(limite)

        if self.gestor == "sqlserver":
            sql = f"SELECT TOP {limite} * FROM {tabla_sql}"
        else:
            sql = f"SELECT * FROM {tabla_sql} LIMIT {limite}"

        return self._ejecutar_query_df(sql)

    def cargar_tabla_completa(self, nombre_tabla):
        tabla_sql = self._formatear_nombre_tabla(nombre_tabla)
        sql = f"SELECT * FROM {tabla_sql}"
        return self._ejecutar_query_df(sql)

    def obtener_relaciones(self):
        if self.gestor == "sqlserver":
            sql = """
                SELECT
                    fk.name AS nombre_relacion,
                    tp.name AS tabla_origen,
                    cp.name AS columna_origen,
                    tr.name AS tabla_destino,
                    cr.name AS columna_destino
                FROM sys.foreign_keys fk
                INNER JOIN sys.foreign_key_columns fkc
                    ON fk.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables tp
                    ON fkc.parent_object_id = tp.object_id
                INNER JOIN sys.columns cp
                    ON fkc.parent_object_id = cp.object_id
                    AND fkc.parent_column_id = cp.column_id
                INNER JOIN sys.tables tr
                    ON fkc.referenced_object_id = tr.object_id
                INNER JOIN sys.columns cr
                    ON fkc.referenced_object_id = cr.object_id
                    AND fkc.referenced_column_id = cr.column_id
                ORDER BY tp.name, tr.name
            """
            df = self._ejecutar_query_df(sql)

        elif self.gestor == "mysql":
            sql = """
                SELECT
                    CONSTRAINT_NAME AS nombre_relacion,
                    TABLE_NAME AS tabla_origen,
                    COLUMN_NAME AS columna_origen,
                    REFERENCED_TABLE_NAME AS tabla_destino,
                    REFERENCED_COLUMN_NAME AS columna_destino
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL
                ORDER BY TABLE_NAME, REFERENCED_TABLE_NAME
            """
            df = self._ejecutar_query_df(sql, params=[self.database])

        relaciones = []
        for _, fila in df.iterrows():
            relaciones.append({
                "nombre_relacion": str(fila["nombre_relacion"]),
                "origen_entidad": str(fila["tabla_origen"]),
                "origen_columna": str(fila["columna_origen"]),
                "destino_entidad": str(fila["tabla_destino"]),
                "destino_columna": str(fila["columna_destino"])
            })

        return relaciones

    def obtener_estructura_tabla(self, nombre_tabla, limite_preview=100, cargar_completa=False):
        estructura = {
            "nombre": nombre_tabla,
            "tipo": "tabla",
            "columnas": self.obtener_columnas(nombre_tabla),
            "filas": self.contar_filas(nombre_tabla),
            "preview": self.cargar_preview(nombre_tabla, limite=limite_preview),
            "dataframe": None
        }

        if cargar_completa:
            estructura["dataframe"] = self.cargar_tabla_completa(nombre_tabla)

        return estructura