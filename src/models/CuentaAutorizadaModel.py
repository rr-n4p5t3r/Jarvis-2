from database.conexion import conectar
from .entities.CuentaAutorizada import CuentaAutorizada
import json
from datetime import datetime

class CuentaAutorizadaModel():
    @classmethod
    def obtener_cuentas_autorizadas(cls):
        try:
            connection = conectar()
            cuentas_autorizadas = []
            with connection.cursor() as cursor:
                cursor.execute("""SELECT cat_id, fopr_id, cat_correoemisor, cat_correocambiado, cat_estado, cat_descricion, cat_identidad 
                                FROM cuentasautorizadas 
                                ORDER BY cat_id DESC""")
                resultset = cursor.fetchall()
                for row in resultset:
                    cuenta_autorizada = {
                        'cat_id': row[0],
                        'fopr_id': row[1],
                        'cat_correoemisor': row[2],
                        'cat_correocambiado': row[3],
                        'cat_estado': row[4],
                        'cat_descricion': row[5],
                        'cat_identidad': row[6]
                    }
                    cuentas_autorizadas.append(cuenta_autorizada)
            connection.close()
            # Convertir la lista de diccionarios a una cadena JSON
            json_data = json.dumps(cuentas_autorizadas, default=str)  # Utilizar str como función de serialización por defecto
            return json_data
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def obtener_cuentas_autorizadas_correo_cambiado(self, email_usuario):
        try:
            connection = conectar()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT cat_correocambiado
                    FROM cuentasautorizadas
                    WHERE cat_correoemisor = %s
                """, (email_usuario,))
                resultset = cursor.fetchall()

            connection.close()

            cuentas_autorizadas = [{'cat_correocambiado': row[0]} for row in resultset]
            result_string = '\n'.join([row['cat_correocambiado'] for row in cuentas_autorizadas])

            return result_string
        except Exception as ex:
            raise Exception(ex)