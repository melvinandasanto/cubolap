from Conexiones import conexionmysql, conexionsqlserver
from Conexiones.conexionmysql import ConexionMYSQL
from Conexiones.conexionsqlserver import ConexionSQLServer

class ClaseConexiones:
    def __init__(self):
        # Diccionario para almacenar conexiones
        self.conexiones = {}

    def agregar_conexion(self, nombre, gestor, **kwargs):
        """Agregar una conexión según el gestor"""
        if gestor.lower() == "mysql":
            self.conexiones[nombre] = ConexionMYSQL(**kwargs)
        elif gestor.lower() == "sqlserver":
            self.conexiones[nombre] = ConexionSQLServer(**kwargs)
        else:
            raise ValueError("Gestor no soportado")

    def obtener_conexion(self, nombre):
        """Obtener objeto de conexión"""
        if nombre not in self.conexiones:
            raise ValueError(f"No existe la conexión '{nombre}'")
        return self.conexiones[nombre]

    def probar_conexion(self, nombre):
        """Probar la conexión usando la clase correspondiente"""
        if nombre not in self.conexiones:
            raise ValueError(f"No existe la conexión '{nombre}'")
        try:
            conn = self.conexiones[nombre].conectar()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def actualizar_conexion(self, nombre, **kwargs):
        """Actualizar parámetros de una conexión"""
        if nombre not in self.conexiones:
            raise ValueError(f"No existe la conexión '{nombre}'")
        # recrea la conexión con nuevos parámetros
        gestor = self.conexiones[nombre].gestor
        self.agregar_conexion(nombre, gestor, **kwargs)

    def eliminar_conexion(self, nombre):
        """Eliminar una conexión"""
        if nombre in self.conexiones:
            del self.conexiones[nombre]
        else:
            raise ValueError(f"No existe la conexión '{nombre}'")

    def listar_conexiones(self):
        """Listar todas las conexiones guardadas"""
        return list(self.conexiones.keys())
