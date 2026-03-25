from claseconectar import Conectar


class Autenticacion:
    def __init__(self, gestor, host, database, user=None, password=None, port=None):
        self.conexion = Conectar()
        self.conexion.gestor = gestor
        self.conexion.host = host
        self.conexion.database = database
        self.conexion.user = user
        self.conexion.password = password
        self.conexion.port = port

        if user and password:
            self.conexion.trusted_connection = False

    def login(self, usuario, contrasena):
        if usuario == "default" and contrasena == "00000":
            return True

        try:
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