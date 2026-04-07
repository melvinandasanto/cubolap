import os
import pandas as pd


class ProveedorArchivoExcel:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.ultimo_error = None
        self.excel_file = None

    def abrir(self):
        try:
            self.excel_file = pd.ExcelFile(self.ruta_archivo)
            self.ultimo_error = None
            return self.excel_file
        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo abrir el archivo Excel: {self.ultimo_error}")

    def cerrar(self):
        self.excel_file = None

    def obtener_hojas(self):
        self.abrir()
        try:
            return self.excel_file.sheet_names
        finally:
            self.cerrar()

    def cargar_hoja_completa(self, nombre_hoja):
        try:
            df = pd.read_excel(self.ruta_archivo, sheet_name=nombre_hoja)
            return df
        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo cargar la hoja '{nombre_hoja}': {self.ultimo_error}")

    def cargar_preview(self, nombre_hoja, limite=100):
        df = self.cargar_hoja_completa(nombre_hoja)
        return df.head(int(limite)).copy()

    def obtener_columnas(self, nombre_hoja):
        df = self.cargar_hoja_completa(nombre_hoja)

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

    def contar_filas(self, nombre_hoja):
        df = self.cargar_hoja_completa(nombre_hoja)
        return int(len(df))

    def obtener_nombre_origen(self):
        return os.path.basename(self.ruta_archivo)

    def obtener_estructura_hoja(self, nombre_hoja, limite_preview=100, cargar_completa=False):
        estructura = {
            "nombre": nombre_hoja,
            "tipo": "hoja_excel",
            "columnas": self.obtener_columnas(nombre_hoja),
            "filas": self.contar_filas(nombre_hoja),
            "preview": self.cargar_preview(nombre_hoja, limite=limite_preview),
            "dataframe": None
        }

        if cargar_completa:
            estructura["dataframe"] = self.cargar_hoja_completa(nombre_hoja)

        return estructura