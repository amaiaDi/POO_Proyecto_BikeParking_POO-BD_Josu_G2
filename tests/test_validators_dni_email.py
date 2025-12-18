# tests/test_validators_dni_email.py
from data_utils import validators

# 5.1 DNI: es_dni_valido
def test_dni_valido_correcto():
    assert validators.es_dni_valido("12345678A") is True

def test_dni_valido_letra_minuscula():
    assert validators.es_dni_valido("12345678a") is True

def test_dni_valido_invalido_formato():
    assert validators.es_dni_valido("1234A") is False

def test_dni_valido_sin_letra():
    assert validators.es_dni_valido("12345678") is False

def test_dni_valido_con_simbolos():
    assert validators.es_dni_valido("1234-567A") is False


# 5.2 Email: es_email_valido
def test_email_valido_correcto():
    assert validators.es_email_valido("ana@example.com") is True

def test_email_valido_sin_arroba():
    assert validators.es_email_valido("anaexample.com") is False

def test_email_valido_sin_dominio():
    assert validators.es_email_valido("ana@") is False

def test_email_valido_vacio():
    assert validators.es_email_valido("") is False
