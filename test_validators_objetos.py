'''
Docstring para tests.test_validators_objetos
Tests para validaciones con listas de objetos (sin SQLite)
'''
from modelo.usuario import Usuario
from modelo.bici import Bici
from modelo.registro import Registro

# Importamos los validadores que trabajan con listas de objetos
from data_utils.validators import (
    es_dni_valido,
    es_email_valido,
    es_dni_unico,
    es_email_unico,
    es_serie_unica,
    existe_usuario,
    existe_bici,
    puede_entrar,
    puede_salir,
    campo_no_vacio,
    normalizar_texto,
    normalizar_email,
)


def test_validadores_dni():
    """Test para validar DNIs correctos e incorrectos"""
    # DNIs válidos
    assert es_dni_valido("12345678Z") is True
    assert es_dni_valido("87654321X") is True
    
    # DNIs inválidos
    assert es_dni_valido("12345678A") is False  # Letra incorrecta
    assert es_dni_valido("1234567Z") is False   # Menos de 8 dígitos
    assert es_dni_valido("123456789Z") is False # Más de 8 dígitos
    assert es_dni_valido("ABCDEFGHZ") is False  # No numérico
    assert es_dni_valido("12345678") is False   # Sin letra


def test_validadores_email():
    """Test para validar emails correctos e incorrectos"""
    # Emails válidos
    assert es_email_valido("ana@ejemplo.com") is True
    assert es_email_valido("usuario.test@dominio.es") is True
    
    # Emails inválidos
    assert es_email_valido("sinArroba.com") is False
    assert es_email_valido("sin@punto") is False
    assert es_email_valido("@ejemplo.com") is False
    assert es_email_valido("usuario@.com") is False


def test_normalizar_email():
    """Test para normalizar y validar emails"""
    # Emails válidos con normalización
    assert normalizar_email("Ana@Ejemplo.COM") is True
    assert normalizar_email("  usuario@dominio.es  ") is True
    
    # Emails inválidos
    assert normalizar_email("sinArroba.com") is False
    assert normalizar_email(None) is False
    assert normalizar_email("") is False


def test_campo_no_vacio():
    """Test para validar campos no vacíos"""
    assert campo_no_vacio("texto") is True
    assert campo_no_vacio("123") is True
    
    assert campo_no_vacio("") is False
    assert campo_no_vacio("   ") is False
    assert campo_no_vacio(None) is False


def test_normalizar_texto():
    """Test para normalizar texto"""
    assert normalizar_texto("Texto Normal") is True
    assert normalizar_texto("  TeXtO  ") is True
    assert normalizar_texto("Ñoño") is True
    
    assert normalizar_texto("") is False
    assert normalizar_texto("   ") is False
    assert normalizar_texto(None) is False


def test_validadores_unicidad_dni():
    """Test para validar unicidad de DNI en listas de objetos"""
    lista_usuarios = []
    
    # Lista vacía: cualquier DNI es único
    assert es_dni_unico("12345678Z", lista_usuarios) is True
    
    # Añadimos un usuario
    lista_usuarios.append(Usuario("12345678Z", "Ana", "ana@ejemplo.com"))
    
    # El mismo DNI ya no es único
    assert es_dni_unico("12345678Z", lista_usuarios) is False
    
    # Un DNI diferente sí es único
    assert es_dni_unico("87654321X", lista_usuarios) is True


def test_validadores_unicidad_email():
    """Test para validar unicidad de email en listas de objetos"""
    lista_usuarios = []
    
    # Lista vacía: cualquier email es único
    assert es_email_unico("ana@ejemplo.com", lista_usuarios) is True
    
    # Añadimos un usuario
    lista_usuarios.append(Usuario("12345678Z", "Ana", "ana@ejemplo.com"))
    
    # El mismo email ya no es único (case-insensitive)
    assert es_email_unico("ana@ejemplo.com", lista_usuarios) is False
    assert es_email_unico("ANA@EJEMPLO.COM", lista_usuarios) is False
    
    # Un email diferente sí es único
    assert es_email_unico("pedro@ejemplo.com", lista_usuarios) is True


def test_validadores_unicidad_serie_bici():
    """Test para validar unicidad de serie de bici en listas de objetos"""
    lista_bicis = []
    
    # Lista vacía: cualquier serie es única
    assert es_serie_unica("BICI001", lista_bicis) is True
    
    # Añadimos una bici
    lista_bicis.append(Bici("BICI001", "12345678Z", "Orbea", "MX40"))
    
    # La misma serie ya no es única
    assert es_serie_unica("BICI001", lista_bicis) is False
    
    # Una serie diferente sí es única
    assert es_serie_unica("BICI002", lista_bicis) is True


