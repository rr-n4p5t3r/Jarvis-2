class RegistrarMensajeSMSAdjuntoRequest():

    def __init__(self, idUsuario = str, texto = str, celular = str, flash = bool, certificado = bool, adjuntos = str) -> None:
        self.idUsuario = idUsuario
        self.texto = texto
        self.celular = celular 
        self.flash = flash
        self.certificado = certificado
        self.adjuntos = adjuntos
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'texto': self.texto,
            'celular': self.celular,
            'flash': self.flash,
            'certificado': self.certificado,
            'adjuntos': self.adjuntos
        }