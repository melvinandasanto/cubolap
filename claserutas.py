import pandas as pd
import os
from claseconectar import Conectar

class ClaseRutas:
    def __init__(self, id_ruta=None, nombreruta=""):
        self.id_ruta = id_ruta
        self.nombreruta = nombreruta
        self.df_original = None
        self.df_transformado = None

    @property
    def nombre_ruta(self):
        return self.nombreruta

    @nombre_ruta.setter
    def nombre_ruta(self, value):
        self.nombreruta = value

    @property
    def id_ruta(self):
        return self._id_ruta

    @id_ruta.setter
    def id_ruta(self, value):
        self._id_ruta = value

    def __str__(self):
        return f"Ruta: {self.nombreruta}"

    def Guardar(self):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql(
            "INSERT INTO rutas (nombreruta) VALUES (?)",
            (self.nombre_ruta,)
        )
        return resultado

    def Eliminar(self, ruta_id):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql(
            "DELETE FROM rutas WHERE idruta = ?",
            (ruta_id,)
        )
        return resultado

    def Editar(self, ruta_id):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql(
            "UPDATE rutas SET nombreruta = ? WHERE idruta = ?",
            (self.nombre_ruta, ruta_id)
        )
        return resultado

    def Buscar(self, ruta_id):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT idruta, nombreruta FROM rutas WHERE idruta = ?",
            (ruta_id,),
            uno=True
        )

        if resultado:
            self.id_ruta = resultado[0]
            self.nombre_ruta = resultado[1]
            return True
        return False

    def Listar(self):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT idruta, nombreruta FROM rutas ORDER BY idruta DESC"
        )
        return resultado

    def cargar_datos(self, ruta):
        try:
            ext = os.path.splitext(ruta)[1].lower()

            if ext == ".csv":
                self.df_original = pd.read_csv(ruta)
            elif ext in [".xlsx", ".xls"]:
                self.df_original = pd.read_excel(ruta)
            elif ext == ".txt":
                self.df_original = pd.read_csv(ruta, delimiter='\t')
            else:
                return False, "Formato no soportado"

            self.df_transformado = self.df_original.copy()
            return True, self.df_original

        except Exception as e:
            return False, str(e)