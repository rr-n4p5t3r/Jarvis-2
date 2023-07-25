class ObtenerAdjuntosRequest():

    def __init__(self, idUsuario = str, idMensaje = str) -> None:
        self.idUsuario = idUsuario
        self.idMensaje = idMensaje
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'idMensaje': self.idMensaje
        }