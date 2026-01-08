
class Registro:
    def to_dict(self) -> dict:
        """
        Convierte el objeto Registro en un diccionario.
        Útil para tests, comparaciones y depuración.
        """
        return {
            "timestamp": self.timestamp,
            "accion": self.accion,
            "serie_cuadro": self.serie_cuadro,
            "dni_usuario": self.dni_usuario
        }
