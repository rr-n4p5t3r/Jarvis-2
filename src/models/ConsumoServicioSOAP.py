# Proyecto Jarvis472
# Clase ConsumoServiciosSOAP
# Desarrollado por Ricardo Rosero - n4p5t3r
# Email: rrosero2000@gmail.com
import hashlib
import base64
import random
from datetime import datetime
import requests
from xml.etree import ElementTree as ET
import json

class ConsumoServicioSOAP():
    
    @classmethod
    def soapRegistrarMensaje(self, subdominio, usuario, clave, asunto, texto, nombre_destinatario, correo_destinatario, adjunto, nombre_archivo, alertas, recordatorio, correo_certificado, fecha_vencimiento):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            print(url)
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username></ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:RegistrarMensajeRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:Asunto>{asunto}</seal:Asunto>
                    <seal:Texto>{texto}</seal:Texto>
                    <seal:NombreDestinatario>{nombre_destinatario}</seal:NombreDestinatario>
                    <seal:CorreoDestinatario>{correo_destinatario}</seal:CorreoDestinatario>
                    <seal:Adjunto>{adjunto}</seal:Adjunto>
                    <seal:NombreArchivo>{nombre_archivo}</seal:NombreArchivo>
                    <seal:Alertas>{alertas}</seal:Alertas>
                    <!--Optional:-->
                    <seal:Recordatorio>{recordatorio}</seal:Recordatorio>
                    <!--Optional:-->
                    <seal:CorreoCertificado>{correo_certificado}</seal:CorreoCertificado>
                    <!--Optional:-->
                    <seal:FechaVencimiento>{fecha_vencimiento}</seal:FechaVencimiento>
                </seal:RegistrarMensajeRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            print('soapRegistrarMensaje soap_payload:')
            print(soap_payload)
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            print('soapRegistrarMensaje response:')
            #print(response)            
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_mensaje = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_mensaje
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapObtenerToken(self, subdominio = str, usuario = str, clave = str, idMensaje = int, generarPDF = bool):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:ObtenerTokenRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:idMensaje>{idMensaje}</seal:idMensaje>
                    <seal:generarPDF>{generarPDF}</seal:generarPDF>
                </seal:ObtenerTokenRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Analizar la respuesta XML
            root = ET.fromstring(str(response))
            
            # Encontrar el elemento 'ns1:hash'
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})
            
            # Extraer el valor de 'idMensaje'
            hash_value = hash_element.text.strip()
            id_mensaje = hash_value.split('\n')[0].split('=')[1]
            
            # Extraer los valores de 'Observacion' y 'Token'
            observacion_element = root.find('.//Observacion')  # Reemplazar 'Observacion' con la etiqueta XML real para Observacion
            token_element = root.find('.//Token')  # Reemplazar 'Token' con la etiqueta XML real para Token
            observacion = observacion_element.text.strip() if observacion_element is not None else ""
            token = token_element.text.strip() if token_element is not None else ""
            
            # Crear la respuesta JSON
            response_json = {
                "idMensaje": id_mensaje,
                "Observacion": observacion,
                "Token": token
            }
            
            return json.dumps(response_json)
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapCrearIdentidad(self, subdominio, usuario, clave, nombre_identidad, email_identidad, nombre_grupo, tipo_doc_asociado, documento_asociado, nombre_asociado, apellido_asociado):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:CrearIdentidadRequest>
                    <seal:NombreIdentidad>{nombre_identidad}</seal:NombreIdentidad>
                    <seal:EmailIdentidad>{email_identidad}</seal:EmailIdentidad>
                    <seal:NombreGrupo>{nombre_grupo}</seal:NombreGrupo>
                    <seal:TipoDocAsociado>{tipo_doc_asociado}</seal:TipoDocAsociado>
                    <seal:DocumentoAsociado>{documento_asociado}</seal:DocumentoAsociado>
                    <seal:NombreAsociado>{nombre_asociado}</seal:NombreAsociado>
                    <seal:ApellidoAsociado>{apellido_asociado}</seal:ApellidoAsociado>
                    <seal:idUsuario>{username}</seal:idUsuario>
                </seal:CrearIdentidadRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_estado = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_estado
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapObtenerAdjuntos(self, subdominio = str, usuario = str, clave = str, idMensaje = int):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:ObtenerAdjuntosRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:idMensaje>{idMensaje}</seal:idMensaje>
                </seal:ObtenerAdjuntosRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_mensaje = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_mensaje
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapRegistrarMensajes(self, subdominio = str, usuario = str, clave = str, datos = str):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:RegistrarMensajesRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:datos>{datos}</seal:datos>
                </seal:RegistrarMensajesRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_mensaje = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_mensaje
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapReporteEnvios(self, subdominio = str, usuario = str, clave = str, fecha_desde = str, fecha_hasta = str, asunto =  str):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:ReporteEnviosRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:FechaDesde>{fecha_desde}</seal:FechaDesde>
                    <seal:FechaHasta>{fecha_hasta}</seal:FechaHasta>
                    <!--Optional:-->
                    <seal:Asunto>{asunto}</seal:Asunto>
                </seal:ReporteEnviosRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_mensaje = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_mensaje
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapRegistrarUsuario(self, subdominio = str, usuario = str, clave = str, tipo_documento = int, numero_documento = str, nombres = str, apellidos = str, correo = str, tipo_persona = int, tipo_regimen = int, ciudad = int, direccion = str, telefono = str, no_factura = str, cupo = int):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:RegistrarUsuarioRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:TipoDocumento>{tipo_documento}</seal:TipoDocumento>
                    <seal:NumeroDocumento>{numero_documento}</seal:NumeroDocumento>
                    <seal:Nombres>{nombres}</seal:Nombres>
                    <seal:Apellidos>{apellidos}</seal:Apellidos>
                    <seal:Correo>{correo}</seal:Correo>
                    <seal:TipoPersona>{tipo_persona}</seal:TipoPersona>
                    <seal:TipoRegimen>{tipo_regimen}</seal:TipoRegimen>
                    <seal:Ciudad>{ciudad}</seal:Ciudad>
                    <seal:Direccion>{direccion}</seal:Direccion>
                    <seal:Telefono>{telefono}</seal:Telefono>
                    <seal:NoFactura>{no_factura}</seal:NoFactura>
                    <seal:Cupo>{ciudad}</seal:Cupo>
                </seal:RegistrarUsuarioRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_estado = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_estado
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
            
    @classmethod
    def soapEliminarCupo(self, subdominio = str, usuario = str, clave = str, correo = str, cupo = int):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:EliminarCupoRequest>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:Correo>{correo}</seal:Correo>
                    <seal:Cupo>{cupo}</seal:Cupo>
                </seal:EliminarCupoRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
            # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_estado = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_estado
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)
    
    @classmethod
    def soapGuardadLog(self, subdominio = str, usuario = str, clave = str, fecha_log = datetime, message_log = str, message_id = int):
        try:
            # Datos de autenticación
            url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
            username = usuario
            password = clave
            
            # Payload de la solicitud soap
            soap_payload = '''
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                    <soap:Header>
                        <ns:Security>
                            <ns:UsernameToken>
                                <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                <ns:Password></ns:Password>
                                <ns:Nonce></ns:Nonce>
                                <ns:Created></ns:Created>
                            </ns:UsernameToken>
                        </ns:Security>
                    </soap:Header>
                    <soap:Body>
                        <!-- Add your SOAP request body here -->
                    </soap:Body>
                </soap:Envelope>
                '''
            
            # Generar nonce aleatorio
            nonce = str(random.randint(0, 999999)).encode("utf-8")
            nonce_encoded = base64.b64encode(nonce).decode("utf-8")
            
            # Obtener fecha y hora actual en formato ISO 8601
            created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Calcular digest del password
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
            password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
            password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
            soap_envelope = ET.fromstring(soap_payload)
            
            # Construir la solicitud SOAP
            soap_payload = f'''
            <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security 
                xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                        <wsse:Username>{username}</wsse:Username>
                        <wsse:Password 
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                        {password_digest_encoded}</wsse:Password>
                        <wsse:Nonce 
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                        {nonce_encoded}</wsse:Nonce>
                        <wsu:Created>{created}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <seal:GuardarLogRequest>
                    <seal:datetime>{fecha_log}</seal:datetime>
                    <seal:idUsuario>{username}</seal:idUsuario>
                    <seal:messagelog>{message_log}</seal:messagelog>
                    <seal:messageid>{message_id}</seal:messageid>
                </seal:GuardarLogRequest>
            </soapenv:Body>
            </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
            
            # Convert the modified XML back to string
            signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
            headers = {'Content-Type': 'text/xml'}
            response = requests.post(url, data=soap_payload, headers=headers)
            
           # Parse the XML response
            root = ET.fromstring(str(response))

            # Find the 'ns1:hash' element
            hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

            # Extract the value of 'idMensaje'
            hash_value = hash_element.text.strip()
            id_estado = hash_value.split('\n')[0].split('=')[1]
            
            # Process the response as needed
            return id_estado
        except Exception as e:
            print("Se ejecuta la excepcion: ", e.args)

    @classmethod
    def soapObtenerTokenPasivo(self, subdominio = str, usuario = str, clave = str, idMensaje = int, generarPDF = bool):
            try:
                # Datos de autenticación
                url = 'https://'+subdominio+'.correocertificado4-72.com.co/webService.php?WSDL'
                username = usuario
                password = clave
                
                # Payload de la solicitud soap
                soap_payload = '''
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="namespace_uri">
                        <soap:Header>
                            <ns:Security>
                                <ns:UsernameToken>
                                    <ns:Username>complementogmail@andesscd.com.co</ns:Username>
                                    <ns:Password></ns:Password>
                                    <ns:Nonce></ns:Nonce>
                                    <ns:Created></ns:Created>
                                </ns:UsernameToken>
                            </ns:Security>
                        </soap:Header>
                        <soap:Body>
                            <!-- Add your SOAP request body here -->
                        </soap:Body>
                    </soap:Envelope>
                    '''
                
                # Generar nonce aleatorio
                nonce = str(random.randint(0, 999999)).encode("utf-8")
                nonce_encoded = base64.b64encode(nonce).decode("utf-8")
                
                # Obtener fecha y hora actual en formato ISO 8601
                created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                
                # Calcular digest del password
                sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest()
                password_digest = hashlib.sha1(nonce + created.encode("utf-8") + sha1_hash.encode("utf-8")).digest()
                password_digest_encoded = base64.b64encode(password_digest).decode("utf-8")
                soap_envelope = ET.fromstring(soap_payload)
                
                
                # Construir la solicitud SOAP
                soap_payload = f'''
                <soapenv:Envelope xmlns:seal="http://www.sealmail.co/" 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <wsse:Security 
                    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                        <wsse:UsernameToken wsu:Id="UsernameToken-D1F774731CDF87E67116839894773481">
                            <wsse:Username>{username}</wsse:Username>
                            <wsse:Password 
                            Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">
                            {password_digest_encoded}</wsse:Password>
                            <wsse:Nonce 
                            EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                            {nonce_encoded}</wsse:Nonce>
                            <wsu:Created>{created}</wsu:Created>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <seal:ObtenerTokenRequest>
                        <seal:idUsuario>{username}</seal:idUsuario>
                        <seal:idMensaje>{idMensaje}</seal:idMensaje>
                        <seal:generarPDF>{generarPDF}</seal:generarPDF>
                    </seal:ObtenerTokenRequest>
                </soapenv:Body>
                </soapenv:Envelope>'''.format(username, password_digest_encoded, nonce_encoded, created)
                
                # Convert the modified XML back to string
                signed_soap_payload = ET.tostring(soap_envelope, encoding='utf-8', method='xml')
                headers = {'Content-Type': 'text/xml'}
                response = requests.post(url, data=soap_payload, headers=headers)
                
                root = ET.fromstring(response.text)

                # Find the 'ns1:hash' element
                hash_element = root.find('.//ns1:hash', {'ns1': 'http://www.sealmail.co/'})

                # Extract the value of 'idMensaje'
                hash_value = hash_element.text.strip()
                id_mensaje = hash_value.split('\n')[0].split('=')[1]
                observacion = hash_value.split('\n')[1].split('=')[1]
                token = hash_value.split('\n')[2].split('=')[1].strip()
                
                return {
                    "token": token,
                    "id_mensaje": id_mensaje,
                    "observacion": observacion
                }
            
            except Exception as e:
                print("Se ejecuta la excepcion: ", e.args)