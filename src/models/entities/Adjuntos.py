class Adjuntos():

    def __init__(self, adjunto = str, nombreArchivo = str) -> None:
        self.adjunto = adjunto
        self.nombreArchivo = nombreArchivo
    
    def to_JSON(self):
        return {
            'adjunto': self.adjunto,
            'nombreArchivo': self.nombreArchivo
        }