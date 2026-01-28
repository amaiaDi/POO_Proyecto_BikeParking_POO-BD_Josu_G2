
import re
import sqlite3

def es_dni_valido(pdni: str):
    """"
    Función que comprueba que el dni es correcto

    args: pdni (str): dni a comprobar

    returns: bool
    """
    return validar_dni(pdni)

def es_email_valido(pemail: str) -> bool:
    
    """"
    Función que comprueba que el email es correcto

    args: pemail (str): email a comprobar

    returns: bool
    """

    if not isinstance(pemail, str):
        return False

    if pemail.count("@") != 1:
        return False

    parte_local, dominio = pemail.split("@")

    if not parte_local:
        return False

    if "." not in dominio:
        return False

    nombre_dominio, extension = dominio.rsplit(".", 1)

    if not nombre_dominio or not extension:
        return False

    return True

def puede_entrar(pentrada: str, plista_entrada: list):
    """"
    Función que comprueba la entrada de la bici

    args: pentrada (str): entrada a comprobar
          plista_entrada (list): lista de entradas validas

    returns: bool
    """
def puede_entrar(pentrada: str, plista_entrada: list):
    if not plista_entrada:
        return True

    for registro in reversed(plista_entrada):
        if registro.numero_serie == pentrada:
            return registro.accion != "IN"

    return True


def puede_salir(psalida: str, plista_salida: list):
    """"
    Función que comprueba la salida de la bici

    args: psalida (str): salida a comprobar
          plista_salida (list): lista de salidas validas

    returns: bool
    """
    puede_salir = False
    if plista_salida != None and len(plista_salida) >0:
            for registro in reversed(plista_salida):
                if registro.numero_serie == (psalida):
                    if registro.accion == ("OUT"):
                        puede_salir = False
                    else: 
                        puede_salir = True
                    break
    return puede_salir

def campo_no_vacio(pcampo: str):
    """"
    Función que comprueba que el campo no esta vacio

    args: pcampo (str): campo a comprobar

    returns: bool
    """
    if pcampo is None:
        return False
    
    # Convertimos a cadena para validar espacios
    texto = str(pcampo).strip()
    
    return texto != ""


def normalizar_texto(pespacio: str):
    """"
    Función que comprueba si hay espacios en el texto

    args: pespacio (str): texto a comprobar

    returns: bool
    """
    import unicodedata
    
    if pespacio is None:
        return False
    
    # Convertimos a texto
    texto = str(pespacio).strip().lower()

    # Normalizamos eliminando acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))

    # Validamos si quedó algo
    return texto != ""




def normalizar_email(valor) -> bool:
    """
    Normaliza un email y devuelve True si, después de limpiarlo
    (quitar espacios, minúsculas y validar formato),
    el email es válido. Si no, devuelve False.
    """
    if valor is None:
        return False

    # Convertimos a texto y limpiamos espacios
    email = str(valor).strip().lower()

    # Expresión regular simple pero correcta para validar emails comunes
    patron = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    
    return bool(re.match(patron, email))


def es_email_unico(p_uniemail: str, plista_usuarios: set | list) -> bool:
    """
    Devuelve True si 'email' no existe en la colección 'emails_existentes'.
    La colección puede ser una lista o un set.
    """

    email_normalizado = p_uniemail.strip().lower()
    emails_existentes = {
        u.email.strip().lower()
        for u in plista_usuarios
        if hasattr(u, "email") and u.email
    }
    return email_normalizado not in emails_existentes

def es_dni_unico(dni, lista_usuarios):    #puni_dni: str, plista_usuario: list
    """
    Función que comprueba si solo hay un dni

    args: puni_dni (str): dni a comprobar
        plista_usuario (list): lista de usuarios validos
    returns: bool
    """
    #es_dni_unico=True
    #for usuarios in plista_usuario:
        #if usuarios.dni == puni_dni:
            #es_dni_unico = False
            #break
        
    #return es_dni_unico

    for usuario in lista_usuarios:
        if usuario.dni == dni:
            return False
    return True


def es_serie_unica(pnumero_serie: str, plista_bici: list):
    """"
    Función que comprueba si solo esta ese numero de serie

    args: puni_serie (str): numero de serie a comprobar
        plista_bicis (list): lista de bicis validas
    returns: bool
    """
    for bici in plista_bici:
        if bici.numero_serie == pnumero_serie:
            return False  
    return True

def existe_usuario(plista_usuarios: str, conn: sqlite3.Connection):
    """"
    Función que comprueba si existe el usuario

    args: pusuario_ok (str): usuario a comprobar
        plista_usuario (list): lista de usuarios validos

    returns: bool
    """
    existe_usuario(conn,plista_usuarios )
    return False
            


def existe_bici(pbici_ok: str, conn: sqlite3.Connection):
    """"
    Función que comprueba si existe la bici
    
    args: pbici_ok (str): bici a comprobar
        plista_bici (list): lista de bicis validas

    returns: bool
    """
    existe_bici(conn, pbici_ok)
    return False

def validar_dni(dni):
    """
    Función que valida un DNI español.
    args: dni (str): DNI a validar
    returns: bool
    """

    # Eliminar espacios y convertir a mayúsculas para simplificar
    dni = dni.strip().upper()

    # Comprobar el formato básico (8 dígitos y una letra)
    if len(dni) != 9:
        return False

    numeros = dni[:-1]
    letra_introducida = dni[-1]

    if not numeros.isdigit():
        return False

    if not letra_introducida.isalpha():
        return False

    # Calcular la letra de control
    letras_control = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    numero_dni = int(numeros)
    resto = numero_dni % 23
    letra_correcta = letras_control[resto]

    return letra_correcta == letra_introducida