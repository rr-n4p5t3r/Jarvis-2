class EstadoServicioRequest():

    def __init__(self, idUsuario = str) -> None:
        self.idUsuario = idUsuario
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario
        }