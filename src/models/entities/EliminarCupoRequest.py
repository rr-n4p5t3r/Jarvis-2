class EliminarCupoRequest():

    def __init__(self, datetime = int, idUsuario = str, correo = str, cupo = int) -> None:
        self.datetime = datetime
        self.idUsuario = idUsuario
        self.correo = correo
        self.cupo = cupo
    
    def to_JSON(self):
        return {
            'datetime': self.datetime,
            'idUsuario': self.idUsuario,
            'correo': self.correo,
            'cupo': self.cupo
        }