from utils.DateFormat import DateFormat
class Organizacion():
    
    def __init__(self,org_id,org_nombre,org_puerto,org_creado,org_actualizado,org_dominiodeemicion,org_subdominio,org_usuariosubdominio,org_clave,org_estado,org_nit):
        self.org_id=org_id
        self.org_nombre=org_nombre
        self.org_dominiodeemicion=org_dominiodeemicion
        self.org_subdominio=org_subdominio
        self.org_usuariosubdominio=org_usuariosubdominio
        self.org_clave=org_clave
        self.org_creado=org_creado
        self.org_actualizado=org_actualizado
        self.org_estado=org_estado
        self.org_nit=org_nit
        self.org_puerto=org_puerto
        self.lista_organizaciones = []
    
    #def __init__(self):
    #    self.lista_organizaciones = []  # Inicializar una lista vacía en el constructor de la clase

    def append(self, organizacion):
        self.lista_organizaciones.append(organizacion)  # Utilizar el método append() de la lista interna

    def to_JSON(self):
        return {
            'id': self.org_id,
            'nombre': self.org_nombre,
            'puerto': self.org_puerto,
            'creado': DateFormat.convert_date(self.org_creado) if self.org_creado is not None else self.org_creado,
            'actualizado': DateFormat.convert_date(self.org_actualizado) if self.org_actualizado is not None else self.org_actualizado,
            'dominio_de_emicion': self.org_dominiodeemicion,
            'subdominio': self.org_subdominio,
            'usuario_subdominio': self.org_usuariosubdominio,
            'clave': self.org_clave,            
            'estado': self.org_estado,
            'nit': self.org_nit
        }
    

    def ports_To_JSON(self):
        return {
            'id': self.org_id,
            'nombre': self.org_nombre,
            'puerto': self.org_puerto
        }
    
    def endpoint_to_JSON(self):
        return{
            'subdominio': self.org_subdominio,
            'usuario': self.org_usuariosubdominio,
            'clave': self.org_clave
        }
    
    def id_organizacion_to_JSON(self):
        return{
            'id': self.org_id
        }