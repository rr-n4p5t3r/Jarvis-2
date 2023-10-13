# Proyecto Jarvis472
# Jarvis Activo
# Desarrollado por Ricardo Rosero - n4p5t3r
# Email: rrosero2000@gmail.com
from hashlib import sha1
import hashlib
import imaplib
import email
import os
from time import sleep
import zipfile
import base64
import json
from email.header import decode_header
from email.utils import getaddresses, parseaddr
#from decouple import config
import requests
from xml.etree import ElementTree as ET
import zipfile 
from database.conexion import conectar
from models.CuentaAutorizadaModel import CuentaAutorizadaModel
from models.ConsumoServicioSOAP import ConsumoServicioSOAP
from models.OperacionModel import OperacionModel
from models.OrganizacionModel import OrganizacionModel
from helpers.Helpers import Helpers
from helpers.sealMail import SealMail
import random
from datetime import datetime
import sys
import re
import chardet
from unidecode import unidecode
import html
from bs4 import BeautifulSoup
import datetime
import email.header
import email.charset
import datetime
import quopri
import re
import codecs
# Aqui inicia el programa
# Conectar con el servidor IMAP
mail = imaplib.IMAP4_SSL("mail.correocertificado-4-72.com")
mail.login("enviocorreocertificado@correocertificado-4-72.com", "3nV10%c0Rr30$c3Rt1F1c4Do&.!")
# conexion al motor
conexion = conectar()
# Crear una instancia de la clase
cuenta_autorizada_model = CuentaAutorizadaModel()
operacion_model = OperacionModel()
organizacion_model = OrganizacionModel()
consumo_soap_model = ConsumoServicioSOAP()
helpers = Helpers()
#print(consumo_soap_model)
# Nombre del archivo ZIP
zip_filename = "_adjuntos_sealmail_.zip" 

# Seleccionar la carpeta de la bandeja de entrada
mail.select('inbox')

# Verificar si la carpeta "procesados" existe
if 'procesados' not in mail.list()[1]:
    # Crear la carpeta "procesados" si no existe
    mail.create('INBOX.procesados')

# Buscar los mensajes sin leer
status, messages = mail.search(None, 'UNSEEN')

