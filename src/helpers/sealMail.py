import http.client
import ssl
import xml.etree.ElementTree as ET
import datetime
import random
import base64
import hashlib
import os

class SealMail:
    def __init__(self, username, password, url,endPoint):
        """
        Esta funcion inicializa la clase SealMail

        :param username: Usuario que va a consumir el servicio web
        :param password: Password del usuario que va a consumir el servicio web
        :param url: URL del enpoint para consumir el servicio web
        :param endpoint: Endpoint para el consumo del servicio
        :type username: str
        :type password: str
        :type url: str
        type endpoint: str
        :raise Exception:
        :return: 
        :rtype: 
        """
        self.username = username
        self.password = password
        self.url = url
        self.endPoint = endPoint

    def generate_nonce(self):
        """
        Esta funcion generar el nonce necesario apra consumir el servicio web de SealMail

        :param: 
        :type:
        :raise Exception:
        :return: Encoded_nonce
        :rtype: b64encode
        """
        simple_nonce = str(random.randint(100000, 999999))        
        encoded_nonce = base64.b64encode(simple_nonce.encode()).decode()
        return encoded_nonce

    def generate_password_digest(self, nonce, created):
        """
        Esta funcion genera el password digest necesario para consumir el servicio web de SealMail

        :param nonce: Nonce generado con anterioridad
        :param created: Fecha actual en la que se consume el servicio web
        :type nonce: str
        :type created: str
        :raise Exception:
        :return: Password_digest
        :rtype: b64encode
        """
        password = hashlib.sha1(self.password.encode()).hexdigest()
        simple_nonce = base64.b64decode(nonce).decode()         
        combined_value = simple_nonce + created + password
        password_digest =  base64.b64encode(hashlib.sha1(combined_value.encode()).digest()).decode()        
        return password_digest

    def generate_security_header(self, nonce, created, password_digest):
        """
        Esta funcion genera la cabecera de seguridad necesaria para consumir el servicio web de SealMail

        :param nonce: Nonce generado con anterioridad
        :param created: Fecha actual en la que se consume el servicio web
        :param password_digest: Password digest generado con anterioridad
        :type nonce: str
        :type created: str
        :type password_digest: str
        :raise Exception:
        :return: Security_xml
        :rtype: Elemnt
        """  
        security = ET.Element('wsse:Security', {'xmlns:wsse': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'})

        username_token = ET.SubElement(security, 'wsse:UsernameToken', {'wsu:Id': 'UsernameToken-3AAFD58E18ED1F5D121683845788752541041'})
        username_element = ET.SubElement(username_token, 'wsse:Username')
        username_element.text = self.username

        password_element = ET.SubElement(username_token, 'wsse:Password', {'Type': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest'})
        password_element.text = password_digest

        nonce_element = ET.SubElement(username_token, 'wsse:Nonce', {'EncodingType': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary'})
        nonce_element.text = nonce

        created_element = ET.SubElement(username_token, 'wsu:Created')
        created_element.text = created

        security.append(username_token)

        security_xml = ET.tostring(security, encoding='utf-8').decode()
        return security_xml

    def send_soap_request(self,request):
        """
        Esta funcion envia la solicitud al servicio web de SealMail

        :param request: Solicitud al servicio web
        :type request: str
        :raise Exception:
        :return: Soap response
        :rtype: soap_response
        """
        tm_created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        encoded_nonce = self.generate_nonce()
        password_digest = self.generate_password_digest(encoded_nonce, tm_created)
        security_header = self.generate_security_header(encoded_nonce, tm_created, password_digest)        
        soap_request = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:seal="http://www.sealmail.co/">
        <soapenv:Header>
            {security_header}
        </soapenv:Header>
        <soapenv:Body>
            {request}
        </soapenv:Body>
        </soapenv:Envelope>
        """.format(security_header=security_header,request=request)
        
        ssl._create_default_https_context = ssl._create_unverified_context
        conn = http.client.HTTPSConnection(self.url)

        headers = {"Content-type": "text/xml"}
        conn.request("POST", self.endPoint, soap_request, headers)
        
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Crear el nombre del archivo con la fecha y hora actual
        nombre_archivo = f"log_SealMail{fecha_actual}.txt"
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
        archivo.write("Seal Mail\n")
        archivo.write("-----------------") 
        archivo.write("\n\n")
        # Escribir la solicitud en el archivo
        archivo.write("XML:\n")
        archivo.write(f"{soap_request}")
        archivo.write("\n\n")
        # Escribir la respuesta en el archivo
        archivo.write("Usuario:\n")
        archivo.write("Jarvis2")
        archivo.write("\n\n")
        # Cerrar el archivo
        archivo.close()
        response = conn.getresponse()
        soap_response = response.read().decode()
        return soap_response
        