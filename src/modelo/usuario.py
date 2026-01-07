
class Usuario:
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