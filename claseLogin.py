from claseconectar import Conexion


class Autenticacion:
    def __init__(self, gestor, host, database, user=None, password=None, port=None):
        self.conexion = Conexion(
            gestor=gestor,
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

    def login(self, usuario, contrasena):
        # 🔹 Usuario por defecto
        if usuario == "default" and contrasena == "00000":
            return True

        try:
            # 🔹 Consulta (SQL Server usa ?, MySQL también lo acepta aquí con connector)
            consulta = "SELECT * FROM usuarios WHERE nombre = ? AND contrasena = ?"

            resultado = self.conexion.ejecutar_sql(
                consulta,
                (usuario, contrasena),
                uno=True
            )

            if resultado:
                return True
            else:
                return False

        except Exception as e:
            print("Error en login:", e)
            return False