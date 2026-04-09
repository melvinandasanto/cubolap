import claseconectar


class Rol:
    def __init__(self, idrol=None, nombrerol=None):
        self.idrol = idrol
        self.nombrerol = nombrerol
        self.ultimo_error = None

    @property
    def IdRol(self):
        return self.idrol

    @IdRol.setter
    def IdRol(self, value):
        self.idrol = value

    @property
    def NombreRol(self):
        return self.nombrerol

    @NombreRol.setter
    def NombreRol(self, value):
        self.nombrerol = value

    def Guardar(self):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "INSERT INTO rol (nombrerol) VALUES (?)",
            (self.nombrerol,)
        )
        self.ultimo_error = conexion.ultimo_error
        return resultado

    def Editar(self):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "UPDATE rol SET nombrerol = ? WHERE idrol = ?",
            (self.nombrerol, self.idrol)
        )
        self.ultimo_error = conexion.ultimo_error
        return resultado

    def Eliminar(self, idrol):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "DELETE FROM rol WHERE idrol = ?",
            (idrol,)
        )
        self.ultimo_error = conexion.ultimo_error
        return resultado

    def Buscar(self, idrol):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT idrol, nombrerol FROM rol WHERE idrol = ?",
            (idrol,),
            uno=True
        )
        self.ultimo_error = conexion.ultimo_error

        if resultado:
            self.idrol = resultado[0]
            self.nombrerol = resultado[1]
            return True
        return False

    def Listar(self):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT idrol, nombrerol FROM rol ORDER BY idrol"
        )
        self.ultimo_error = conexion.ultimo_error
        return resultado if resultado else []

    def AsignarRolAUsuario(self, idusuario, idrol):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "UPDATE usuario SET idrol = ? WHERE idusuario = ?",
            (idrol, idusuario)
        )
        self.ultimo_error = conexion.ultimo_error
        return resultado

    def CrearRolesPredeterminados(self):
        roles_predeterminados = [
            "Administrador",
            "Supervisor",
            "Analista",
            "Aseadora",
            "Cajero"
        ]

        conexion = claseconectar.Conectar()
        existentes = conexion.ejecutar_sql("SELECT nombrerol FROM rol")
        self.ultimo_error = conexion.ultimo_error

        nombres_existentes = set()

        if existentes:
            for fila in existentes:
                nombres_existentes.add(str(fila[0]).strip().lower())

        for nombre in roles_predeterminados:
            if nombre.lower() not in nombres_existentes:
                conexion_insert = claseconectar.Conectar()
                resultado = conexion_insert.ejecutar_sql(
                    "INSERT INTO rol (nombrerol) VALUES (?)",
                    (nombre,)
                )
                self.ultimo_error = conexion_insert.ultimo_error

                if not resultado and self.ultimo_error:
                    print("Error al crear rol predeterminado:", self.ultimo_error)