def test_validadores_existencia_usuario():
    """Test para validar existencia de usuario en listas de objetos"""
    lista_usuarios = []
    
    # Lista vacía: ningún usuario existe
    assert existe_usuario("12345678Z", lista_usuarios) is False
    
    # Añadimos usuarios
    lista_usuarios.append(Usuario("12345678Z", "Ana", "ana@ejemplo.com"))
    lista_usuarios.append(Usuario("87654321X", "Pedro", "pedro@ejemplo.com"))
    
    # Los usuarios añadidos existen
    assert existe_usuario("12345678Z", lista_usuarios) is True
    assert existe_usuario("87654321X", lista_usuarios) is True
    
    # Un usuario no añadido no existe
    assert existe_usuario("11111111H", lista_usuarios) is False


def test_validadores_existencia_bici():
    """Test para validar existencia de bici en listas de objetos"""
    lista_bicis = []
    
    # Lista vacía: ninguna bici existe
    assert existe_bici("BICI001", lista_bicis) is False
    
    # Añadimos bicis
    lista_bicis.append(Bici("BICI001", "12345678Z", "Orbea", "MX40"))
    lista_bicis.append(Bici("BICI002", "87654321X", "Giant", "Talon"))
    
    # Las bicis añadidas existen
    assert existe_bici("BICI001", lista_bicis) is True
    assert existe_bici("BICI002", lista_bicis) is True
    
    # Una bici no añadida no existe
    assert existe_bici("BICI999", lista_bicis) is False


def test_estado_in_out_puede_entrar():
    """Test para validar si una bici puede entrar según los registros"""
    lista_registros = []
    
    # Sin registros: puede entrar (lista vacía)
    assert puede_entrar("BICI001", lista_registros) is True
    
    # Lista None: puede entrar
    assert puede_entrar("BICI001", None) is True
    
    # Después de un registro IN: NO puede entrar
    lista_registros.append(Registro("2025-12-21T10:00:00", "IN", "BICI001", "12345678Z"))
    assert puede_entrar("BICI001", lista_registros) is False
    
    # Después de un registro OUT: puede entrar
    lista_registros.append(Registro("2025-12-21T11:00:00", "OUT", "BICI001", "12345678Z"))
    assert puede_entrar("BICI001", lista_registros) is True
    
    # Otra bici diferente puede entrar
    assert puede_entrar("BICI002", lista_registros) is True
    
    # Secuencia IN-OUT-IN: NO puede entrar
    lista_registros.append(Registro("2025-12-21T12:00:00", "IN", "BICI001", "12345678Z"))
    assert puede_entrar("BICI001", lista_registros) is False


def test_estado_in_out_puede_salir():
    """Test para validar si una bici puede salir según los registros"""
    lista_registros = []
    
    # Sin registros: NO puede salir (lista vacía)
    assert puede_salir("BICI001", lista_registros) is False
    
    # Lista None: NO puede salir
    assert puede_salir("BICI001", None) is False
    
    # Después de un registro IN: puede salir
    lista_registros.append(Registro("2025-12-21T10:00:00", "IN", "BICI001", "12345678Z"))
    assert puede_salir("BICI001", lista_registros) is True
    
    # Después de un registro OUT: NO puede salir
    lista_registros.append(Registro("2025-12-21T11:00:00", "OUT", "BICI001", "12345678Z"))
    assert puede_salir("BICI001", lista_registros) is False
    
    # Otra bici diferente NO puede salir
    assert puede_salir("BICI002", lista_registros) is False
    
    # Secuencia IN-OUT-IN: puede salir
    lista_registros.append(Registro("2025-12-21T12:00:00", "IN", "BICI001", "12345678Z"))
    assert puede_salir("BICI001", lista_registros) is True


def test_estado_in_out_multiples_bicis():
    """Test para validar el estado de múltiples bicis simultáneamente"""
    lista_registros = []
    
    # BICI001 entra
    lista_registros.append(Registro("2025-12-21T10:00:00", "IN", "BICI001", "12345678Z"))
    
    # BICI002 entra
    lista_registros.append(Registro("2025-12-21T10:30:00", "IN", "BICI002", "87654321X"))
    
    # BICI001 está dentro: NO puede entrar, SÍ puede salir
    assert puede_entrar("BICI001", lista_registros) is False
    assert puede_salir("BICI001", lista_registros) is True
    
    # BICI002 está dentro: NO puede entrar, SÍ puede salir
    assert puede_entrar("BICI002", lista_registros) is False
    assert puede_salir("BICI002", lista_registros) is True
    
    # BICI001 sale
    lista_registros.append(Registro("2025-12-21T11:00:00", "OUT", "BICI001", "12345678Z"))
    
    # BICI001 está fuera: SÍ puede entrar, NO puede salir
    assert puede_entrar("BICI001", lista_registros) is True
    assert puede_salir("BICI001", lista_registros) is False
    
    # BICI002 sigue dentro: NO puede entrar, SÍ puede salir
    assert puede_entrar("BICI002", lista_registros) is False
    assert puede_salir("BICI002", lista_registros) is True
