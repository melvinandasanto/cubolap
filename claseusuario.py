import claseconectar

class Usuario: 
    def __init__(self, idusuario=None, nombre=None, apellido=None, contrasenia=None, idrol=None, activo=None):
        self.idusuario = idusuario
        self.nombre = nombre
        self.apellido = apellido
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
    def Apellido(self):
        return self.apellido
    @Apellido.setter
    def Apellido(self, apellido):
        self.apellido = apellido
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
        conexion = claseconectar.Conexion()
        conexion.ejecutar_sql(
            "INSERT INTO usuarios (nombre, apellido, contrasenia, idrol, activo) VALUES (%s, %s, %s, %s, %s)",
            (self.nombre, self.apellido, self.contrasenia, self.idrol, self.activo)
        )
        print("Guardado el usuario en la base de datos...")

    def Eliminar(self, idusuario):
        print(f"Eliminando usuario con ID {idusuario} de la base de datos...")
        conexion = claseconectar.Conexion()
        conexion.ejecutar_sql(
            "DELETE FROM usuarios WHERE idusuario = %s",
            (idusuario,)
        )
    
    def Buscar(self, idusuario):
        conexion = claseconectar.Conexion()
        resultado = conexion.ejecutar_sql(
            "SELECT idusuario, nombre, apellido, contrasenia, idrol, activo FROM usuarios WHERE idusuario = %s",
            (idusuario,), uno=True
        )
        if resultado:
            self.idusuario = resultado[0]
            self.nombre = resultado[1]
            self.apellido = resultado[2]
            self.contrasenia = resultado[3]
            self.idrol = resultado[4]
            self.activo = resultado[5]
    
    def Editar(self):
        conexion = claseconectar.Conexion()
        conexion.ejecutar_sql(
            "UPDATE usuarios SET nombre = %s, apellido = %s, contrasenia = %s, idrol = %s, activo = %s WHERE idusuario = %s",
            (self.nombre, self.apellido, self.contrasenia, self.idrol, self.activo, self.idusuario)
        )
        print(f"Usuario con ID {self.idusuario} actualizado en la base de datos...")