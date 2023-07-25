# Proyecto Jarvis472
# Jarvis Pasivo
# Desarrollado por Andrés Tobón
# Email: ziroxdeveloper@outlook.com
from hashlib import sha1
import imaplib
import email
import zipfile
import base64
import json
import os
from smtplib import SMTPResponseException
from email.header import decode_header
from decouple import config
import requests
from xml.etree import ElementTree as ET
import zipfile 
from database.conexion import conectar
from models.CuentaAutorizadaModel import CuentaAutorizadaModel
from models.ConsumoServicioSOAP import ConsumoServicioSOAP
from models.OrganizacionModel import OrganizacionModel
from models.OperacionModel import OperacionModel
from email.utils import getaddresses
from helpers.Helpers import Helpers
from helpers.sealMail import SealMail
from datetime import datetime
import datetime
# Aqui inicia el programa
conexion = conectar()

# Cargar el JSON de correos en estado 1, en la tabla operaciones
organizaciones = OperacionModel.obtener_operaciones_estado_pasivo()

# Acceder a los datos
for organizacion in organizaciones:
    
    try:
        '''
        soap_data = ConsumoServicioSOAP.soapObtenerTokenPasivo(
            organizacion['org_subdominio'],
            organizacion['org_usuariosubdominio'],
            organizacion['org_clave'],
            organizacion['opr_idientificadoranddes'],
            True
        )
        '''
        
        usuario = organizacion['org_usuariosubdominio']
        clave = organizacion['org_clave']
        url = organizacion['org_subdominio'] +'.correocertificado4-72.com.co'
        endpoint = '/webService.php'

        seal = SealMail(usuario, clave, url, endpoint)
        
        request = f"""
            <seal:ObtenerTokenRequest>
            <seal:idUsuario>{usuario}</seal:idUsuario>
            <seal:idMensaje>{organizacion['opr_idientificadoranddes']}</seal:idMensaje>
            <seal:generarPDF>{True}</seal:generarPDF>
            </seal:ObtenerTokenRequest>"""

        soap_response = seal.send_soap_request(request)
        root = ET.fromstring(str(soap_response))
        
        hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})
        if hash_element == None:
            raise Exception("Error consumiendo webservice")

        hash_value = hash_element.text.strip()
        id_mensaje = hash_value.split('\n')[0].split('=')[1]
        observacion = hash_value.split('\n')[1].split('=')[1]

        token = hash_value.split('\n')[2].split('=')[1].strip()
        soap_data = {
            "token": token,
            "id_mensaje": id_mensaje,
            "observacion": observacion
        }

        #OperacionModel.auditoria(f"ObtenerToken id_mensaje={soap_data['id_mensaje']}", "pasivo", f"{organizacion['org_usuariosubdominio']}|{organizacion['opr_idientificadoranddes']}")                      
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Crear el nombre del archivo con la fecha y hora actual
        nombre_archivo = f"log_Pasivo_ObtenerToken_{fecha_actual}.txt"
        # Crear la carpeta de log si no existe
        carpeta_log = "log"
        if not os.path.exists(carpeta_log):
            os.makedirs(carpeta_log)
        # Ruta completa del archivo de registro
        ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
        # Abrir el archivo en modo escritura
        archivo = open(ruta_archivo, "a")
        # Escribir la solicitud en el archivo
        archivo.write("Jarvis2 Pasivo\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("ObntenerToken WS\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("Accion:\n")
        archivo.write(f"ObtenerToken id_mensaje={soap_data['id_mensaje']}" +" pasivo" + f"{organizacion['org_usuariosubdominio']}|{organizacion['opr_idientificadoranddes']}")
        archivo.write("\n\n")
        # Escribir la respuesta en el archivo
        archivo.write("Usuario:\n")
        archivo.write("Jarvis2")
        archivo.write("\n\n")
        # Cerrar el archivo
        archivo.close()
            #print("id mensaje", soap_data['id_mensaje'])
            #Validar si id_mensaje es diferente a 1 
        if soap_data['id_mensaje'] != "1":
            org_name = organizacion["opr_correoorganizacion"]
            id_andes = organizacion['opr_idientificadoranddes']
            soap_data["observacion_time"] = soap_data["observacion"].split("|")[0]
            soap_data["observacion_msg"] = soap_data["observacion"].split("|")[1]


            d = datetime.fromtimestamp(int(soap_data["observacion_time"]))
            formatted_date = d.strftime('%d-%m-%Y %H:%M')
                #print(formatted_date)
                
            xml = Helpers.generar_xml(
                organizacion["opr_creado"].strftime("%d-%m-%Y %H:%M"),
                organizacion["opr_asunto"],
                organizacion["opr_destinatario"],
                formatted_date,
                formatted_date
            )

            Helpers.enviar_correo_certificado(xml, organizacion, soap_data)

            org_name = organizacion["opr_correoorganizacion"]
            id_andes = organizacion['opr_idientificadoranddes']
            correo_emisor = organizacion["opr_correoemisor"]
            #OperacionModel.auditoria(f"Enviar correo a {correo_emisor}", "pasivo", f"{org_name}|{id_andes}")
            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Crear el nombre del archivo con la fecha y hora actual
            nombre_archivo = f"log_Pasivo_EnviarCorreo_{fecha_actual}.txt"
            # Crear la carpeta de log si no existe
            carpeta_log = "log"
            if not os.path.exists(carpeta_log):
                os.makedirs(carpeta_log)
            # Ruta completa del archivo de registro
            ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
            # Abrir el archivo en modo escritura
            archivo = open(ruta_archivo, "a")
            # Escribir la solicitud en el archivo
            archivo.write("Jarvis2 Pasivo\n")
            archivo.write("-----------------") 
            archivo.write("\n\n")
            # Escribir la solicitud en el archivo
            archivo.write("Envio Correo\n")
            archivo.write("-----------------") 
            archivo.write("\n\n")
            # Escribir la solicitud en el archivo
            archivo.write("Accion:\n")
            archivo.write(f"Enviar correo a {correo_emisor}" + "pasivo" + f"{org_name}|{id_andes}")
            archivo.write("\n\n")
            # Escribir la respuesta en el archivo
            archivo.write("Usuario:\n")
            archivo.write("Jarvis2")
            archivo.write("\n\n")
            # Cerrar el archivo
            archivo.close()

            id_estado_operacion = organizacion['opr_id']
            
            OperacionModel.actualizar_opr_estado(id_estado_operacion)

            org_name = organizacion["opr_correoorganizacion"]
            id_andes = organizacion['opr_idientificadoranddes']
            opr_id = organizacion["opr_id"]
            #OperacionModel.auditoria(f"Actualizar opr_estado = 1 de opr_id: {opr_id}", "pasivo", f"{org_name}|{id_andes}")
            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Crear el nombre del archivo con la fecha y hora actual
            nombre_archivo = f"log_Pasivo_ActualizarEstado_{fecha_actual}.txt"
            # Crear la carpeta de log si no existe
            carpeta_log = "log"
            if not os.path.exists(carpeta_log):
                os.makedirs(carpeta_log)
            # Ruta completa del archivo de registro
            ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
            # Abrir el archivo en modo escritura
            archivo = open(ruta_archivo, "a")
            # Escribir la solicitud en el archivo
            archivo.write("Jarvis2 Pasivo\n")
            archivo.write("-----------------") 
            archivo.write("\n\n")
            # Escribir la solicitud en el archivo
            archivo.write("Actualizar Estado\n")
            archivo.write("-----------------") 
            archivo.write("\n\n")
            # Escribir la solicitud en el archivo
            archivo.write("Accion:\n")
            archivo.write(f"Actualizar opr_estado = 1 de opr_id: {opr_id}" + " pasivo" + f"{org_name}|{id_andes}")
            archivo.write("\n\n")
            # Escribir la respuesta en el archivo
            archivo.write("Usuario:\n")
            archivo.write("Jarvis2")
            archivo.write("\n\n")
            # Cerrar el archivo
            archivo.close()
    
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
            # Registrar auditoría con el código de error y mensaje de error SMTP
        org_name = organizacion["opr_correoorganizacion"]
        id_andes = organizacion['opr_idientificadoranddes']
        error_details = f"Código de error SMTP: {error_code}, Mensaje de error SMTP: {error_message}"
        #OperacionModel.auditoria(f"Error al enviar el correo: {error_details}", "pasivo", f"{org_name}|{id_andes}")
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Crear el nombre del archivo con la fecha y hora actual
        nombre_archivo = f"log_Pasivo_Error_EnviarCorreo_{fecha_actual}.txt"
        # Crear la carpeta de log si no existe
        carpeta_log = "log"
        if not os.path.exists(carpeta_log):
            os.makedirs(carpeta_log)
        # Ruta completa del archivo de registro
        ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
        # Abrir el archivo en modo escritura
        archivo = open(ruta_archivo, "a")
        # Escribir la solicitud en el archivo
        archivo.write("Jarvis2 Pasivo\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("Error Enviar Correo\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("Accion:\n")
        archivo.write(f"Error al enviar el correo: {error_details}" + " pasivo" + f"{org_name}|{id_andes}")
        archivo.write("\n\n")
        # Escribir la respuesta en el archivo
        archivo.write("Usuario:\n")
        archivo.write("Jarvis2")
        archivo.write("\n\n")
        # Cerrar el archivo
        archivo.close()

    except Exception as e:
        org_name = organizacion["opr_correoorganizacion"]
        id_andes = organizacion['opr_idientificadoranddes']
        #id_andes = organizacion['opr_idientificadoranddes']
        usuario = organizacion['org_usuariosubdominio']
        #OperacionModel.auditoria(f"Error en el pasivo opr_id = {id_andes} usuario = {usuario}", "pasivo", f"{org_name}|{id_andes}")
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Crear el nombre del archivo con la fecha y hora actual
        nombre_archivo = f"log_Pasivo_Error_{fecha_actual}.txt"
        # Crear la carpeta de log si no existe
        carpeta_log = "log"
        if not os.path.exists(carpeta_log):
            os.makedirs(carpeta_log)
        # Ruta completa del archivo de registro
        ruta_archivo = os.path.join(carpeta_log, nombre_archivo)
        # Abrir el archivo en modo escritura
        archivo = open(ruta_archivo, "a")
        # Escribir la solicitud en el archivo
        archivo.write("Jarvis2 Pasivo\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("Error\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("Accion:\n")
        archivo.write(f"Usuario {usuario} falló al consumir servicio ObtenerToken" + " pasivo" + f" {org_name}|{id_andes}")
        archivo.write("\n" + str(soap_response))
        archivo.write("\n\n")
        # Escribir la respuesta en el archivo
        archivo.write("Usuario:\n")
        archivo.write("Jarvis2")
        archivo.write("\n\n")
        # Cerrar el archivo
        archivo.close()
        

# Cierro todas las conexiones
conexion.close()
