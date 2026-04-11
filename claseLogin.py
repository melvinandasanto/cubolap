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
        """Login y retorna datos del usuario si es exitoso, None si no"""
        if usuario == "default" and contrasena == "00000":
            # Usuario por defecto
            return {
                'id': 1,
                'nombre': 'default',
                'id_rol': 1,
                'nombre_rol': 'Administrador',
                'activo': True
            }

        try:
            consulta = """
                SELECT u.idusuario, u.nombre, u.idrol, r.nombrerol, u.activo 
                FROM usuario u
                LEFT JOIN rol r ON u.idrol = r.idrol
                WHERE u.nombre = ? AND u.contrasenia = ?
            """

            resultado = self.conexion.ejecutar_sql(
                consulta,
                (usuario, contrasena),
                uno=True
            )

            if resultado:
                return {
                    'id': resultado[0],
                    'nombre': resultado[1],
                    'id_rol': resultado[2],
                    'nombre_rol': resultado[3] or 'Sin Rol',
                    'activo': resultado[4]
                }
            else:
                return None

        except Exception as e:
            print("Error en login:", e)
            return None