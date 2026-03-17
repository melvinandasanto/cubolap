import mssql_python.connection

class ConexionSQLServer:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def conectar(self):
        try:
            connection = mssql_python.connection.Connection(
                server=self.server,
                database=self.database,
                username=self.username,
                password=self.password
            )
            return connection
        except Exception as e:
            print(f"Error al conectar a SQL Server: {e}")
            return None
    
    def cerrar(self, connection):
        try:
            if connection:
                connection.close()
                print("Conexión cerrada correctamente.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    