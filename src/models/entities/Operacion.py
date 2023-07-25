from utils.DateFormat import DateFormat
class Operacion():

    def __init__(self,opr_id,fopr_id,opr_idientificadorcliente,opr_idientificadoranddes,opr_correoemisor,opr_creado,opr_actualizado,opr_estado,opr_asunto,opr_correoorganizacion,opr_destinatario):
        self.opr_id=opr_id
        self.fopr_id=fopr_id
        self.opr_idientificadorcliente=opr_idientificadorcliente
        self.opr_idientificadoranddes=opr_idientificadoranddes
        self.opr_correoemisor=opr_correoemisor
        self.opr_creado=opr_creado
        self.opr_actualizado=opr_actualizado
        self.opr_estado=opr_estado
        self.opr_asunto=opr_asunto
        self.opr_correoorganizacion=opr_correoorganizacion
        self.opr_destinatario=opr_destinatario

    def to_JSON(self):
        return {
            'id': self.opr_id,
            'fopr': self.fopr_id,
            'idientificador_cliente': self.opr_idientificadorcliente,
            'idientificador_anddes': self.opr_idientificadoranddes,
            'correoemisor': self.opr_correoemisor,
            'creado': DateFormat.convert_date(self.opr_creado) if self.opr_creado is not None else self.opr_creado,                      
            'actualizado': DateFormat.convert_date(self.opr_actualizado) if self.opr_actualizado is not None else self.opr_actualizado,  
            'estado': self.opr_estado,
            'asunto': self.opr_asunto,
            'correo_organizacion': self.opr_correoorganizacion,
            'destinatario': self.opr_destinatario
        }
    
    
    def to_JSON_pasivo(self):
        import datetime
        return {
            'id': self.opr_id,
            'fopr': self.fopr_id,
            'idientificador_cliente': self.opr_idientificadorcliente,
            'idientificador_anddes': self.opr_idientificadoranddes,
            'correoemisor': self.opr_correoemisor,
            'creado': DateFormat.convert_date(datetime.datetime.strptime(self.opr_creado, '%Y%m%d%H%M')) if self.opr_creado is not None else self.opr_creado,
            'actualizado': DateFormat.convert_date(datetime.datetime.strptime(self.opr_actualizado[:-1], '%H%M')) if self.opr_actualizado is not None else self.opr_actualizado,
            'estado': self.opr_estado,
            'asunto': self.opr_asunto,
            'correo_organizacion': self.opr_correoorganizacion,
            'destinatario': self.opr_destinatario
        }