import os
import pandas as pd


class ProveedorArchivoPlano:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.ultimo_error = None

    def _leer_archivo(self):
        try:
            extension = os.path.splitext(self.ruta_archivo)[1].lower()

            if extension == ".csv":
                df = pd.read_csv(self.ruta_archivo)
            elif extension == ".txt":
                df = pd.read_csv(self.ruta_archivo, delimiter="\t")
            else:
                raise Exception("Formato no soportado. Use .csv o .txt")

            self.ultimo_error = None
            return df

        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo leer el archivo plano: {self.ultimo_error}")

    def obtener_nombre_origen(self):
        return os.path.basename(self.ruta_archivo)

    def obtener_nombre_tabla(self):
        nombre = os.path.basename(self.ruta_archivo)
        return os.path.splitext(nombre)[0]

    def cargar_completo(self):
        return self._leer_archivo()

    def cargar_preview(self, limite=100):
        df = self._leer_archivo()
        return df.head(int(limite)).copy()

    def contar_filas(self):
        df = self._leer_archivo()
        return int(len(df))

    def obtener_columnas(self):
        df = self._leer_archivo()

        columnas = []
        for col in df.columns:
            serie = df[col]
            columnas.append({
                "nombre": str(col),
                "tipo": str(serie.dtype),
                "nulo": bool(serie.isnull().any()),
                "longitud": None
            })

        return columnas

    def obtener_estructura_archivo(self, limite_preview=100, cargar_completa=False):
        nombre_tabla = self.obtener_nombre_tabla()

        estructura = {
            "nombre": nombre_tabla,
            "tipo": "archivo_plano",
            "columnas": self.obtener_columnas(),
            "filas": self.contar_filas(),
            "preview": self.cargar_preview(limite=limite_preview),
            "dataframe": None
        }

        if cargar_completa:
            estructura["dataframe"] = self.cargar_completo()

        return estructura