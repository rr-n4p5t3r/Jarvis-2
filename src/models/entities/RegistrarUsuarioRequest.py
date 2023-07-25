class RegistrarUsuarioRequest():

    def __init__(self, idUsuario = str, tipoDocumento = int, numeroDocumento = str, nombres = str, apellidos = str, correo = str, tipoPersona = int, tipoRegimen = int, ciudad = int, direccion = str, telefono = str, noFactura = str, cupo =  int) -> None:
        self.idUsuario = idUsuario
        self.tipoDocumento = tipoDocumento
        self.numeroDocumento = numeroDocumento
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.tipoPersona = tipoPersona
        self.tipoRegimen = tipoRegimen
        self.ciudad = ciudad
        self.direccion = direccion
        self.telefono = telefono
        self.noFactura = noFactura
        self.cupo = cupo

    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'tipoDocumento': self.tipoDocumento,
            'numeroDocumento': self.numeroDocumento,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'correo': self.correo,                      
            'tipoPersona': self.tipoPersona,  
            'tipoRegimen': self.tipoRegimen,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'noFactura': self.noFactura,
            'cupo': self.cupo
        }