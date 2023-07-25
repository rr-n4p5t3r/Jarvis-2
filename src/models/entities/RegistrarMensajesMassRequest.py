class RegistrarMensajesMassRequest():

    def __init__(self, idUsuario = str, asunto = str, texto = str, nombreDestinatario = str, correoDestinatario = str, adjunto = str, nombreArchivo = str, alertas = bool, recordatorio = int, correoCertificado = bool, fechaVencimiento = str) -> None:
        self.idUsuario = idUsuario
        self.asunto = asunto
        self.texto = texto
        self.nombreDestinatario = nombreDestinatario
        self.correoDestinatario = correoDestinatario
        self.adjunto = adjunto
        self.nombreArchivo = nombreArchivo
        self.alertas = alertas
        self.recordatorio = recordatorio
        self.correoCertificado = correoCertificado
        self.fechaVencimiento = fechaVencimiento

    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'asunto': self.asunto,
            'texto': self.texto,
            'nombreDestinatario': self.nombreDestinatario,
            'correoDestinatario': self.correoDestinatario,
            'adjunto': self.adjunto,                      
            'nombreArchivo': self.nombreArchivo,  
            'alertas': self.alertas,
            'recordatorio': self.recordatorio,
            'correoCertificado': self.correoCertificado,
            'fechaVencimiento': self.fechaVencimiento
        }