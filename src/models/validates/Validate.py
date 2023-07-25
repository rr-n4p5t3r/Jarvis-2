import json
import jsonschema
from jsonschema import validate


class Validate():

    def validateRequest(jsonData):
        # Tipo de Solicitud que se espera
        schema = {
            "type": "object",
            "properties": {
                "idmensaje": {"type": "string"},
                "estado": {"type": "number"},
                "descripcion": {"type": "string"},
                "fecha_evento": {"type": "string"}
            },
            "required":["idmensaje","estado","descripcion"],
            "additionalProperties": False
        }
    
        try:
            validate(instance=jsonData, schema=schema)

        except jsonschema.exceptions.ValidationError as err:
            return False
        return True