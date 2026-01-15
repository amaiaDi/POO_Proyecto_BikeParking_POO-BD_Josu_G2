
def test_schema_crea_tablas(conn):
    """
    Verifica que, tras ejecutar init_db(conn), existen las tablas principales
    definidas en data/schema.sql.

    Se consulta sqlite_master para comprobar la creación real en SQLite.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)
    tables = {row["name"] for row in cur.fetchall()}

    assert "usuarios" in tables
    assert "bicis" in tables
    assert "registros" in tables


def test_schema_crea_indices(conn):
    """
    Verifica que existen los índices definidos en data/schema.sql.
    (Si cambian nombres en el schema, este test debe actualizarse.)
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='index'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    indexes = {row["name"] for row in cur.fetchall()}

    assert "idx_registros_serie_timestamp" in indexes
    assert "idx_bicis_dni_usuario" in indexes
