from flask import Blueprint, jsonify, request
# Entities
from models.entities.Operacion import Operacion
# Import Models
from models.OperacionModel import OperacionModel
from models.OrganizacionModel import OrganizacionModel
# Validates
from models.validates.Validate import Validate
# Enums
from enums.FieldsName import FieldsName

from urllib.parse import urlparse

main=Blueprint('api_blueprint',__name__)

@main.route('/estado', methods=['POST'])
def actualizacion():
    operacion=None
    try:
        # Obtenr el puerto de la paticion
        parts_url = urlparse(request.url)
        port = parts_url.port
        history_response = request.json
        # Validar la estructura de la peticion desde Anddes
        if Validate.validateRequest(request.json):
            history_response[FieldsName.ESTADO.value] = 1
            #Obtener id de la organizacion por el puerto de la peticion
            organizacion_id = OrganizacionModel.obtener_organizacion_id_por_puerto(port)
            if organizacion_id == None:
                response = {
                    "ok": False,
                    "msg": "[500] Se ha presentado un error inesperado!",
                    "history": history_response
                }
                return jsonify(response), 500
            idmensaje = request.json['idmensaje']
            # Validar si existe el correo en la tabla operacion            
            operacion=OperacionModel.obtener_email_por_idmensaje_y_organizacion_id(idmensaje, organizacion_id)
            # Si no se encuentra el email se reponde un mensaje de error 400
            if operacion == None:
                # Si No existe el email se reponde un mensaje con codigo 400
                response = {
                    "ok": False,
                    "msg": "[400] No existe el Email que estas buscando!",
                    "history": history_response
                }
                return jsonify(response), 400
            # TODO llamar al funcion que lanza el llamdoa Anddes los datos del email estan operacion
            # Si existe el email se reponde un mensaje con codgio 200
            response = {
                "ok": True,
                "msg": "[200] Se creo Correctamente!",
                "history": history_response
            }
            return jsonify(response), 200
        else:
            # Sino se cumple con la estructura desde Anddes se retorna error 500
            history_response[FieldsName.ESTADO.value] = 1
            response = {
                "ok": False,
                "msg": "[500] Se ha presentado un error inesperado!",
                "history": history_response
            }
            return jsonify(response), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

