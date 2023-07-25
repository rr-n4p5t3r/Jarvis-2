from flask import Blueprint, jsonify
# Import Models
from models.OperacionModel import OperacionModel
from models.OrganizacionModel import OrganizacionModel

main=Blueprint('api_blueprint',__name__)

@main.route('/organizaciones')
def get_organizaciones():
    try:
        organizaciones = OrganizacionModel.obtener_organizaciones()
        return jsonify(organizaciones)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@main.route('/operaciones')
def get_operaciones():
    try:
        operaciones = OperacionModel.obtener_operaciones()
        return jsonify(operaciones)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
    
@main.route('/puertos')
def get_puertos():
    try:
        organizaciones = OrganizacionModel.obtener_puerto_organizacion()
        return jsonify(organizaciones)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
