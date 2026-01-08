# tests/test_csv_utils.py
import os
import csv
import io
import builtins
import pytest

from data_utils import csv_utils

# --------- helpers ---------
USU_FIELDS = ["dni", "nombre", "email"]
BICI_FIELDS = ["serie_cuadro", "dni_usuario", "marca", "modelo"]
REG_FIELDS  = ["timestamp", "accion", "serie_cuadro", "dni_usuario"]


def test_leer_csv_dic_devuelve_lista_vacia_si_solo_cabecera(tmp_path):
    p = tmp_path / "usuarios.csv"
    p.write_text(",".join(USU_FIELDS) + "\n", encoding="utf-8")
    rows = csv_utils.leer_csv_dic(str(p))
    assert rows == []


def test_escribir_csv_dic_crea_archivo_y_cabecera(tmp_path):
    p = tmp_path / "usuarios.csv"
    data = [{"dni": "12345678A", "nombre": "Ana", "email": "ana@example.com"}]
    csv_utils.escribir_csv_dic(str(p), data, USU_FIELDS)
    text = p.read_text(encoding="utf-8").strip().splitlines()
    assert text[0] == ",".join(USU_FIELDS)
    assert "12345678A,Ana,ana@example.com" in text[1]


def test_escribir_csv_dic_orden_campos_respetado(tmp_path):
    p = tmp_path / "bicis.csv"
    data = [{"marca": "Orbea", "modelo": "Carpe", "dni_usuario": "12345678A", "serie_cuadro": "BK001"}]
    csv_utils.escribir_csv_dic(str(p), data, BICI_FIELDS)
    content = p.read_text(encoding="utf-8").splitlines()
    assert content[0] == ",".join(BICI_FIELDS)
    assert content[1] == "BK001,12345678A,Orbea,Carpe"  # orden correcto


def test_escribir_csv_dic_lista_vacia_mantiene_solo_cabecera(tmp_path):
    p = tmp_path / "registros.csv"
    csv_utils.escribir_csv_dic(str(p), [], REG_FIELDS)
    content = p.read_text(encoding="utf-8").splitlines()
    assert content == [",".join(REG_FIELDS)]


def test_leer_csv_dic_ignora_lineas_con_columnas_incorrectas(tmp_path):
    p = tmp_path / "usuarios.csv"
    # cabecera + una línea correcta + una incorrecta (menos columnas)
    p.write_text("dni,nombre,email\n12345678A,Ana,ana@example.com\n99999999Z,Pepe\n", encoding="utf-8")
    rows = csv_utils.leer_csv_dic(str(p))
    assert rows == [{"dni": "12345678A", "nombre": "Ana", "email": "ana@example.com"}]


def test_asegurar_csvs_crea_archivos_con_cabecera(tmp_path, monkeypatch):
    # Redirigimos las rutas internas del módulo a la carpeta temporal
    usuarios = tmp_path / "usuarios.csv"
    bicis = tmp_path / "bicis.csv"
    regs = tmp_path / "registros.csv"

    monkeypatch.setattr(csv_utils, "USUARIOS_PATH", str(usuarios))
    monkeypatch.setattr(csv_utils, "BICIS_PATH", str(bicis))
    monkeypatch.setattr(csv_utils, "REGISTROS_PATH", str(regs))

    # Ejecutar
    csv_utils.asegurar_csvs()

    # Comprobar existencia y cabeceras
    assert usuarios.exists() and usuarios.read_text(encoding="utf-8").splitlines()[0] == ",".join(USU_FIELDS)
    assert bicis.exists() and bicis.read_text(encoding="utf-8").splitlines()[0] == ",".join(BICI_FIELDS)
    assert regs.exists() and regs.read_text(encoding="utf-8").splitlines()[0] == ",".join(REG_FIELDS)


def test_escrituras_consecutivas_no_duplican_cabeceras(tmp_path):
    p = tmp_path / "usuarios.csv"
    data1 = [{"dni": "12345678A", "nombre": "Ana", "email": "ana@example.com"}]
    data2 = [{"dni": "87654321B", "nombre": "Luis", "email": "luis@example.com"}]

    csv_utils.escribir_csv_dic(str(p), data1, USU_FIELDS)
    csv_utils.escribir_csv_dic(str(p), data2, USU_FIELDS)

    lines = p.read_text(encoding="utf-8").splitlines()
    assert lines[0] == ",".join(USU_FIELDS)
    assert len([l for l in lines if l == ",".join(USU_FIELDS)]) == 1  # solo una cabecera
    assert "12345678A,Ana,ana@example.com" not in lines  # la segunda escritura sobreescribe (según contrato)
    assert "87654321B,Luis,luis@example.com" in lines


def test_codificacion_utf8_y_delimitador_coma(tmp_path):
    p = tmp_path / "usuarios.csv"
    data = [{"dni": "12345678A", "nombre": "Ána López", "email": "ana@example.com"}]
    csv_utils.escribir_csv_dic(str(p), data, USU_FIELDS)

    with open(p, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=",")
        rows = list(reader)
    assert rows[0] == USU_FIELDS
    assert rows[1] == ["12345678A", "Ána López", "ana@example.com"]
