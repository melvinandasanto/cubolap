"""
Gestor de sesión global para pasar datos entre formularios
"""


class SesionUsuario:
    """Clase para almacenar los datos del usuario actual en sesión"""
    
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SesionUsuario, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        self.id_usuario = None
        self.nombre_usuario = None
        self.id_rol = None
        self.nombre_rol = None
        self.activo = None
    
    def iniciar_sesion(self, id_usuario, nombre_usuario, id_rol, nombre_rol, activo=True):
        """Registra al usuario que inicia sesión"""
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol
        self.activo = activo
    
    def cerrar_sesion(self):
        """Limpia los datos de sesión"""
        self._inicializar()
    
    def es_administrador(self):
        """Verifica si el usuario es administrador"""
        return self.nombre_rol and self.nombre_rol.lower() == "administrador"
    
    def obtener_info_usuario(self):
        """Retorna un diccionario con la info del usuario"""
        return {
            'id': self.id_usuario,
            'nombre': self.nombre_usuario,
            'id_rol': self.id_rol,
            'nombre_rol': self.nombre_rol,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f"SesionUsuario({self.nombre_usuario}, Rol: {self.nombre_rol})"
