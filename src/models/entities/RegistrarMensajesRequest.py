class RegistrarMensajesRequest():

    def __init__(self, idUsuario = str, datos = str) -> None:
        self.idUsuario = idUsuario
        self.datos = datos
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'datos': self.datos,
        }