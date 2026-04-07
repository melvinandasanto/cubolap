import os
from conexionorigen import ConexionOrigen
from proveedorarchivoexcel import ProveedorArchivoExcel
from proveedorarchivoplano import ProveedorArchivoPlano


class ConstructorModeloDatos:
    def __init__(self):
        self.ultimo_error = None

    def construir_desde_conexion(
        self,
        gestor,
        host,
        database,
        user=None,
        password=None,
        port=None,
        instancia=None,
        limite_preview=100,
        cargar_completa=False
    ):
        try:
            proveedor = ConexionOrigen(
                gestor=gestor,
                host=host,
                database=database,
                user=user,
                password=password,
                port=port,
                instancia=instancia
            )

            tablas = proveedor.obtener_tablas()
            relaciones = proveedor.obtener_relaciones()

            entidades = {}

            for tabla in tablas:
                entidades[tabla] = proveedor.obtener_estructura_tabla(
                    nombre_tabla=tabla,
                    limite_preview=limite_preview,
                    cargar_completa=cargar_completa
                )

            modelo_datos = {
                "tipo_origen": "conexion",
                "nombre_origen": str(database),
                "entidades": entidades,
                "relaciones": relaciones
            }

            self.ultimo_error = None
            return modelo_datos

        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo construir el modelo desde conexión: {self.ultimo_error}")

    def construir_desde_excel(self, ruta_excel, limite_preview=100, cargar_completa=False):
        try:
            proveedor = ProveedorArchivoExcel(ruta_excel)
            hojas = proveedor.obtener_hojas()

            entidades = {}
            for hoja in hojas:
                entidades[hoja] = proveedor.obtener_estructura_hoja(
                    nombre_hoja=hoja,
                    limite_preview=limite_preview,
                    cargar_completa=cargar_completa
                )

            modelo_datos = {
                "tipo_origen": "archivo_excel",
                "nombre_origen": proveedor.obtener_nombre_origen(),
                "entidades": entidades,
                "relaciones": []
            }

            self.ultimo_error = None
            return modelo_datos

        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo construir el modelo desde Excel: {self.ultimo_error}")

    def construir_desde_archivo_plano(self, ruta_archivo, limite_preview=100, cargar_completa=False):
        try:
            proveedor = ProveedorArchivoPlano(ruta_archivo)

            estructura = proveedor.obtener_estructura_archivo(
                limite_preview=limite_preview,
                cargar_completa=cargar_completa
            )

            modelo_datos = {
                "tipo_origen": "archivo_plano",
                "nombre_origen": proveedor.obtener_nombre_origen(),
                "entidades": {
                    estructura["nombre"]: estructura
                },
                "relaciones": []
            }

            self.ultimo_error = None
            return modelo_datos

        except Exception as e:
            self.ultimo_error = str(e)
            raise Exception(f"No se pudo construir el modelo desde archivo plano: {self.ultimo_error}")

    def construir_desde_ruta(self, ruta_archivo, limite_preview=100, cargar_completa=False):
        extension = os.path.splitext(ruta_archivo)[1].lower()

        if extension in [".xlsx", ".xls"]:
            return self.construir_desde_excel(
                ruta_excel=ruta_archivo,
                limite_preview=limite_preview,
                cargar_completa=cargar_completa
            )

        elif extension in [".csv", ".txt"]:
            return self.construir_desde_archivo_plano(
                ruta_archivo=ruta_archivo,
                limite_preview=limite_preview,
                cargar_completa=cargar_completa
            )

        else:
            raise Exception("Formato de archivo no soportado")