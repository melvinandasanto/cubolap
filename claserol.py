from claseconectar import Conectar


class ClaseRol:
    def __init__(self, idrol=None, nombrerol=None):
        self.conexion = Conectar()
        self.idrol = idrol
        self.nombrerol = nombrerol

    def Guardar(self):
        return self.conexion.ejecutar_sql(
            "INSERT INTO dbo.rol (nombrerol) VALUES (?)",
            (self.nombrerol,)
        )

    def Listar(self):
        resultado = self.conexion.ejecutar_sql(
            "SELECT idrol, nombrerol FROM dbo.rol ORDER BY idrol DESC"
        )
        return resultado if resultado else []

    def Editar(self, idrol):
        return self.conexion.ejecutar_sql(
            "UPDATE dbo.rol SET nombrerol = ? WHERE idrol = ?",
            (self.nombrerol, idrol)
        )

    def Eliminar(self, idrol):
        return self.conexion.ejecutar_sql(
            "DELETE FROM dbo.rol WHERE idrol = ?",
            (idrol,)
        )