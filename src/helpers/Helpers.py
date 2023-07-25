# Proyecto Jarvis472
# Clase Helpers
# Desarrollado por Ricardo Rosero - n4p5t3r
# Email: rrosero2000@gmail.com
from email.mime.application import MIMEApplication
import string
import xml.etree.ElementTree as ET
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib, ssl
from email import encoders
import base64
import chardet
#from decouple import config
from models.CuentaAutorizadaModel import CuentaAutorizadaModel
from models.ConsumoServicioSOAP import ConsumoServicioSOAP
from models.OperacionModel import OperacionModel
from models.OrganizacionModel import OrganizacionModel
import json
import email.header
import os
import zipfile
from email.header import decode_header
import imaplib
import datetime
from io import BytesIO
import re
class Helpers:
    # Esta funcion genera un archivo XML
    def generar_xml(fechaenvio, asunto, destinatario, fecharecepcion, fechavisualizacion):
        """
        Esta funcion genera un archivo XML

        :param fechaenvio: Fecha de envio del mensaje
        :param asunto: Asunto del mensaje enviado
        :param destinatario: Direccion de correo electronico a quien va dirigido el mensaje
        :param fecharecepcion: Fecha de recibo del mensaje
        :param fechavisualizacion: Fecha en que fue leido el mensaje
        :type fechaenvio: datetime
        :type asunto: str
        :type destinatario: str
        :type fecharecepcion: datetime
        :type fechavisualizacion: datetime
        :raise Exception: Error al generar el archivo XML
        :return: Archivo XML xml_string
        :rtype: str
        """
        try:
            # Crear el elemento raíz del XML
            xml_string = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                        <acuse>
                            <asunto>{asunto}</asunto>
                            <destinatario>{destinatario}</destinatario>
                            <estadoacuse>ENTREGADO</estadoacuse>
                            <estadovisualizacion>Abierto</estadovisualizacion>
                            <fechaenvio>{fechaenvio}</fechaenvio>
                            <fecharecepcion>{fecharecepcion}</fecharecepcion>
                            <fechavisualizacion>{fechavisualizacion}</fechavisualizacion>
                        </acuse>
                        '''
            return xml_string
        except Exception as e:
            print("Error al generar el XML: ", e)
            """Esta excepcion se genera cuando se presenta un error al generar el archivo XML"""
            return None
    
    # Esta funcion envia un mensaje de correo certificado
    def enviar_correo_certificado(xml, organizacion, soap_data):
        """
        Esta funcion envia un correo certificado

        :param xml: Archivo XML generado con anterioridad
        :param organizacion: Objeto Organizacion
        :param soap_data: Objeto SOAP
        :type xml: str
        :type organizacion: object
        :type soap_data: soap_object
        :raise Exception:
        """
        port = 587  # For starttls
        smtp_server = "mail.correocertificado-4-72.com"
        sender_email = "enviocorreocertificado@correocertificado-4-72.com"
        receiver_email = organizacion["opr_correoemisor"]
        password = "3nV10%c0Rr30$c3Rt1F1c4Do&.!"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = organizacion["opr_asunto"]
        
        # Cuerpo del mensaje
        msg.attach(MIMEText(soap_data["observacion"], "plain"))
        
        emisor = organizacion["opr_correoemisor"]
        destinatario = organizacion["opr_destinatario"]
        body = f"""A continuación se adjuntan los archivos de certificación
        Correo emisor: {emisor}
        Correo destinatario: {destinatario}
        """
        msg.attach(MIMEText(body, "plain"))
        xml_file = MIMEText(xml, 'xml')
        xml_file.add_header('Content-Disposition', 'attachment', filename='Certificado.xml')
        msg.attach(xml_file)

        decoded_pdf = soap_data["token"]
        padding = len(decoded_pdf) % 4
        decoded_pdf += "=" * padding
        
        attachment = MIMEApplication(base64.b64decode(decoded_pdf), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=soap_data["observacion"] + ".pdf")
        msg.attach(attachment)
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())


    # Esta funcion obtiene los nombres de los archivos adjuntos en el correo
    def obtener_nombre_adjuntos(correo):
        """
        Esta funcion obtiene el nombre de los archivos adjuntos en un mensaje de correo electronico

        :param correo: Mensaje de correo electronico
        :type correo: email
        :raise Exception:
        :return: Nombre del archivo adjunto
        :rtype: str
        """
        mensaje = email.message_from_string(correo)
        adjuntos = mensaje.get_payload()

        if isinstance(adjuntos, list) and len(adjuntos) > 1:
            return "_adjuntos_sealmail_.zip"
        elif isinstance(adjuntos, list) and len(adjuntos) == 1:
            nombre_adjunto = adjuntos[0].get_filename()
            return nombre_adjunto
        else:
            return ""
    
    # Esta funcion se encarga de buscar el correo autorizado
    def buscar_correo_autorizado(correo):
        """
        Esta funcion obtiene una direccion de correo electronico en la tabla cuentas autorizadas

        :param correo: Mensaje de correo electronico
        :type correo: email
        :raise Exception:
        :return: Direccion de correo electronico existente
        :rtype: Objeto
        """
        cuenta_autorizada_model = CuentaAutorizadaModel()
        # Cargar el JSON de cuentas autorizadas
        json_cuentas_autorizadas = cuenta_autorizada_model.obtener_cuentas_autorizadas()
        #print(json_cuentas_autorizadas)
        lista = json.loads(json_cuentas_autorizadas)
        for objeto in lista:
            if objeto['cat_correoemisor'] == correo:
                return objeto
        return None
    
    # Esta funcion obtiene el cuerpo del mensaje
    def obtener_cuerpo_mensaje(msg):
        """
        Esta funcion obtiene el cuerpo de un mensaje de correo electronico

        :param correo: Mensaje de correo electronico
        :type correo: email
        :raise Exception:
        :return: Nombre del archivo adjunto
        :rtype: str
        """
        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    if part.get_content_charset():
                        cuerpo = part.get_payload(decode=True).decode(part.get_content_charset())
                    else:
                        cuerpo = part.get_payload(decode=True).decode()
                    break
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                if msg.get_content_charset():
                    cuerpo = msg.get_payload(decode=True).decode(msg.get_content_charset())
                else:
                    cuerpo = msg.get_payload(decode=True).decode()
        if cuerpo:
            # Eliminar la firma si está presente
            lineas = cuerpo.split('\n')
            firma_encontrada = False
            cuerpo_filtrado = []

            for linea in lineas:
                if linea.strip() == "--":
                    firma_encontrada = True
                elif firma_encontrada:
                    # Ignorar las líneas posteriores a la firma
                    pass
                else:
                    cuerpo_filtrado.append(linea)
            cuerpo = '\n'.join(cuerpo_filtrado)
        # Eliminar líneas en blanco adicionales al final del cuerpo
        cuerpo = cuerpo.strip()
        
        #return cuerpo_html
        return cuerpo
    
    # La siguiente funcion valida el tamano del cuerpo del mensaje, si el tamano supera el limite permitido retornara false 
    # de lo contrario retornara true
    def validar_tamano_cuerpo(msg, limite_caracteres):
        """
        Esta funcion el tamano cuerpo de un mensaje de correo electronico

        :param msg: Cuerpo del mensaje
        :param limite_caracteres: Limite de caracteres definido por el usuario
        :type msg: email
        :type limite_caracteres: int
        :raise Exception:
        :return: True o False
        :rtype: bool
        """
        cuerpo_del_mensaje = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    cuerpo_del_mensaje = part.get_payload(decode=True).decode()  # Decodificar el contenido si está codificado
        if len(cuerpo_del_mensaje) > limite_caracteres:
            return False
        else:
            return True
        
    # Esta funcion decodifica el asunto del mensaje en un correo electronico
    def decodificar_asunto(msg):
        """
        Esta funcion decodifica el asunto de un mensaje de correo electronico

        :param msg: Asunto del correo electronico
        :type msg: email
        :raise Exception:
        :return: Asunto decodificado
        :rtype: str
        """
        asunto = msg.get('Subject')
        if asunto is not None:
            asunto_decodificado = email.header.decode_header(asunto)
            asunto_plano = ""
            for texto, encoding in asunto_decodificado:
                try:
                    if isinstance(texto, bytes):
                        asunto_plano += texto.decode(encoding or 'utf-8')
                    else:
                        asunto_plano += texto
                except AttributeError:
                    asunto_plano += texto.decode('latin-1')
            return asunto_plano
        return ""

    # Esta funcion se encarga de buscar la identidad de un correo autorizado
    def buscar_identidad_correo_autorizado(correo):
        """
        Esta funcion busca la identidad de una cuenta autorizada a traves de un correo electronico

        :param correo: Correo electronico
        :type correo: str
        :raise Exception:
        :return: Objeto
        :rtype: obj
        """
        cuenta_autorizada_model = CuentaAutorizadaModel()
        # Cargar el JSON de cuentas autorizadas
        json_cuentas_autorizadas = cuenta_autorizada_model.obtener_cuentas_autorizadas()
        #print(json_cuentas_autorizadas)
        lista = json.loads(json_cuentas_autorizadas)
        for objeto in lista:
            if objeto['cat_correoemisor'] == correo:
                return objeto
        return None
    
    # Esta funcion obtiene los archivos adjuntos de un correo electronico
    def obtener_adjuntos(correo):
        """
        Esta funcion obtiene los archivos adjuntos de un mensaje de correo electronico

        :param correo: Mensaje de correo electronico
        :type correo: email
        :raise Exception:
        :return: Listado de archivos adjuntos
        :rtype: obj
        """
        adjuntos = []
        for part in correo.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if not filename:
                continue
            adjuntos.append(part)
        return adjuntos

    # Esta funcion comprime los archivos adjuntos en un unico archivo zip
    #def comprimir_adjuntos(adjuntos, nombre_zip):
        """
        Esta funcion obtiene los archivos adjuntos de un mensaje de correo electronico

        :param adjuntos: Archivos adjuntos de un mensaje de correo electronico
        :param nombre_zip: Nombre por defecto del archivo zip en el cual se van a comprimir todos los archivos adjuntos
        :type adjuntos: objeto
        :type nombre_zip: str
        :raise Exception:
        :return: 
        :rtype: 
        """
        '''
        with zipfile.ZipFile(nombre_zip, 'w') as zipf:
            for adjunto in adjuntos:
                filename = adjunto.get_filename()
                decoded_filename = decode_header(filename)[0][0]
                if isinstance(decoded_filename, bytes):
                    #decoded_filename = decoded_filename.decode()
                    try:
                        decoded_filename = decoded_filename.decode()
                    except UnicodeDecodeError:
                        decoded_filename = decoded_filename.decode('utf-8', 'replace')

                content = adjunto.get_payload(decode=True)
                zipf.writestr(decoded_filename, content)
        '''
    
    def comprimir_adjuntos(adjuntos, nombre_zip):
        with zipfile.ZipFile(nombre_zip, 'w') as zipf:
            for adjunto in adjuntos:
                filename = adjunto.get_filename()
                decoded_filename = decode_header(filename)[0][0]
                if isinstance(decoded_filename, bytes):
                    try:
                        decoded_filename = decoded_filename.decode()
                    except UnicodeDecodeError:
                        decoded_filename = decoded_filename.decode('utf-8', 'replace')

                try:
                    content = adjunto.get_payload(decode=True)
                    if content:
                        zipf.writestr(decoded_filename, content)
                    else:
                        print(f"El archivo adjunto '{decoded_filename}' está vacío.")
                except Exception as e:
                    print(f"Error al comprimir el archivo '{decoded_filename}': {e}")


    # Esta funcion cifra un archivo en base64
    def cifrar_base64(archivo):
        """
        Esta funcion cifra sobre base64 un archivo

        :param archivo: Archivo a cifrar sobre base64
        :type archivo: file
        :raise Exception:
        :return: Archivo cifrado
        :rtype: file (b64encode)
        """
        with open(archivo, 'rb') as file:
            contenido = file.read()
            contenido_cifrado = base64.b64encode(contenido)
        return contenido_cifrado
    
    def generar_diccionario_entidades_html():
        """
        Esta funcion genera un diccionario de entidades html

        :param: ningun parametro recibido
        :type: 
        :raise Exception:
        :return: un diccionario de entidades
        :rtype: 
        """
        diccionario_entidades = {
            "$": "&dollar;", "%": "&percnt;", "^": "&circ;",
            "`": "&grave;", "¢": "&cent;", "£": "&pound;", "¤": "&curren;", "¥": "&yen;", 
            "¦": "&brvbar;", "§": "&sect;", "¨": "&uml;", "©": "&copy;", "ª": "&ordf;", "«": "&laquo;", 
            "¬": "&not;", "®": "&reg;", "¯": "&macr;", "°": "&deg;", "±": "&plusmn;", "²": "&sup2;", 
            "³": "&sup3;", "´": "&acute;", "µ": "&micro;", "¶": "&para;", "·": "&middot;", "¸": "&cedil;", 
            "¹": "&sup1;", "º": "&ordm;", "»": "&raquo;", "¼": "&frac14;", "½": "&frac12;", 
            "¾": "&frac34;", "¿": "&iquest;", "À": "&Agrave;", "Á": "&Aacute;", "Â": "&Acirc;", 
            "Ã": "&Atilde;", "Ä": "&Auml;", "Å": "&Aring;", "Æ": "&AElig;", 
            "Ç": "&Ccedil;", "È": "&Egrave;", "É": "&Eacute;", "Ê": "&Ecirc;", "Ë": "&Euml;", "Ì": "&Igrave;", 
            "Í": "&Iacute;", "Î": "&Icirc;", "Ï": "&Iuml;", "Ð": "&ETH;", "Ñ": "&Ntilde;", "Ò": "&Ograve;", 
            "Ó": "&Oacute;", "Ô": "&Ocirc;", "Õ": "&Otilde;", "Ö": "&Ouml;", "×": "&times;", "Ø": "&Oslash;", 
            "Ù": "&Ugrave;", "Ú": "&Uacute;", "Û": "&Ucirc;", "Ü": "&Uuml;", "Ý": "&Yacute;", "Þ": "&THORN;",
            "ß": "&szlig;", "à": "&agrave;", "á": "&aacute;", "â": "&acirc;", "ã": "&atilde;", "ä": "&auml;", 
            "å": "&aring;", "æ": "&aelig;", "ç": "&ccedil;", "è": "&egrave;", "é": "&eacute;", "ê": "&ecirc;", 
            "ë": "&euml;", "ì": "&igrave;", "í": "&iacute;", "î": "&icirc;", "ï": "&iuml;", "ð": "&eth;",
            "ñ": "&ntilde;", "ò": "&ograve;", "ó": "&oacute;", "ô": "&ocirc;", "õ": "&otilde;", "ö": "&ouml;",
            "÷": "&divide;", "ø": "&oslash;", "ù": "&ugrave;", "ú": "&uacute;", "û": "&ucirc;", "ü": "&uuml;",
            "ý": "&yacute;", "þ": "&thorn;", "ÿ": "&yuml;", "€": "&euro;", "nbsp;":"", "\n":"&#10;", "\r":"&#141;"
        }
        return diccionario_entidades
    
    def encode_base64(text):
        """
        Esta funcion codifica cualquier cadena de texto en base64
        :param: cadena de texto
        :type: str (cualquier codificacion)
        :raise Exception:
        :return: str base64
        :rtype: 
        """
        # Convert the text to bytes.
        bytes_text = bytes(text, "utf-8")

        # Detect the encoding of the text.
        encoding = chardet.detect(bytes_text).get('encoding')

        # Encode the text to base64.
        encoded_text = base64.b64encode(bytes_text).decode(encoding)

        return encoded_text
    
    def base64_encode_html(html_text):
        """
        Esta funcion codifica cualquier cadena de texto en base64
        :param: cadena de texto
        :type: str (cualquier codificacion)
        :raise Exception:
        :return: str base64
        :rtype: 
        """
        # Paso 1: Convertir la cadena a bytes para que chardet pueda trabajar correctamente
        if isinstance(html_text, str):
            html_bytes = html_text.encode()
        else:
            html_bytes = html_text

        # Paso 2: Detectar la codificación del HTML
        result = chardet.detect(html_bytes)
        encoding = result['encoding']

        # Paso 3: Si la detección de codificación falla, usar una codificación predeterminada como 'utf-8'
        if encoding is None:
            encoding = 'utf-8'

        # Paso 4: Codificar el HTML a bytes usando la codificación detectada o predeterminada
        html_bytes = html_text.encode(encoding)

        # Paso 5: Cifrar en Base64
        encoded_html = base64.b64encode(html_bytes).decode()

        return encoded_html

    def encode_images_in_html(html_content):
        # Reemplazar las URLs de las imágenes locales en el HTML con Base64
        def replace_image_urls(match):
            image_path = match.group(1)
            if image_path.startswith("data:image/"):
                return match.group(0)  # La imagen ya está en Base64, no es necesario reemplazarla
            else:
                return f'src="{image_path}"'

        # Patrón para buscar las URLs de las imágenes en el HTML
        img_pattern = r'src="(.*?)"'
        encoded_html = re.sub(img_pattern, replace_image_urls, html_content)

        return encoded_html

    