class ReporteEnviosRequest():

    def __init__(self, idUsuario = str, fechaDesde = str, fechaHasta = str, asunto = str) -> None:
        self.idUsuario = idUsuario
        self.fechaDesde = fechaDesde
        self.fechaHasta = fechaHasta
        self.asunto = asunto
    
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'fechaDesde': self.fechaDesde,
            'fechaHasta': self.fechaHasta,
            'asunto': self.asunto
        }