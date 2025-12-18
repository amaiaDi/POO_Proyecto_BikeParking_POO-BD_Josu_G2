# tests/test_validators_unicidad_existencia.py
from data_utils import validators

# 5.3 Unicidad
def test_email_unico_nuevo():
    usuarios = [{"email": "ana@example.com"}]
    assert validators.es_email_unico("carlos@example.com", usuarios) is True

def test_email_unico_duplicado():
    usuarios = [{"email": "ANA@example.com"}]
    assert validators.es_email_unico("  ana@example.com  ", usuarios) is False  # case-insensitive + strip

def test_dni_unico_nuevo():
    usuarios = [{"dni": "12345678A"}]
    assert validators.es_dni_unico("99999999Z", usuarios) is True

def test_dni_unico_duplicado():
    usuarios = [{"dni": "12345678A"}]
    assert validators.es_dni_unico("12345678A", usuarios) is False

def test_serie_unica_nueva():
    bicis = [{"serie_cuadro": "BK001"}, {"serie_cuadro": "BK002"}]
    assert validators.es_serie_unica("BK003", bicis) is True

def test_serie_unica_duplicada():
    bicis = [{"serie_cuadro": "BK001"}, {"serie_cuadro": "BK002"}]
    assert validators.es_serie_unica("BK001", bicis) is False


# 5.4 Existencia
def test_existe_usuario_si():
    usuarios = [{"dni": "12345678A"}, {"dni": "87654321B"}]
    assert validators.existe_usuario("12345678A", usuarios) is True

def test_existe_usuario_no():
    usuarios = [{"dni": "12345678A"}]
    assert validators.existe_usuario("99999999Z", usuarios) is False

def test_existe_bici_si():
    bicis = [{"serie_cuadro": "BK001"}]
    assert validators.existe_bici("BK001", bicis) is True

def test_existe_bici_no():
    bicis = [{"serie_cuadro": "BK001"}]
    assert validators.existe_bici("BK999", bicis) is False
