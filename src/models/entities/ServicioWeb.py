class ServicioWeb():

    def __init__(self, subdominio = str, usuario = str, clave = str) -> None:
        self.subdominio = subdominio
        self.usuario = usuario
        self.clave = clave
    
    def obtenerSubdominio(self):
        return self.subdominio
    
    def modificaSubdominio(self, subdominio):
        self.subdominio = subdominio
    
    def obtenerUsuario(self):
        return self.usuario
    
    def modificarUsuario(self, usuario):
        self.usuario = usuario
    
    def obtenerClave(self):
        return self.clave
    
    def modificarClave(self, clave):
        self.clave = clave
     
    def to_JSON(self):
        return {
            'subdominio': self.subdominio,
            'usuario': self.usuario,
            'clave': self.clave
        }