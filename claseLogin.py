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

    def hay_usuarios(self):
        """Verifica si hay usuarios en la tabla"""
        try:
            consulta = "SELECT COUNT(*) FROM usuario"
            resultado = self.conexion.ejecutar_sql(consulta, uno=True)
            return resultado[0] > 0 if resultado else False
        except Exception as e:
            print("Error al contar usuarios:", e)
            return False

    def hay_admin(self):
        """Verifica si hay al menos un usuario admin en la base de datos"""
        try:
            consulta = """
                SELECT COUNT(*) FROM usuario u
                LEFT JOIN rol r ON u.idrol = r.idrol
                WHERE r.nombrerol = 'Administrador'
            """
            resultado = self.conexion.ejecutar_sql(consulta, uno=True)
            return resultado[0] > 0 if resultado else False
        except Exception as e:
            print("Error al verificar admin:", e)
            return False

    def solo_existe_default(self):
        """Verifica si solo existe el usuario 'default' en la tabla"""
        try:
            consulta = "SELECT COUNT(*) FROM usuario"
            resultado = self.conexion.ejecutar_sql(consulta, uno=True)
            if resultado and resultado[0] == 1:
                # Verificar si ese único usuario es 'default'
                consulta_nombre = "SELECT nombre FROM usuario"
                resultado_nombre = self.conexion.ejecutar_sql(consulta_nombre, uno=True)
                return resultado_nombre and resultado_nombre[0] == 'default'
            return False
        except Exception as e:
            print("Error al verificar si solo existe default:", e)
            return False

    def login(self, usuario, contrasena):
        """Login y retorna datos del usuario si es exitoso, None si no"""
        if usuario == "default" and contrasena == "00000":
            # Usuario por defecto: solo permitir si no hay usuarios en la tabla
            if not self.hay_usuarios():
                return {
                    'id': 0,
                    'nombre': 'default',
                    'id_rol': 1,
                    'nombre_rol': 'Administrador',
                    'activo': True,
                    'es_primera_vez': True
                }
            else:
                # Hay usuarios admin, no se permite usar default
                return None

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
                    'activo': resultado[4],
                    'es_primera_vez': False
                }
            else:
                return None

        except Exception as e:
            print("Error en login:", e)
            return None