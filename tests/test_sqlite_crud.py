import sqlite3

#TODO Revisar los imports según la estructura del proyecto
from data_utils.sqlite_utils import (
    insert_usuario,
    insert_bici,
    insert_registro,
    fetch_usuarios,
    fetch_bicis,
    fetch_registros_by_serie,
)
from modelo.usuario import Usuario
from modelo.bici import Bici
from modelo.registro import Registro


def test_crud_insert_y_fetch(conn):
    u = Usuario(dni="12345678A", nombre="Ana", email="ana@ejemplo.com")
    insert_usuario(conn, u)

    b = Bici(serie_cuadro="BICI001", dni_usuario="12345678A", marca="Orbea", modelo="MX40")
    insert_bici(conn, b)

    r = Registro(timestamp="2025-12-21T10:00:00", accion="IN", serie_cuadro="BICI001", dni_usuario="12345678A")
    insert_registro(conn, r)

    usuarios = fetch_usuarios(conn)
    assert len(usuarios) == 1
    assert usuarios[0].dni == "12345678A"
    assert usuarios[0].email == "ana@ejemplo.com"

    bicis = fetch_bicis(conn)
    assert len(bicis) == 1
    assert bicis[0].serie_cuadro == "BICI001"
    assert bicis[0].dni_usuario == "12345678A"

    regs = fetch_registros_by_serie(conn, "BICI001")
    assert len(regs) == 1
    assert regs[0].accion == "IN"
    assert regs[0].serie_cuadro == "BICI001"


def test_restricciones_unicidad(conn):
    insert_usuario(conn, Usuario("12345678A", "Ana", "ana@ejemplo.com"))

    # DNI duplicado
    with pytest.raises(sqlite3.IntegrityError):
        insert_usuario(conn, Usuario("12345678A", "Otra", "otra@ejemplo.com"))

    # Email duplicado
    with pytest.raises(sqlite3.IntegrityError):
        insert_usuario(conn, Usuario("87654321B", "Berta", "ana@ejemplo.com"))

    insert_bici(conn, Bici("BICI001", "12345678A", "Orbea", "MX40"))

    # Serie duplicada
    with pytest.raises(sqlite3.IntegrityError):
        insert_bici(conn, Bici("BICI001", "12345678A", "BH", "X1"))


def test_restriccion_fk_usuario_en_bici(conn):
    # Insert bici con dni_usuario inexistente => FK debe fallar
    with pytest.raises(sqlite3.IntegrityError):
        insert_bici(conn, Bici("BICI999", "00000000Z", "Orbea", "MX40"))
