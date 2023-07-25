class CrearIdentidadRequest():

    def __init__(self, nombreIdentidad = str, emailIdentidad = str, nombreGrupo = str, tipoDocAsociado = int, documentoAsociado = str, nombreAsociado = str, apellidoAsociado = str, idUsuario = str) -> None:
        self.nombreIdentidad = nombreIdentidad
        self.emailIdentidad = emailIdentidad
        self.nombreGrupo = nombreGrupo
        self.tipoDocAsociado = tipoDocAsociado
        self.documentoAsociado = documentoAsociado
        self.nombreAsociado = nombreAsociado
        self.apellidoAsociado = apellidoAsociado
        self.idUsuario = idUsuario
    
    def to_JSON(self):
        return {
            'nombreIdentidad': self.nombreIdentidad,
            'emailIdentidad': self.emailIdentidad,
            'nombreGrupo': self.nombreGrupo,
            'tipoDocAsociado': self.tipoDocAsociado,
            'documentoAsociado': self.documentoAsociado,
            'nombreAsociado': self.nombreAsociado,
            'apellidoAsociado': self.apellidoAsociado,
            'idUsuario': self.idUsuario
        }