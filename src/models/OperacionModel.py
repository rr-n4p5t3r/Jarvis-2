from database.conexion import conectar
from .entities.Operacion import Operacion
import datetime
import os

class OperacionModel():

    @classmethod
    def obtener_operaciones(self):
        try:
            connection = conectar()
            operaciones = []

            with connection.cursor() as cursor:
                cursor.execute("""SELECT opr_id, fopr_id, opr_idientificadoranddes, opr_idientificadorcliente, opr_correoemisor, opr_creado, opr_actualizado,opr_estado,opr_asunto,opr_correoorganizacion,opr_destinatario 
                    FROM operacion 
                    ORDER BY opr_id DESC 
                    LIMIT 10""")
                resultset = cursor.fetchall()

                for row in resultset:
                    operacion = Operacion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
                    operaciones.append(operacion.to_JSON())

            connection.close()
            return operaciones
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def obtener_email_por_idmensaje_y_organizacion_id(self, idmensaje, organizacion_id):
        try:
            connection=conectar()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT opr_id, fopr_id, opr_idientificadoranddes, opr_idientificadorcliente, opr_correoemisor, opr_creado, opr_actualizado,opr_estado,opr_asunto,opr_correoorganizacion,opr_destinatario
                    FROM operacion 
                    WHERE opr_Idientificadoranddes=%s
                    AND fopr_id=%s""", (idmensaje, organizacion_id))
                row=cursor.fetchone()
                
                operacion=None
                if row !=  None:
                    operacion = Operacion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
                    operacion = operacion.to_JSON()

            connection.close()
            return operacion                
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def insertar_registro_operacion(self, fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, correo_cambiado, opr_asunto, opr_correoorganizacion, opr_destinatario):
        try:
            connection = conectar()
            cursor = connection.cursor()
            print("Insertar en operacion")
            if correo_cambiado is not None and len(correo_cambiado) > 0:
                consulta = """INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, 
                opr_correoemisor, opr_asunto, opr_correoorganizacion, 
                opr_destinatario) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valor1 = fopr_id
                valor2 = opr_idientificadorcliente
                valor3 = opr_idientificadoranddes
                valor4 = correo_cambiado
                valor5 = opr_asunto
                valor6 = opr_correoorganizacion
                valor7 = opr_correoorganizacion
                print(consulta)
                print("Correo guardado: ", valor4)
                # Ejecutar la consulta de inserción con los valores
                cursor.execute(consulta, (valor1, valor2, valor3, valor4, valor5, valor6, valor7))
                print(cursor.query)
                connection.commit()
                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()  
            else:
                consulta = """INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, 
                opr_correoemisor, opr_asunto, opr_correoorganizacion, 
                opr_destinatario) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valor1 = fopr_id
                valor2 = opr_idientificadorcliente
                valor3 = opr_idientificadoranddes
                valor4 = opr_correoemisor
                valor5 = opr_asunto
                valor6 = opr_correoorganizacion
                valor7 = opr_destinatario
                print(consulta)
                print("Correo guardado: ", valor4)
                # Ejecutar la consulta de inserción con los valores
                cursor.execute(consulta, (valor1, valor2, valor3, valor4, valor5, valor6, valor7))
                print(cursor.query)
                connection.commit()
                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()  
                        
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def obtener_operaciones_estado(self):
        try:
            connection = conectar()
            operaciones = []

            with connection.cursor() as cursor:
                cursor.execute("""SELECT opr_id, fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado,opr_asunto,opr_correoorganizacion,opr_destinatario 
                    FROM operacion 
                    WHERE opr_estado = 1 
                    ORDER BY opr_id DESC 
                    LIMIT 10""")
                resultset = cursor.fetchall()

                for row in resultset:
                    operacion = Operacion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
                    operaciones.append(operacion.to_JSON())

            connection.close()
            return operaciones
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def obtener_operaciones_estado_pasivo(self):
        lista_organizaciones = []
        try:
            connection = conectar()
            operaciones = []

            with connection.cursor() as cursor:
                cursor.execute("""SELECT opr_id, fopr_id, org_subdominio,
	                org_usuariosubdominio,
	                org_clave,opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado, opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario
	                FROM operacion inner join organizacion on (fopr_id=org_id)
	                where opr_estado=1;""")
                resultset = cursor.fetchall()

                for row in resultset:
                    lista_organizaciones.append({
                    "opr_id" : row[0],
                    "forp_id" : row[1],
                    "org_subdominio": row[2],
                    "org_usuariosubdominio": row[3],
                    "org_clave": row[4],
                    "opr_idientificadorcliente": row[5],
                    "opr_idientificadoranddes": row[6],
                    "opr_correoemisor" : row[7],
                    "opr_creado" : row[8],
                    "opr_actualizado": row[9],
                    "opr_estado": row[10],
                    "opr_asunto" : row[11],
                    "opr_correoorganizacion" : row[12],
                    "opr_destinatario": row[13]

                })
                
                return lista_organizaciones

            connection.close()
            return operaciones
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_opr_estado(self, identificador):
        try:
            connection = conectar()

            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE operacion SET opr_estado = 0 WHERE opr_id = {identificador}")

            connection.commit()

        except (Exception) as error:
            print("Error actualizando tabla:", error)

        finally:
            connection.close()

    @classmethod
    def auditoria(self, accion, tipo, usuario, bodega=None):
        
        try:
            connection = conectar()

            with connection.cursor() as cursor:
                fecha = datetime.datetime.now()
                print(f"INSERT INTO auditoria2 (fecha, accion, tipo, usuario, bodega) VALUES ({fecha}, {accion}, {tipo}, {usuario}, {bodega});")
                cursor.execute(f"INSERT INTO auditoria2 (fecha, accion, tipo, usuario, bodega) VALUES ({fecha}, {accion}, {tipo}, {usuario}, {bodega});")
                
            connection.commit()
        except (Exception) as error:
            print("Error al insertar en la tabla auditoria:", error.args)
            

        finally:
            connection.close()
        
    #Validar si ya existe registro en la tabla operacion para asunto, destinatario, remitente no entren el mismo dia
    @staticmethod
    def verificar_existencia_registro_operaciones(id_mensaje, asunto, remitente, destinatario):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM operacion
                    WHERE opr_idientificadoranddes = %s AND opr_asunto = %s AND opr_correoemisor = %s AND opr_destinatario = %s""", (id_mensaje, asunto, remitente, destinatario))
                count = cursor.fetchone()[0]
                print("El resultado de count es:", count)
                return count
        finally:
            conexion.close()
            
    @staticmethod
    def validar_repetido(id_mensaje):
        try:
            conexion = conectar()
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM operacion
                    WHERE opr_idientificadoranddes = %s""", (id_mensaje))
                count = cursor.fetchone()[0]
                print("El resultado de count es:", count)
                return count
        finally:
            conexion.close()
    
    
    def guardar_operacion(self, fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, correo_cambiado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_actualizado=None, opr_peso=None):
        try:
            connection = conectar()
            cursor = connection.cursor()
            print("Insertar en operacion")
            fecha = datetime.datetime.now()
            opr_estado = 1
            if correo_cambiado is not None and len(correo_cambiado) > 0:
                consulta = """INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, 
                opr_creado, opr_actualizado, opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, 
                opr_peso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valor1 = fopr_id
                valor2 = opr_idientificadorcliente
                valor3 = opr_idientificadoranddes
                valor4 = correo_cambiado
                valor5 = fecha
                valor6 = opr_actualizado
                valor7 = opr_estado
                valor8 = opr_asunto
                valor9 = opr_correoorganizacion
                valor10 = opr_destinatario
                valor11 = opr_peso
                print(consulta)
                print("Correo guardado: ", valor4)
                # Ejecutar la consulta de inserción con los valores
                cursor.execute(consulta, (valor1, valor2, valor3, valor4, valor5, valor6, valor7, valor8, valor9, valor10, valor11))
                print(cursor.query)
                connection.commit()
                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()  
            else:
                consulta = """INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, 
                opr_creado, opr_actualizado, opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, 
                opr_peso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valor1 = fopr_id
                valor2 = opr_idientificadorcliente
                valor3 = opr_idientificadoranddes
                valor4 = opr_correoemisor
                valor5 = fecha
                valor6 = opr_actualizado
                valor7 = opr_estado
                valor8 = opr_asunto
                valor9 = opr_correoorganizacion
                valor10 = opr_destinatario
                valor11 = opr_peso
                print(consulta)
                print("Correo guardado: ", valor4)
                # Ejecutar la consulta de inserción con los valores
                cursor.execute(consulta, (valor1, valor2, valor3, valor4, valor5, valor6, valor7, valor8, valor9, valor10, valor11))
                print(cursor.query)
                connection.commit()
                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()  
        except (Exception) as error:
            print("Error al insertar en la tabla operacion:", error)

        finally:
            connection.close()
    
    @classmethod
    def log(self, accion, tipo, usuario):
        
        try:
            connection = conectar()

            with connection.cursor() as cursor:
                fecha = datetime.datetime.now()
                print(f"INSERT INTO registro_log (fecha, accion, tipo, usuario) VALUES ('{fecha}', '{accion}', '{tipo}', '{usuario}');")
                cursor.execute(f"INSERT INTO registro_log (fecha, accion, tipo, usuario) VALUES ('{fecha}', '{accion}', '{tipo}', '{usuario}');")
                connection.commit()
                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()  
        except (Exception) as error:
            print("Error al insertar en la tabla log:", error.args)
        finally:
            connection.close()