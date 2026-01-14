
class Usuario:
    def __init__(self,dni,nombre,email):
        self.dni = dni
        self.nombre = nombre
        self.email = email
        
    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario en un diccionario.
        Útil para tests, comparaciones y depuración.
        """
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "email": self.email
        }