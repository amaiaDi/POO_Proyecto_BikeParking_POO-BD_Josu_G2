
class Bici:
    def __init__(self,serie_cuadro,dni_usuario,marca,modelo):
        self.modelo = modelo
        self.marca = marca
        self.serie_cuadro = serie_cuadro
        self.dni_usuario = dni_usuario
        
    def to_dict(self) -> dict:
        """
        Convierte el objeto Bici en un diccionario.
        Útil para tests, comparaciones y depuración.
        """
        return {
            "modelo": self.modelo,
            "marca": self.marca,
            "serie_cuadro": self.serie_cuadro,
            "dni_usuario": self.dni_usuario
            }
