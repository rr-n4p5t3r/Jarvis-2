from flask import Blueprint, jsonify
# Import Models
from models.OperacionModel import OperacionModel

main=Blueprint('api_operacion_blueprint',__name__)

@main.route('/')
def get_operaciones():
    try:
        operaciones = OperacionModel.obtener_operaciones()
        return jsonify(operaciones)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500