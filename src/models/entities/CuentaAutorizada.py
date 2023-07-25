from utils.DateFormat import DateFormat
class CuentaAutorizada():
    def __init__(self,cat_id,fopr_id=None, cat_correoemisor=None, cat_correocambiado=None, cat_creado=None, cat_actualizado=None, cat_estado=None, cat_descripcion=None) -> None:
        self.cat_id = cat_id
        self.fopr_id = fopr_id
        self.cat_correoemisor = cat_correoemisor
        self.cat_correocambiado = cat_correocambiado
        self.cat_creado = cat_creado
        self.cat_actualizado = cat_actualizado
        self.cat_estado = cat_estado
        self.cat_descripcion = cat_descripcion
        

    def to_JSON(self):
        return {
            'id': self.cat_id,
            'fopr_id': self.fopr_id,
            'correoemisor': self.cat_correoemisor,
            'correocambiado': self.cat_correocambiado,
            'creado': DateFormat.convert_date(self.cat_creado) if self.cat_creado is not None else self.cat_creado,
            'actualizado': DateFormat.convert_date(self.cat_actualizado) if self.cat_actualizado is not None else self.cat_actualizado,
            'estado': self.cat_estado,
            'descripcion': self.cat_descripcion
        }
    
        