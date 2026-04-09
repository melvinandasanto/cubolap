import claseconectar


class Usuario:
    def __init__(self, idusuario=None, nombre=None, contrasenia=None, idrol=None, activo=None):
        self.idusuario = idusuario
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.idrol = idrol
        self.activo = activo

    @property
    def IdUsuario(self):
        return self.idusuario

    @IdUsuario.setter
    def IdUsuario(self, idusuario):
        self.idusuario = idusuario

    @property
    def Nombre(self):
        return self.nombre

    @Nombre.setter
    def Nombre(self, nombre):
        self.nombre = nombre

    @property
    def Contrasenia(self):
        return self.contrasenia

    @Contrasenia.setter
    def Contrasenia(self, contrasenia):
        self.contrasenia = contrasenia

    @property
    def IdRol(self):
        return self.idrol

    @IdRol.setter
    def IdRol(self, idrol):
        self.idrol = idrol

    @property
    def Activo(self):
        return self.activo

    @Activo.setter
    def Activo(self, activo):
        self.activo = activo

    def Guardar(self):
        conexion = claseconectar.Conectar()
        return conexion.ejecutar_sql(
            "INSERT INTO usuario (nombre, contrasenia, idrol, activo) VALUES (?, ?, ?, ?)",
            (self.nombre, self.contrasenia, self.idrol, self.activo)
        )

    def Eliminar(self, idusuario):
        conexion = claseconectar.Conectar()
        return conexion.ejecutar_sql(
            "DELETE FROM usuario WHERE idusuario = ?",
            (idusuario,)
        )

    def Buscar(self, idusuario):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT idusuario, nombre, contrasenia, idrol, activo FROM usuario WHERE idusuario = ?",
            (idusuario,),
            uno=True
        )

        if resultado:
            self.idusuario = resultado[0]
            self.nombre = resultado[1]
            self.contrasenia = resultado[2]
            self.idrol = resultado[3]
            self.activo = resultado[4]
            return True
        return False

    def Editar(self):
        conexion = claseconectar.Conectar()
        return conexion.ejecutar_sql(
            "UPDATE usuario SET nombre = ?, contrasenia = ?, idrol = ?, activo = ? WHERE idusuario = ?",
            (self.nombre, self.contrasenia, self.idrol, self.activo, self.idusuario)
        )

    def Listar(self):
        conexion = claseconectar.Conectar()
        return conexion.ejecutar_sql("""
            SELECT u.idusuario, u.nombre, r.idrol, r.nombrerol, u.activo
            FROM usuario u
            LEFT JOIN rol r ON u.idrol = r.idrol
            ORDER BY u.idusuario
        """)

    def ObtenerNombreRol(self, idrol):
        conexion = claseconectar.Conectar()
        resultado = conexion.ejecutar_sql(
            "SELECT nombrerol FROM rol WHERE idrol = ?",
            (idrol,),
            uno=True
        )
        if resultado:
            return resultado[0]
        return "Sin rol"