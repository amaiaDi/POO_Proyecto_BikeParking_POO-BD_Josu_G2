from __future__ import annotations

import sqlite3

from modelo.usuario import Usuario
from modelo.bici import Bici
from modelo.registro import Registro



def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Abre una conexión a la base de datos SQLite y
    devuelve filas como diccionarios (sqlite3.Row).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Crea las tablas ejecutando el fichero schema.sql.
    """
    cursor = conn.cursor()

    with open("data/schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()


def existe_dni(conn: sqlite3.Connection, dni: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM usuarios WHERE dni = ? LIMIT 1",
        (dni,)
    )
    return cursor.fetchone() is not None


def existe_email(conn: sqlite3.Connection, email: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM usuarios WHERE email = ? LIMIT 1",
        (email,)
    )
    return cursor.fetchone() is not None


def existe_usuario(conn: sqlite3.Connection, dni: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM usuarios WHERE dni = ? LIMIT 1",
        (dni,)
    )
    return cursor.fetchone() is not None


def existe_bici(conn: sqlite3.Connection, serie: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM bicis WHERE serie_cuadro = ? LIMIT 1",
        (serie,)
    )
    return cursor.fetchone() is not None


def insert_usuario(conn: sqlite3.Connection, usuario: Usuario) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO usuarios (dni, nombre, email)
        VALUES (?, ?, ?)
        """,
        (usuario.dni, usuario.nombre, usuario.email)
    )
    conn.commit()


def delete_usuario(conn: sqlite3.Connection, dni: str) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM usuarios WHERE dni = ?",
        (dni,)
    )
    conn.commit()


def insert_bici(conn: sqlite3.Connection, bici: Bici) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bicis (serie_cuadro, dni_usuario, marca, modelo)
        VALUES (?, ?, ?, ?)
        """,
        (bici.serie_cuadro, bici.dni_usuario, bici.marca, bici.modelo)
    )
    conn.commit()


def delete_bici(conn: sqlite3.Connection, serie: str) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM bicis WHERE serie_cuadro = ?",
        (serie,)
    )
    conn.commit()


def insert_registro(conn: sqlite3.Connection, registro: Registro) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO registros (timestamp, accion, serie_cuadro, dni_usuario)
        VALUES (?, ?, ?, ?)
        """,
        (
            registro.timestamp,
            registro.accion,
            registro.serie_cuadro,
            registro.dni_usuario
        )
    )
    conn.commit()



def leer_usuarios(conn: sqlite3.Connection) -> list[Usuario]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT dni, nombre, email FROM usuarios"
    )
    rows = cursor.fetchall()
    return [Usuario.from_row(row) for row in rows]


def leer_bicis(conn: sqlite3.Connection) -> list[Bici]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT serie_cuadro, dni_usuario, marca, modelo FROM bicis"
    )
    rows = cursor.fetchall()
    return [Bici.from_row(row) for row in rows]


def leer_registros_by_serie(
    conn: sqlite3.Connection,
    serie: str
) -> list[Registro]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, timestamp, accion, serie_cuadro, dni_usuario
        FROM registros
        WHERE serie_cuadro = ?
        ORDER BY timestamp ASC
        """,
        (serie,)
    )
    rows = cursor.fetchall()
    return [Registro.from_row(row) for row in rows]




def get_ultimo_estado_bici(
    conn: sqlite3.Connection,
    serie: str
) -> str | None:
    """
    Devuelve:
    - 'IN'  si el último registro es IN
    - 'OUT' si el último registro es OUT
    - None  si la bici no tiene registros
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT accion
        FROM registros
        WHERE serie_cuadro = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (serie,)
    )
    row = cursor.fetchone()

    if row is None:
        return None

    return row["accion"]


