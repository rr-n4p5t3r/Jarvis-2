class RegistrarMensajeSMSRequest():

    def __init__(self, idUsuario = str, texto = str, celular = str, flash = bool, certificado = bool, adjunto = str, nombreArchivo = str) -> None:
        self.idUsuario = idUsuario
        self.texto = texto
        self.celular = celular 
        self.flash = flash
        self.certificado = certificado
        self.adjunto = adjunto
        self.nombreArchivo = nombreArchivo
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'texto': self.texto,
            'celular': self.celular,
            'flash': self.flash,
            'certificado': self.certificado,
            'adjunto': self.adjunto,
            'nombreArchivo': self.nombreArchivo
        }