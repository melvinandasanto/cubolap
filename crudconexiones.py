from claseconectar import ClaseConexiones

class CrudConexiones:
    def __init__(self, idconexion=None, nombreconexion=None, gestor=None, host=None, puerto=None, usuario=None, contrasenia=None, basedatos=None):
        self.conexion = ClaseConexiones()
        self._idconexion = idconexion
        self._nombreconexion = nombreconexion
        self._gestor = gestor
        self._host = host
        self._puerto = puerto
        self._usuario = usuario
        self._contrasenia = contrasenia
        self._basedatos = basedatos

    @property
    def idconexion(self):
        return self._idconexion
    @idconexion.setter
    def idconexion(self, value):
        self._idconexion = value
    @property
    def nombreconexion(self):
        return self._nombreconexion
    @nombreconexion.setter
    def nombreconexion(self, value):
        self._nombreconexion = value
    @property
    def gestor(self):
        return self._gestor
    @gestor.setter
    def gestor(self, value):
        self._gestor = value
    @property
    def host(self):
        return self._host
    @host.setter
    def host(self, value):
        self._host = value
    @property
    def puerto(self):
        return self._puerto
    @puerto.setter
    def puerto(self, value):
        self._puerto = value
    @property
    def usuario(self):
        return self._usuario
    @usuario.setter
    def usuario(self, value):
        self._usuario = value
    @property
    def contrasenia(self):
        return self._contrasenia
    @contrasenia.setter
    def contrasenia(self, value):
        self._contrasenia = value
    @property
    def basedatos(self):
        return self._basedatos
    @basedatos.setter
    def basedatos(self, value):
        self._basedatos = value

    def Guardar(self):
        conexion = ClaseConexiones()
        conexion.ejecutar_sql(
            "INSERT INTO CONEXIONES (nombreconexion, gestor, host, puerto, usuario, contrasenia, basedatos) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (self.nombreconexion, self.gestor, self.host, self.puerto, self.usuario, self.contrasenia, self.basedatos)
        )
        print("Conexion guardada en la base de datos")

    def Eliminar(self, producto_id):
            print(f"Eliminando conexion de la base de datos")
            conexion = ClaseConexiones()
            conexion.ejecutar_sql(
                "DELETE FROM CONEXIONES WHERE idconexion = %s",
                (producto_id,)
            )
    
    def Editar(self, producto_id):
        print(f"Editando conexion con ID {producto_id} en la base de datos...")
        conexion = ClaseConexiones()
        conexion.ejecutar_sql(
            "UPDATE CONEXIONES SET nombreconexion = %s, gestor = %s, host = %s, puerto = %s, usuario = %s, contrasenia = %s, basedatos = %s WHERE idconexion = %s",
            (self.nombreconexion, self.gestor, self.host, self.puerto, self.usuario, self.contrasenia, self.basedatos, producto_id)
        )
            
    def Buscar(self, productos_id):
        conexion = ClaseConexiones()
        resultado = conexion.ejecutar_sql(
            "SELECT idconexion, nombreconexion, gestor, host, puerto, usuario, contrasenia, basedatos "
            "FROM CONEXIONES WHERE idconexion = %s",
            (productos_id,), uno=True
        )

        if resultado:
            self.idconexion = resultado[0]
            self.nombreconexion = resultado[1]
            self.gestor = resultado[2]
            self.host = resultado[3]
            self.puerto = resultado[4]
            self.usuario = resultado[5]
            self.contrasenia = resultado[6]
            self.basedatos = resultado[7]
            return True
        else:
            return False
        
    def probarconexion(self):
        conexion = ClaseConexiones()
        try:
            conn = conexion.conectar(
                self.host, self.puerto, self.usuario, self.contrasenia, self.basedatos, self.gestor
            )
            conn.close()
            print("Conexión exitosa")
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
