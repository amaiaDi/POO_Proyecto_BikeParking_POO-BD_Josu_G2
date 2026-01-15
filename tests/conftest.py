'''
Docstring para tests.conftest 
Si existe un fichero tests/conftest.py, pytest lo ejecuta antes de 
cualquier test y pone disponibles sus fixtures en todos los ficheros de test que estén en ese árbol de carpetas.
'''
from pathlib import Path

import pytest

import sqlite3
from src.data_utils.sqlite_utils import get_connection

#TODO Revisar los imports según la estructura del proyecto
from data_utils.sqlite_utils import init_db


@pytest.fixture()
def conn(tmp_path, monkeypatch):
    """
    Crea un entorno aislado para tests:
    - Copia el schema.sql real del proyecto
    - Crea una BD SQLite vacía (fichero)
    - Ejecuta init_db(conn)
    - Devuelve una conexión lista para usar
    """
    project_root = Path(__file__).resolve().parents[1]  # carpeta raíz del repo
    schema_src = project_root / "data" / "schema.sql"
    if not schema_src.exists():
        raise FileNotFoundError(
            "No existe data/schema.sql en el proyecto. "
            "Debes incluirlo en el repo para poder ejecutar tests."
        )

    # Crear estructura data/ en el entorno temporal de tests
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Copiar schema.sql real a tmp_path/data/schema.sql
    schema_dst = data_dir / "schema.sql"
    schema_dst.write_text(schema_src.read_text(encoding="utf-8"), encoding="utf-8")

    # Cambiar CWD para que init_db lea "data/schema.sql"
    monkeypatch.chdir(tmp_path)

    # Crear BD temporal de test
    db_path = data_dir / "bike_parking_test.db"
    connection = get_connection(str(db_path))
    try:
        init_db(connection)
        yield connection
    finally:
        connection.close()
