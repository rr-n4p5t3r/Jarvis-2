from utils.DateFormat import DateFormat
class CuentaAutorizada():

    def __init__(self,err_id, err_andesid=None, err_idmensaje=None, err_observacion=None, err_timestamp=None) -> None:
        self.err_id = err_id
        self.err_andesid = err_andesid
        self.err_idmensaje = err_idmensaje
        self.err_observacion = err_observacion
        self.err_timestamp = err_timestamp
        
    def to_JSON(self):
        return {
            'id' : self.err_id,
            'andesid' : self.err_andesid ,
            'idmensaje' : self.err_idmensaje,
            'observacion' : self.err_observacion,
            'timestamp' : DateFormat.convert_date(self.err_timestamp) if self.err_timestamp is not None else self.err_timestamp,
        }
                 
    