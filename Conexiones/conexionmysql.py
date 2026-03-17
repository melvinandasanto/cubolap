import mysql.connector

class ConexionMYSQL:
    def __init__(self, host="localhost", user="root", password="12345", database="examenPython"):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            print("Error al conectar a la base de datos:", err)

    def ejecutar_sql(self, consulta, valores=None):
        try:
            self.conectar()
            self.cursor.execute(consulta, valores)
            self.conexion.commit()
            print("Consulta ejecutada correctamente.")
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta:", err)
        finally:
            self.cerrar()

    def ejecutar_sql(self, consulta, valores=None, uno=False, todos=False):
        try:
            self.conectar()
            self.cursor.execute(consulta, valores)

            if uno:
                resultado = self.cursor.fetchone()
            elif todos:
                resultado = self.cursor.fetchall()
            else:
                self.conexion.commit()
                resultado = True  # ← importante

            return resultado

        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta:", err)
            return None

        finally:
            self.cerrar()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()