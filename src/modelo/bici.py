def to_dict(self) -> dict:
    """
        Convierte el objeto Usuario en un diccionario.
        Útil para tests, comparaciones y depuración.
        """
    return {
        "modelo": self.modelo,
        "marca": self.marca,
        "serie_cuadro": self.serie_cuadro,
        "dni_usuario": self.dni_usuario
        }
