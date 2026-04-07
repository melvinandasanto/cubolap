from claseconectar import Conectar


class ClaseConexiones:
    def __init__(self, idconexion=None, gestor=None, host=None, puerto=None,
                 usuario=None, contrasenia=None, basedatos=None):
        self.conexion = Conectar()
        self._idconexion = idconexion
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
        conexion = Conectar()
        return conexion.ejecutar_sql(
            """
            INSERT INTO CONEXIONES (gestor, host, puerto, usuario, contrasenia, basedatos)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (self.gestor, self.host, self.puerto, self.usuario,
             self.contrasenia, self.basedatos)
        )

    def Eliminar(self, conexion_id):
        conexion = Conectar()
        return conexion.ejecutar_sql(
            "DELETE FROM CONEXIONES WHERE idconexion = ?",
            (conexion_id,)
        )

    def Editar(self, conexion_id):
        conexion = Conectar()
        return conexion.ejecutar_sql(
            """
            UPDATE CONEXIONES
            SET gestor = ?, host = ?, puerto = ?, usuario = ?, contrasenia = ?, basedatos = ? 
            WHERE idconexion = ?
            """,
            (self.gestor, self.host, self.puerto, self.usuario,
             self.contrasenia, self.basedatos, conexion_id)
        )

    def Buscar(self, idconexion):
        conexion = Conectar()
        resultado = conexion.ejecutar_sql("""
            SELECT idconexion, gestor, host, puerto, usuario,
                   contrasenia, basedatos
            FROM conexiones
            WHERE idconexion = ?
        """, (idconexion,), uno=True)

        if resultado:
            self.idconexion = resultado[0]
            self.gestor = resultado[1]
            self.host = resultado[2]
            self.puerto = resultado[3]
            self.usuario = resultado[4]
            self.contrasenia = resultado[5]
            self.basedatos = resultado[6]
            return True

        return False

    def Listar(self):
        conexion = Conectar()
        return conexion.ejecutar_sql(
            """
            SELECT idconexion, gestor, host, puerto, usuario, contrasenia, basedatos
            FROM CONEXIONES
            ORDER BY idconexion DESC
            """
        )

    def probarconexion(self):
        conexion = Conectar()
        conn = None
        try:
            conn = conexion.conectar(
                self.gestor,
                self.host,
                self.basedatos,
                self.usuario,
                self.contrasenia,
                self.puerto
            )
            return conn is not None
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass