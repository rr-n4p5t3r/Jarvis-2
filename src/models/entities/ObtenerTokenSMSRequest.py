class ObtenerTokenSMSRequest():

    def __init__(self, idUsuario = str, idMensaje = int, generarPDF = bool) -> None:
        self.idUsuario = idUsuario
        self.idMensaje = idMensaje
        self.generarPDF = generarPDF

    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'idMensaje': self.idMensaje,
            'generarPDF': self.generarPDF
        }