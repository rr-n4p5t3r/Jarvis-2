from database.conexion import conectar
from .entities.Organizacion import Organizacion
import json
class OrganizacionModel():

    @classmethod
    def obtener_organizaciones(self):
        try:
            connection = conectar()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT org_id, org_nombre, org_puerto, org_creado, org_actualizado, org_dominiodeemicion, org_subdominio, org_usuariosubdominio, org_clave, org_estado, org_nit
                                FROM organizacion 
                                ORDER BY org_nombre 
                                LIMIT 10""")
                resultset = cursor.fetchall()

                json_list = []  # Lista para almacenar los objetos JSON

                for row in resultset:
                    json_data = json.dumps(row)  # Convierte la fila a cadena JSON
                    json_list.append(json_data)  # Agrega el objeto JSON a la lista

                connection.close()

                json_result = json.dumps(json_list)  # JSON resultante
                return json_result
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def obtener_puerto_organizacion(self):
        try:
            connection = conectar()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT org_id, org_nombre, org_puerto, org_creado, org_actualizado 
                                FROM organizacion 
                                WHERE org_puerto IS NOT NULL 
                                ORDER BY org_puerto""")
                resultset = cursor.fetchall()

                json_list = []  # Lista para almacenar los objetos JSON

                for row in resultset:
                    json_data = json.dumps(row)  # Convierte la fila a cadena JSON
                    json_list.append(json_data)  # Agrega el objeto JSON a la lista

                connection.close()

                json_result = json.dumps(json_list)  # JSON resultante
                return json_result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_organizacion_id_por_puerto(self, puerto):
        try:
            connection = conectar()
            with connection.cursor() as cursor:
                cursor.execute("SELECT org_id FROM organizacion WHERE org_puerto = %s", [puerto])
                row = cursor.fetchone()

                connection.close()
                return row[0] if row is not None else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_organizacion_endpoint(self, id_organizacion):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT org_id, org_subdominio, org_usuariosubdominio, org_clave FROM organizacion WHERE org_id = %s", [id_organizacion])
                resultset = cursor.fetchone()
                
                # Cerrar la conexión después de obtener el resultado
                conexion.close()

                return resultset  # Devolver el resultado directamente
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def obtener_id_organizacion_email(cls, email_emisor):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("""SELECT o.org_id 
                               FROM organizacion o, cuentasautorizadas c 
                               WHERE c.fopr_id = o.org_id AND c.cat_correoemisor = %s""", [email_emisor])
                row = cursor.fetchone()  # Obtener la primera fila del resultado

                conexion.close()

                if row:
                    id_organizacion = row[0]
                    return id_organizacion
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)