if status == 'OK':
    # Obtener los números de los mensajes sin leer
    message_nums = messages[0].split()
    OperacionModel.log(f"Proceso Iniciado: Iniciamos el proceso con {len(message_nums)} mensajes","activo","jarvis2")
    if len(message_nums) > 0:           
        for num in message_nums:
            try:
                # Obtener los datos del mensaje
                status, data = mail.fetch(num, '(RFC822)')
                print(f"status message: {status}")
                if status == 'OK':
                    if isinstance(data[0][1], bytes):
                        msg = email.message_from_bytes(data[0][1])
                    
                        campo_from = msg['From']
                        print("Remitente: ", campo_from)
                        # Obtener únicamente la dirección de correo electrónico en formato de c
                        cadena = campo_from

                        # Patrón para buscar la dirección de correo electrónico
                        pattern = r'[\w\.-]+@[\w\.-]+'

                        # Buscar el patrón en la cadena
                        match = re.search(pattern, cadena)

                        # Extraer la dirección de correo electrónico si se encontró un resultado
                        if match:
                            direccion_correo = match.group()
                        else:
                            OperacionModel.log(f"No se encontró ninguna dirección de correo electrónico en la cadena.","activo","jarvis2")
                        
                        #email_address = parseaddr(campo_from)[1]                    
                        email_address = direccion_correo
                        # Buscar si el remitente es una cuenta autorizada                
                        cuenta = Helpers.buscar_correo_autorizado(email_address)
                        
                        if cuenta is not None:
                            
                            # Si tiene valor correocambiado
                            if cuenta['cat_correocambiado']:
                                cuenta['cat_correoemisor'] = cuenta['cat_correocambiado']                        
                            
                            id = cuenta['cat_id']
                            fopr_id = cuenta['fopr_id']
                            correo_emisor = cuenta['cat_correoemisor']
                            print(correo_emisor)
                            correo_cambiado = cuenta['cat_correocambiado']
                            print(correo_cambiado)
                            estado = cuenta['cat_estado']
                            descripcion = cuenta['cat_descricion']
                            identidad = cuenta['cat_identidad']
                            print(identidad)
                            
                            resultado = organizacion_model.obtener_organizacion_endpoint(fopr_id)
                            print(resultado)
                            
                            org_id = resultado[0]
                            org_subdominio = resultado[1]
                            org_usuariosubdominio = resultado[2]
                            org_clave = resultado[3]
                            print(f"id:{org_id} subdominio:{org_subdominio}, usuario:{org_usuariosubdominio}")
                            # Obtén el valor del asunto del mensaje de correo electrónico
                            subject = msg["Subject"]
                            # Decodifica el asunto utilizando email.header.decode_header()
                            decoded_subject = email.header.decode_header(subject)
                            print(decoded_subject)
                            # Recorre los fragmentos decodificados y reconstruye el asunto
                            decoded_subject_str = ""
                            for fragment, encoding in decoded_subject:
                                if isinstance(fragment, bytes):
                                    charset = email.charset.Charset(encoding)
                                    decoded_fragment = fragment.decode(charset.input_charset, errors="replace")
                                else:
                                    decoded_fragment = str(fragment)
                                decoded_subject_str += decoded_fragment
                            # Imprime el asunto decodificado
                            print("Asunto: ", decoded_subject_str)

                            cifrado_base64_subject = Helpers.encode_base64(decoded_subject_str)
                            
                            # Obtener el cuerpo del mensaje
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    charset = part.get_content_charset()
                                    
                                    if content_type == 'text/plain' or content_type == 'text/html':
                                        payload = part.get_payload(decode=True)

                                        if charset:
                                            body += payload.decode(charset, errors="replace")
                                        else:
                                            body += payload.decode(errors="replace")
                            else:
                                content_type = msg.get_content_type()
                                charset = msg.get_content_charset()

                                if content_type == 'text/plain' or content_type == 'text/html':
                                    payload = msg.get_payload(decode=True)

                                    if charset:
                                        body += payload.decode(charset, errors="replace")
                                    else:
                                        body += payload.decode(errors="replace")
                            # Codificar el contenido del cuerpo del mensaje en Base64
                            encoded_body = Helpers.base64_encode_html(body)
                            cifrado_base64 = encoded_body  
                            

                            # Obtener adjuntos
                            adjuntos = Helpers.obtener_adjuntos(msg)
                            
                            # Comprimir adjuntos en un archivo ZIP
                            nombre_zip = '_adjuntos_sealmail_.zip'
                            Helpers.comprimir_adjuntos(adjuntos, nombre_zip)

                            # Cifrar contenido en base64
                            nombre_archivo_cifrado = '_adjuntos_sealmail_'
                            contenido_cifrado = Helpers.cifrar_base64(nombre_zip)
                            contenido_cifrado_str = contenido_cifrado.decode()
                            
                            # Guardar contenido cifrado en un archivo
                            with open(nombre_archivo_cifrado, 'wb') as file:
                                file.write(contenido_cifrado)
                            
                            # Obtener el tamaño del archivo
                            tamano_archivo = os.path.getsize(nombre_archivo_cifrado)
                            tamano_mb = tamano_archivo / 1048576  # Convertir a megabytes

                            # Formatear el resultado para que sea más legible
                            tamano_mb_formateado = "{:.2f}".format(tamano_mb)  # Redondear a 2 decimales
                            print("Tamaño del archivo: ", tamano_mb_formateado, "MB")
                            
                            if tamano_mb > 20000000:
                                OperacionModel.log(f"Archivo supera el limite permitido: Nombre Archivo: {nombre_archivo_cifrado} | Tamano Archivo: {tamano_mb_formateado} MB | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")    
                            else:
                                OperacionModel.log(f"Información archivo procesado: Nombre Archivo: {nombre_archivo_cifrado} | Tamano Archivo: {tamano_mb_formateado} MB | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")
                                # Verificar si el mensaje tiene destinatarios
                                if 'To' in msg:
                                    print("Verificar destinatarios")
                                    to_recipient = msg.get_all('To', [])
                                    #print(to_recipient, len(to_recipient))
                                    
                                    patron_correo = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'                                
                                    # obtener un [] de los TO en formato de correo electronico             
                                    recipients = re.findall(patron_correo, to_recipient[0]) 
                                    print("Destintarios: ", recipients)
                                    
                                    # Guardar cada destinatario en la base de datos
                                    for recipient in recipients:
                                        # Validar si ya existe registro en la tabla operacion para asunto y destinatario (confirmar Con Luis)
                                        print("==========================================")
                                        print(f"recipient: {recipient}")                          
                                        print("Vamos a consumir el ws")
                                        # Datos de autenticación
                                        url = org_subdominio+'.correocertificado4-72.com.co'
                                        print(url)
                                        username = org_usuariosubdominio
                                        #print(username)
                                        password = org_clave
                                        #print(password)
                                        endPoint = '/webService.php'
                                        print(endPoint)
                                        client = SealMail(username,password,url,endPoint)
                                        print(client)
                                        
                                        if identidad is not None:
                                            # Incluir solo los parametros que van dentro del Body de la peticion Soap
                                            request = f"""
                                            <seal:RegistrarMensajeRequest>
                                            <seal:idUsuario>{identidad}</seal:idUsuario>
                                            <seal:Asunto>{cifrado_base64_subject}</seal:Asunto>
                                            <seal:Texto>{cifrado_base64}</seal:Texto>
                                            <seal:NombreDestinatario>{recipient}</seal:NombreDestinatario>
                                            <seal:CorreoDestinatario>{recipient}</seal:CorreoDestinatario>
                                            <seal:Adjunto>{contenido_cifrado_str}</seal:Adjunto>
                                            <seal:NombreArchivo>{nombre_archivo_cifrado}</seal:NombreArchivo>
                                            <seal:Alertas/>
                                            <!--Optional:-->
                                            <seal:Recordatorio/>
                                            <!--Optional:-->
                                            <seal:CorreoCertificado/>
                                            <!--Optional:-->
                                            <seal:FechaVencimiento/>
                                            </seal:RegistrarMensajeRequest>
                                            """
                                            print("Request: ", request)
                                            OperacionModel.log(f"Realizar peticion con identidad {identidad}","activo","jarvis2")
                                            #OperacionModel.log(f"Peticion del servicio web {request} ","activo","jarvis2")
                                            
                                            # Response WS
                                            response = client.send_soap_request(request)   
                                            #respuesta = "response"                             
                                            print("Response: ", response)
                                            #OperacionModel.log(f"Respuesta del request {response} ","activo","jarvis2")
                                            # Obtener la fecha y hora actual
                                            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                            # Crear el nombre del archivo con la fecha y hora actual
                                            nombre_archivo = f"log_ResponseWS_{fecha_actual}.txt"
                                            # Crear la carpeta de log si no existe
                                            carpeta_log = "log"
                                            if not os.path.exists(carpeta_log):
                                                os.makedirs(carpeta_log)
                                            # Ruta completa del archivo de registro
                                            ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
                                            # Abrir el archivo en modo escritura
                                            archivo = open(ruta_archivo, "a")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Jarvis2 Activo\n")
                                            archivo.write("-----------------") 
                                            archivo.write("\n\n")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Response WS\n")
                                            archivo.write("-----------------") 
                                            archivo.write("\n\n")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Response:\n")
                                            archivo.write(f"{response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                            archivo.write("\n\n")
                                            # Escribir la respuesta en el archivo
                                            archivo.write("Usuario:\n")
                                            archivo.write("Jarvis2")
                                            archivo.write("\n\n")
                                            # Cerrar el archivo
                                            archivo.close()
                                        
                                            #print(response)
                                            id_mensaje_entero = 0
                                            if response:
                                                try:
                                                    # Parsear el XML
                                                    root = ET.fromstring(response)

                                                    # Obtener el elemento "hash" dentro de "ObtenerTokenResponse"
                                                    hash_element = root.find('.//ns1:RegistrarMensajeResponse/ns1:hash', namespaces={'ns1': 'http://www.sealmail.co/'})
                                                    
                                                    # Verificar si se encontró el elemento "hash"
                                                    if hash_element is not None:
                                                        print("Hash Element: ", hash_element)
                                                        # Extract the value of 'idMensaje'
                                                        hash_value = hash_element.text.strip()
                                                        #print("Hash Value: ", hash_value)
                                                        id_mensaje = hash_value.split('\n')[0].split('=')[1]
                                                        id_mensaje_entero = int(id_mensaje) 
                                                        print(id_mensaje_entero)  
                                                    else:
                                                        # Manejar el caso en el que el elemento "hash" no se encontró en el XML
                                                        print("No se encontró el elemento 'hash' en el XML.")
                                                except ET.ParseError as e:
                                                    # Manejar el error de análisis del XML
                                                    print("Error al analizar el XML:", str(e))
                                            else:
                                                # Manejar el caso en el que la respuesta está vacía
                                                print("La respuesta está vacía.")
                                            
                                            request_Token = f"""
                                                <seal:ObtenerTokenRequest>
                                                <seal:idUsuario>{identidad}</seal:idUsuario>
                                                <seal:idMensaje>{id_mensaje_entero}</seal:idMensaje>
                                                <seal:generarPDF>{False}</seal:generarPDF>
                                                </seal:ObtenerTokenRequest>"""

                                            soap_response = client.send_soap_request(request_Token)
                                            root_Token = ET.fromstring(str(soap_response))
                                            
                                            hash_element_token = root_Token.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})
                                            if hash_element_token == None:
                                                raise Exception("Error consumiendo webservice")

                                            hash_value_token = hash_element_token.text.strip()
                                            id_mensaje_token = hash_value_token.split('\n')[0].split('=')[1]
                                            observacion_token = hash_value_token.split('\n')[1].split('=')[1]

                                            token = hash_value_token.split('\n')[2].split('=')[1].strip()
                                            soap_data = {
                                                "token": token,
                                                "id_mensaje": id_mensaje_token,
                                                "observacion": observacion_token
                                            }
                                            
                                            print("SoapData Token: ", soap_data['id_mensaje'])
                                            
                                            OperacionModel.log(f"Estampa de tiempo ObtenerToken: id_Mensaje: {soap_data['id_mensaje']} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")

                                            if soap_data['id_mensaje'] == "0" or soap_data["id_mensaje"] == "1":
                                            #if id_mensaje_entero > 0:
                                                #subject = helpers.decodificar_asunto(msg)
                                                print("Asunto: ", decoded_subject_str)
                                                if '|' in decoded_subject_str:
                                                    identificador_cliente = decoded_subject_str.split('|')[1].strip()
                                                    resultado = operacion_model.verificar_existencia_registro_operaciones(id_mensaje, decoded_subject_str, correo_emisor, recipient)
                                                    #resultado = operacion_model.validar_repetido(id_mensaje)
                                                    if resultado:
                                                        print(f"*****El registro existe en la base de datos.")
                                                        # Obtener la fecha y hora actual
                                                        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                                        OperacionModel.log(f"Registro existente en la base de datos, tabla operaciones id_mensaje:{id_mensaje} {recipient} {decoded_subject_str}","activo","jarvis2")
                                                    else:
                                                        #operacion_model.insertar_registro_operacion(fopr_id, identificador_cliente, id_mensaje, email_address, correo_emisor, subject, org_usuariosubdominio, recipient)
                                                        with  conexion.cursor() as cursor:
                                                            fecha = datetime.datetime.now()
                                                            opr_estado = 1
                                                            print("Insertar en operacion linea 545")
                                                            if correo_cambiado is not None and len(correo_cambiado) > 0:
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 549 ws")
                                                            else:
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 552 ws")
                                                                print("Inserta DB con identificador cliente |")
                                                        conexion.commit()
                                                        #OperacionModel.guardar_operacion(fopr_id, identificador_cliente, id_mensaje, email_address, correo_emisor, subject, org_usuariosubdominio, recipient)
                                                        #OperacionModel.auditoria(f"Insertado en BD id_mensaje:{recipient} {fopr_id} {email_address} {correo_emisor} {decoded_subject_str} {recipient}","activo",org_usuariosubdominio, None)
                                                else:
                                                    resultado = operacion_model.verificar_existencia_registro_operaciones(id_mensaje, decoded_subject_str, correo_emisor, recipient)
                                                    #resultado = operacion_model.validar_repetido(id_mensaje)
                                                    print("Resultado verificar registro: ", resultado)
                                                    if resultado > 0:
                                                        print(f"*****El registro existe en la base de datos.")
                                                        OperacionModel.log(f"Registro existente en la base de datos, tabla operaciones id_mensaje:{id_mensaje} {recipient} {decoded_subject_str}","activo","jarvis2")
                                                    else:
                                                        with  conexion.cursor() as cursor:
                                                            fecha = datetime.datetime.now()
                                                            opr_estado = 1
                                                            print("Insertar en operacion linea 570")
                                                            if correo_cambiado is not None and len(correo_cambiado) > 0:
                                                                identificador_cliente = None
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 572 ws")
                                                            else:
                                                                identificador_cliente = None
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 575 ws")
                                                                
                                                        conexion.commit()
                                                        #OperacionModel.guardar_operacion(fopr_id, None, id_mensaje, email_address, correo_emisor, decoded_subject_str, org_usuariosubdominio, recipient)
                                                        print("Inserta BD else")
                                                # Mover el mensaje a la carpeta "procesados"
                                                mail.copy(num, 'INBOX.procesados')
                                                print("Mensaje movido a la carpeta 'procesados' con éxito")
                                                print(f"***** Correo procesaso id_mensaje: {id_mensaje} {email_address} {username} {decoded_subject_str}")
                                                #OperacionModel.auditoria(f"Movido a procesados id_mensaje:{id_mensaje} {recipient} {decoded_subject_str}", "activo", "jarvis2", None)
                                            #elif id_mensaje_entero == -14:
                                            #    print(f"Mensaje repetido: {response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                            else:
                                                mail.copy(num, 'INBOX.noprocesados')
                                                print("Mensaje movido a la carpeta 'noprocesados' con éxito")
                                                print(f"***** Correo no procesado: {email_address} {username} {decoded_subject_str}")
                                                OperacionModel.log(f"Correo no procesaso: | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")
                                                # Obtener la fecha y hora actual
                                                fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                                # Crear el nombre del archivo con la fecha y hora actual
                                                nombre_archivo = f"log_No_Procesado_{fecha_actual}.txt"
                                                # Crear la carpeta de log si no existe
                                                carpeta_log = "log"
                                                if not os.path.exists(carpeta_log):
                                                    os.makedirs(carpeta_log)
                                                # Ruta completa del archivo de registro
                                                ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
                                                # Abrir el archivo en modo escritura
                                                archivo = open(ruta_archivo, "a")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Jarvis2 Activo\n")
                                                archivo.write("-----------------") 
                                                archivo.write("\n\n")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Log No Procesado\n")
                                                archivo.write("-----------------") 
                                                archivo.write("\n\n")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Registro:\n")
                                                archivo.write(f"{request} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                                archivo.write("\n\n")
                                                archivo.write(f"{response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                                archivo.write("\n\n")
                                                # Escribir la respuesta en el archivo
                                                archivo.write("Usuario:\n")
                                                archivo.write("Jarvis2")
                                                archivo.write("\n\n")
                                                # Cerrar el archivo
                                                archivo.close()
                                        else:
                                            # Incluir solo los parametros que van dentro del Body de la peticion Soap
                                            request = f"""
                                            <seal:RegistrarMensajeRequest>
                                            <seal:idUsuario>{username}</seal:idUsuario>
                                            <seal:Asunto>{cifrado_base64_subject}</seal:Asunto>
                                            <seal:Texto>{cifrado_base64}</seal:Texto>
                                            <seal:NombreDestinatario>{recipient}</seal:NombreDestinatario>
                                            <seal:CorreoDestinatario>{recipient}</seal:CorreoDestinatario>
                                            <seal:Adjunto>{contenido_cifrado_str}</seal:Adjunto>
                                            <seal:NombreArchivo>{nombre_archivo_cifrado}</seal:NombreArchivo>
                                            <seal:Alertas/>
                                            <!--Optional:-->
                                            <seal:Recordatorio/>
                                            <!--Optional:-->
                                            <seal:CorreoCertificado/>
                                            <!--Optional:-->
                                            <seal:FechaVencimiento/>
                                            </seal:RegistrarMensajeRequest>
                                            """
                                            print("Request: ", request)
                                            OperacionModel.log(f"Realizar peticion con usuario {username}","activo","jarvis2")
                                            
                                            #Response
                                            response = client.send_soap_request(request)                                
                                            print("Response: ", response)
                                            # Obtener la fecha y hora actual
                                            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                            # Crear el nombre del archivo con la fecha y hora actual
                                            nombre_archivo = f"log_ResponseWS_{fecha_actual}.txt"
                                            # Crear la carpeta de log si no existe
                                            carpeta_log = "log"
                                            if not os.path.exists(carpeta_log):
                                                os.makedirs(carpeta_log)
                                            # Ruta completa del archivo de registro
                                            ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
                                            # Abrir el archivo en modo escritura
                                            archivo = open(ruta_archivo, "a")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Jarvis2 Activo\n")
                                            archivo.write("-----------------") 
                                            archivo.write("\n\n")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Response WS\n")
                                            archivo.write("-----------------") 
                                            archivo.write("\n\n")
                                            # Escribir la solicitud en el archivo
                                            archivo.write("Response:\n")
                                            archivo.write(f"{response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                            archivo.write("\n\n")
                                            # Escribir la respuesta en el archivo
                                            archivo.write("Usuario:\n")
                                            archivo.write("Jarvis2")
                                            archivo.write("\n\n")
                                            # Cerrar el archivo
                                            archivo.close()
                                            
                                            #print(response)
                                            id_mensaje_entero = 0
                                            if response:
                                                try:
                                                    # Parsear el XML
                                                    root = ET.fromstring(response)
                                                    # Obtener el elemento "hash" dentro de "ObtenerTokenResponse"
                                                    hash_element = root.find('.//ns1:RegistrarMensajeResponse/ns1:hash', namespaces={'ns1': 'http://www.sealmail.co/'})
                                                    # Verificar si se encontró el elemento "hash"
                                                    if hash_element is not None:
                                                        print("Hash Element: ", hash_element)
                                                        # Extract the value of 'idMensaje'
                                                        hash_value = hash_element.text.strip()
                                                        #print("Hash Value: ", hash_value)
                                                        id_mensaje = hash_value.split('\n')[0].split('=')[1]
                                                        id_mensaje_entero = int(id_mensaje)   
                                                        print(id_mensaje_entero)                                      
                                                    else:
                                                        # Manejar el caso en el que el elemento "hash" no se encontró en el XML
                                                        print("No se encontró el elemento 'hash' en el XML.")
                                                except ET.ParseError as e:
                                                    # Manejar el error de análisis del XML
                                                    print("Error al analizar el XML:", str(e))
                                            else:
                                                # Manejar el caso en el que la respuesta está vacía
                                                print("La respuesta está vacía.")
                                            
                                            request_Token = f"""
                                                <seal:ObtenerTokenRequest>
                                                <seal:idUsuario>{username}</seal:idUsuario>
                                                <seal:idMensaje>{id_mensaje_entero}</seal:idMensaje>
                                                <seal:generarPDF>{False}</seal:generarPDF>
                                                </seal:ObtenerTokenRequest>"""

                                            soap_response = client.send_soap_request(request_Token)
                                            root_Token = ET.fromstring(str(soap_response))
                                            
                                            hash_element_token = root_Token.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})
                                            if hash_element_token == None:
                                                raise Exception("Error consumiendo webservice")

                                            hash_value_token = hash_element_token.text.strip()
                                            id_mensaje_token = hash_value_token.split('\n')[0].split('=')[1]
                                            observacion_token = hash_value_token.split('\n')[1].split('=')[1]

                                            token = hash_value_token.split('\n')[2].split('=')[1].strip()
                                            soap_data = {
                                                "token": token,
                                                "id_mensaje": id_mensaje_token,
                                                "observacion": observacion_token
                                            }
                                            
                                            print("SoapData Token: ", soap_data['id_mensaje'])
                                            
                                            OperacionModel.log(f"Estampa de tiempo ObtenerToken: id_Mensaje: {soap_data['id_mensaje']} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")

                                            if soap_data['id_mensaje'] == "0" or soap_data["id_mensaje"] == "1":
                                            #if id_mensaje_entero > 0:
                                                #subject = helpers.decodificar_asunto(msg)
                                                print("Asunto: ", decoded_subject_str)
                                                if '|' in decoded_subject_str:
                                                    identificador_cliente = decoded_subject_str.split('|')[1].strip()
                                                    print("Identificador cliente: ", identificador_cliente)
                                                    resultado = operacion_model.verificar_existencia_registro_operaciones(id_mensaje, decoded_subject_str, correo_emisor, recipient)
                                                    #resultado = operacion_model.validar_repetido(id_mensaje)
                                                    if resultado:
                                                        print(f"*****El registro existe en la base de datos.")
                                                        OperacionModel.log(f"Registro existente en la base de datos, tabla operaciones id_mensaje:{id_mensaje} {recipient} {decoded_subject_str}","activo","jarvis2")
                                                    else:
                                                        with conexion.cursor() as cursor:
                                                            opr_estado = 1
                                                            print("Insertar en operacion linea 767")
                                                            fecha = datetime.datetime.now()
                                                            fecha_actualizado = datetime.datetime.now()
                                                            if correo_cambiado is not None and len(correo_cambiado) > 0:
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 767 ws")
                                                            else:
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 771 ws")
                                                                
                                                        conexion.commit()
                                                        #OperacionModel.guardar_operacion(fopr_id, identificador_cliente, id_mensaje, email_address, correo_emisor, decoded_subject_str, org_usuariosubdominio, recipient)
                                                        print("Inserta DB con identificador cliente |")
                                                else:
                                                    resultado = operacion_model.verificar_existencia_registro_operaciones(id_mensaje, decoded_subject_str, correo_emisor, recipient)
                                                    #resultado = operacion_model.validar_repetido(id_mensaje)
                                                    print("Resultado verificar registro: ", resultado)
                                                    if resultado > 0:
                                                        print(f"*****El registro existe en la base de datos.")
                                                        OperacionModel.log(f"Registro existente en la base de datos, tabla operaciones id_mensaje:{id_mensaje} {recipient} {decoded_subject_str}","activo","jarvis2")
                                                    else:
                                                        with  conexion.cursor() as cursor:
                                                            fecha = datetime.datetime.now()
                                                            opr_estado = 1
                                                            print("Insertar en operacion 791")
                                                            if correo_cambiado is not None and len(correo_cambiado) > 0:
                                                                identificador_cliente = None
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{correo_cambiado}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 791 ws")
                                                            else:
                                                                identificador_cliente = None
                                                                fecha_actualizado = datetime.datetime.now()
                                                                print(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}')")
                                                                cursor.execute(f"INSERT INTO operacion (fopr_id, opr_idientificadorcliente, opr_idientificadoranddes, opr_correoemisor, opr_creado, opr_actualizado,opr_estado, opr_asunto, opr_correoorganizacion, opr_destinatario, opr_peso) VALUES ({fopr_id}, '{identificador_cliente}', '{id_mensaje}', '{email_address}', '{fecha}','{fecha_actualizado}',{opr_estado}, '{decoded_subject_str}','{org_usuariosubdominio}', '{recipient}','{tamano_mb_formateado}');")
                                                                print("Cursor: ", cursor.query)
                                                                print("Inserto con correo cambiado en linea 795 ws")
                                                        
                                                        conexion.commit()
                                                        #OperacionModel.guardar_operacion(fopr_id, None, id_mensaje, email_address, correo_emisor, decoded_subject_str, org_usuariosubdominio, recipient)
                                                        print("Inserta BD else")
                                                # Mover el mensaje a la carpeta "procesados"
                                                mail.copy(num, 'INBOX.procesados')
                                                print("Mensaje movido a la carpeta 'procesados' con éxito")
                                                print(f"***** Correo procesado: {email_address} {username} {decoded_subject_str}")
                                            #elif id_mensaje_entero == -14:
                                            #    print(f"Mensaje Repetido: {response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                            else:
                                                mail.copy(num, 'INBOX.noprocesados')
                                                print("Mensaje movido a la carpeta 'noprocesados' con éxito")
                                                print(f"***** Correo no procesado: {email_address} {username} {decoded_subject_str}")
                                                OperacionModel.log(f"Correo no procesaso: | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}","activo","jarvis2")
                                                # Obtener la fecha y hora actual
                                                fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                                # Crear el nombre del archivo con la fecha y hora actual
                                                nombre_archivo = f"log_No_Procesado{fecha_actual}.txt"
                                                # Crear la carpeta de log si no existe
                                                carpeta_log = "log"
                                                if not os.path.exists(carpeta_log):
                                                    os.makedirs(carpeta_log)
                                                # Ruta completa del archivo de registro
                                                ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
                                                # Abrir el archivo en modo escritura
                                                archivo = open(ruta_archivo, "a")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Jarvis2 Activo\n")
                                                archivo.write("-----------------") 
                                                archivo.write("\n\n")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Log No Procesado\n")
                                                archivo.write("-----------------") 
                                                archivo.write("\n\n")
                                                # Escribir la solicitud en el archivo
                                                archivo.write("Registro:\n")
                                                archivo.write(f"{request} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                                archivo.write("\n\n")
                                                archivo.write(f"{response} | Correo Emisor: {correo_emisor} - Correo Cambiado: {correo_cambiado} - Identidad: {identidad} | Asunto: {decoded_subject_str}")
                                                archivo.write("\n\n")
                                                # Escribir la respuesta en el archivo
                                                archivo.write("Usuario:\n")
                                                archivo.write("Jarvis2")
                                                archivo.write("\n\n")
                                                # Cerrar el archivo
                                                archivo.close()
                                else:
                                    mail.copy(num, 'INBOX.noprocesados')
                                    print("Mensaje movido a la carpeta 'noprocesados' con éxito")
                                    print(f"***** El mensaje no contiene destinatarios")
                                    OperacionModel.log(f"Correo no procesado Email no tiene destinatarios {email_address} | Asunto: {subject}","activo",f"jarvis2")
                        else:
                            mail.copy(num, 'INBOX.noprocesados')
                            print("Mensaje movido a la carpeta 'noprocesados' con éxito")
                            print(f"***** La cuenta no esta autorizada")
                            OperacionModel.log(f"La cuenta no esta autorizada {email_address}","activo",f"jarvis2")
                    else: 
                        mail.copy(num, 'INBOX.noprocesados')
                        print("Mensaje movido a la carpeta 'noprocesados' con éxito")
                        print(f"***** Correo no procesado Email no Autorizado {email_address}")
                        OperacionModel.log(f"Correo no procesado Email no Autorizado {email_address}","activo","jarvis2")
                else:
                    print(f"***** El buzon no tiene mensajes sin leer.")
                    OperacionModel.log(f"El buzon no tiene mensajes sin leer.","activo","jarvis2")
            except requests.exceptions.RequestException as e:
                print(f"Error al procesar el mensaje: {str(e)}")
                OperacionModel.log(f"Error excepcion: {str(e)}", "activo","jarvis2")
            # Borrar los mensajes sin leer de la carpeta actual
            #mail.store(num, '+FLAGS', '\\Deleted')
            #mail.expunge()    
            #continue         
else:
    print("Error al buscar los mensajes sin leer.")
    OperacionModel.log(f"Error al buscar los mensajes sin leer.", "activo","jarvis2")
OperacionModel.log("Proceso Finalizado","activo","jarvis2")
print("======Proceso Finalizado======")
# Cierro todas las conexiones
conexion.close()
mail.close()
mail.logout()