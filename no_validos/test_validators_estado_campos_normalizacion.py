from data_utils import validators

# ---- Estado bici ----

def test_puede_entrar_correcto():
    serie = "BK001"
    registros = [
        {"timestamp": "2025-03-01 08:15:22", "accion": "IN",  "serie_cuadro": "BK001", "dni_usuario": "12345678A"},
        {"timestamp": "2025-03-01 09:02:10", "accion": "OUT", "serie_cuadro": "BK001", "dni_usuario": "12345678A"},
    ]
    assert validators.puede_entrar(serie, registros) is True

def test_puede_entrar_incorrecto():
    serie = "BK001"
    registros = [{"timestamp": "2025-03-01 09:15:44", "accion": "IN", "serie_cuadro": "BK001", "dni_usuario": "87654321B"}]
    assert validators.puede_entrar(serie, registros) is False

def test_puede_salir_correcto():
    serie = "BK001"
    registros = [{"timestamp": "2025-03-01 09:15:44", "accion": "IN", "serie_cuadro": "BK001", "dni_usuario": "87654321B"}]
    assert validators.puede_salir(serie, registros) is True

def test_puede_salir_incorrecto():
    serie = "BK001"
    registros = [
        {"timestamp": "2025-03-01 08:15:22", "accion": "IN",  "serie_cuadro": "BK001", "dni_usuario": "12345678A"},
        {"timestamp": "2025-03-01 09:02:10", "accion": "OUT", "serie_cuadro": "BK001", "dni_usuario": "12345678A"},
    ]
    assert validators.puede_salir(serie, registros) is False

def test_puede_salir_incorrecto_sin_registros_previos():
    assert validators.puede_salir("BK404", []) is False

# ---- Campos vacíos ----

def test_campo_no_vacio_correcto():
    assert validators.campo_no_vacio("Orbea") is True

def test_campo_no_vacio_vacio():
    assert validators.campo_no_vacio("") is False

def test_campo_no_vacio_espacios():
    assert validators.campo_no_vacio("   ") is False

# ---- Normalización ----

def test_normalizar_texto_espacios():
    assert validators.normalizar_texto(" Ana López ") == "Ana López"

def test_normalizar_email_mayus_minus():
    assert validators.normalizar_email("ANA@EXAMPLE.COM") == "ana@example.com"
