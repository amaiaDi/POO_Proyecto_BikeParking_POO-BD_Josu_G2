'''
Docstring para tests.test_validators_sqlite
'''
#TODO Revisar los imports según la estructura del proyecto
from data_utils.sqlite_utils import (
    insert_usuario,
    insert_bici,
    insert_registro,
    get_ultimo_estado_bici,
)
from modelo.usuario import Usuario
from modelo.bici import Bici
from modelo.registro import Registro

# Ajusta este import al módulo real donde estén tus validadores
from no_validos.test_validators_unicidad_existencia import (
    existe_usuario,
    existe_email,
    existe_bici,
    puede_entrar,
    puede_salir,
)


def test_validadores_unicidad_y_existencia(conn):
    assert not existe_usuario(conn, "12345678A")
    assert not existe_email(conn, "ana@ejemplo.com")

    insert_usuario(conn, Usuario("12345678A", "Ana", "ana@ejemplo.com"))

    assert existe_usuario(conn, "12345678A")
    assert existe_email(conn, "ana@ejemplo.com")

    assert not existe_bici(conn, "BICI001")
    insert_bici(conn, Bici("BICI001", "12345678A", "Orbea", "MX40"))
    assert existe_bici(conn, "BICI001")


def test_estado_in_out_por_ultimo_registro(conn):
    insert_usuario(conn, Usuario("12345678A", "Ana", "ana@ejemplo.com"))
    insert_bici(conn, Bici("BICI001", "12345678A", "Orbea", "MX40"))

    # Sin registros: estado None
    assert get_ultimo_estado_bici(conn, "BICI001") is None

    # Al inicio se permite IN y no se permite OUT
    assert puede_entrar(conn, "BICI001") is True
    assert puede_salir(conn, "BICI001") is False

    # IN
    insert_registro(conn, Registro("2025-12-21T10:00:00", "IN", "BICI001", "12345678A"))
    assert get_ultimo_estado_bici(conn, "BICI001") == "IN"
    assert puede_entrar(conn, "BICI001") is False
    assert puede_salir(conn, "BICI001") is True

    # OUT
    insert_registro(conn, Registro("2025-12-21T11:00:00", "OUT", "BICI001", "12345678A"))
    assert get_ultimo_estado_bici(conn, "BICI001") == "OUT"
    assert puede_entrar(conn, "BICI001") is True
    assert puede_salir(conn, "BICI001") is False
