"""
app.py — Aplicación básica del Sistema de Parking de Bicis

Este archivo contiene:
- El menú principal.
- Las funciones de cada opción (alta usuario, alta bici, IN/OUT, etc.).
- Funciones de interfaz (mostrar menús, pedir datos, mensajes).
- El bucle principal (main).
"""

# ----------------------------------
# 1. IMPORTS
# IMPORTAR AQUÍ:
# - datetime (para timestamp)
# - Constantes y rutas desde config.py
# - Funciones de lectura/escritura desde csv_utils
# - Validaciones desde validators
#
# EJEMPLO (NO ESCRIBIRLO):
# from data_utils.validators import es_dni_valido
#
# SOLO INDICAR LOS IMPORTS NECESARIOS.
# ----------------------------------
from datetime import datetime
import data_utils.validators  as valid
from data_utils.csv_utils import *
from config import *
import sqlite3 
import data_utils.sqlite_utils  as sql_ut
from pathlib import Path
from modelo.bici import Bici
from modelo.usuario import Usuario
from modelo.registro import Registro
# ----------------------------------
# 2. CONSTANTES LOCALES (opcional)
# AQUÍ PUEDEN DEFINIR:
# - Títulos del menú
# - Separadores de texto
# - Mensajes reutilizables
#
# Ejemplos orientativos:
# TITULO_APP = "SISTEMA DE PARKING DE BICIS"
# SEPARADOR = "-" * 40
#
# Pero SIN poner código aún.
# ----------------------------------

# ----------------------------------
# 3. FUNCIONES DE INTERFAZ (UI)
# FUNCIONES QUE EL ALUMNADO DEBE CREAR:
#
# mostrar_titulo():
#   - Muestra título y separadores.
#
# print_ok(mensaje):
#   - Imprime OK: ...
#
# print_error(mensaje):
#   - Imprime ERROR: ...
#
# pedir_dato(prompt):
#   - Pide un dato al usuario y devuelve el texto.
#
# pausar():
#   - Espera a que el usuario pulse Enter.
#
# mostrar_menu_principal():
#   - Imprime las opciones del menú principal.
#
# mostrar_menu_gestion():
#   - Imprime las opciones del submenú (usuarios y bicis).
#
# Todas estas funciones deben ser ESCRITAS POR LOS ALUMNOS.
# SOLO DEJAR LOS COMENTARIOS.
# ----------------------------------

def mostrar_titulo():
    """Muestra el titulo cuando un usuario llega a la pantalla
    """
    titulo = "SISTEMA DE PARKING DE BICIS"
    
    print("=" * 5 + " " + titulo + " " + "=" * 5)
    print("-" * (5 + 1 + len(titulo) + 1 + 5))

def print_ok(mensaje):
    """Manda un mensaje de ok al usuario

    Args:
        mensaje (str): Es el mensaje que se le pone al usuario
    """
    print(f"ok: {mensaje}")

def print_error(mensaje):
    """Le pone por pantalla un mensaje de error al usuario

    Args:
        mensaje (str): Es el mensaje que se le pone al usuario
    """
    print(f"ERROR: {mensaje}")

def pedir_dato(prompt):
    """Pide los datos
    """
    input("Dame tus datos.")
    print(f"{prompt}")

def pausar():
    """Espera a que el usuario pulse enter para pasar al siguiente paso
    """
    pass

def mostrar_menu_principal():
    """Muestra el menu principal
    """
    mostrar_titulo()
    print("1) Gestión de usuarios y bicis")
    print("2) Registrar ENTRADA (IN)")
    print("3) Registrar SALIDA (OUT)")
    print("0) Salir")

# ----------------------------------
# 4. FUNCIONES DE CASO DE USO
# AQUÍ DEBEN CREAR UNA FUNCIÓN POR CADA ACCIÓN DEL MENÚ:
#
# alta_usuario():
#   - Pedir DNI, nombre, email.
#   - Validar formato y unicidad con validators.py.
#   - Leer usuarios CSV.
#   - Añadir usuario si es válido.
#   - Guardar CSV.
#   - Mostrar OK o ERROR.
#
# eliminar_usuario():
#   - Pedir DNI.
#   - Verificar que el usuario existe.
#   - Verificar que NO tiene bicis asociadas.
#   - Si es válido, eliminarlo del CSV.
#
# eliminar_bici():
#   - Pedir serie.
#   - Verificar que existe.
#   - Verificar que NO está dentro (mirar registros.csv).
#   - Eliminarla del CSV.
# registrar_entrada():
#   - Pedir serie + DNI.
#   - Validar existencia.
#   - Verificar con validators si puede entrar.
#   - Añadir un registro con timestamp y acción IN.
# registrar_salida():
#   - Igual que entrada, pero acción OUT.
#
# Estas funciones SOLO deben tener comentarios,
# no código.
# ----------------------------------


def añadir_usuario():
    dni = input("Escribe tu DNI: ").strip()
    while dni == "":
        print("ERROR: Valor no correcto")
        dni = input("Escribe tu DNI: ").strip()

    nombre = input("Escribe tu nombre completo: ").strip()
    while nombre == "":
        print("ERROR: Valor no correcto")
        nombre = input("Escribe tu nombre completo: ").strip()

    email = input("Escribe tu email: ").strip()
    while email == "":
        print("ERROR: Valor no correcto")
        email = input("Escribe tu email: ").strip()

    lista_usuarios = sql_ut.leer_usuarios(conn)
    
    for usuario in lista_usuarios:
        if usuario.dni == dni:
            print("ERROR: El DNI ya existe")
            return

    for usuario in lista_usuarios:
        if usuario.email == email:
            print("ERROR: El email ya existe")
            return

    nuevo_usuario = Usuario(dni, nombre, email)
    sql_ut.insert_usuario(conn, nuevo_usuario)

    print("OK: Usuario registrado correctamente.")
          

def añadir_bici():
    """Esta parte del codigo se encarga de añadir las bicis del usuario
    que no esten ya previamente registradas
    """
    
    numero_serie = input("Introduce nº de serie del cuadro:")
    while numero_serie == "":
        numero_serie = input("Introduce nº de serie del cuadro:")
       
    dni_usuario = input("Introduce DNI del usuario:")
    while dni_usuario == "":
        dni_usuario = input("Introduce DNI del usuario:")

    marca = input("Introduce marca de la bici:")
    while marca == "":
        marca = input("Introduce marca de la bici:")

    modelo = input("Introduce modelo de la bici:")
    while modelo == "":
        modelo = input("Introduce modelo de la bici:")

    lista_bicis = sql_ut.leer_bicis(conn)

    for bici in lista_bicis:
        if bici.numero_serie == numero_serie:
            print("ERROR: Esta bici ya existe")
            return
        
    nueva_bici = Bici(numero_serie, dni_usuario, marca, modelo)
    sql_ut.insert_bici(conn, nueva_bici)

    print("OK: Bici registrada correctamente")


def registrar_entrada():


    """ Comprueba si la bici esta de dentro del parking, si no es así la puedes meter.
    """
    lista_bicis = leer_csv_dic(PATH_BICIS)
    lista_registro = leer_csv_dic(PATH_REGISTROS)

    numero_serie = input("Introduce nº de serie del cuadro:")
    while numero_serie == "":
        numero_serie = input("Introduce nº de serie del cuadro:")
       
    if not valid.existe_bici(numero_serie, lista_bicis): 
    
        print("Esta bici no existe")
        return

    dni_usuario = input("Introduce DNI del usuisario:")
    while dni_usuario == "":
        dni_usuario = input("Introduce DNI del usuisario:")
    
    else:
        # Verificación de los datos la bici existe y esta vinculada al usuario
        if lista_bicis != None and len(lista_bicis) >0:
            for bici in lista_bicis:
                if bici["serie_cuadro"] == (numero_serie) and bici["dni_usuario"] != dni_usuario:               
                    print("No coinciden los datos: no se puede meter la bici")
                    return

        # Validación de la situacion de la bici en el registro y registro de la misma
        if valid.puede_entrar(numero_serie, lista_registro) == False:
         timestamp = timestamp
         accion = accion
         reg_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         sql_ut.insert_registro(conn, Registro(timestamp,accion, numero_serie, dni_usuario ))
         print("OK: Entrada registrada.") 

        else:
            print("La bici está dentro")


def registrar_salida():

    """ Comprueba si la bici esta fuera del parking, si no es así la puedes sacar.
    """
    lista_bicis = leer_csv_dic(PATH_BICIS)
    lista_registro = leer_csv_dic(PATH_REGISTROS)

    numero_serie = input("Introduce nº de serie del cuadro:")
    while numero_serie == "":
        numero_serie = input("Introduce nº de serie del cuadro:")
       
    if not valid.existe_bici(numero_serie, lista_bicis): 
    
        print("Esta bici no existe")
        return

    dni_usuario = input("Introduce DNI del usuisario:")
    while dni_usuario == "":
        dni_usuario = input("Introduce DNI del usuisario:")
    
    else:
        # Verificación de los datos la bici existe y esta vinculada al usuario
        if lista_bicis != None and len(lista_bicis) >0:
            for bici in lista_bicis:
                if bici["serie_cuadro"] == (numero_serie) and bici["dni_usuario"] != dni_usuario:               
                    print("No coinciden los datos: no se puede sacar la bici")
                    return

        # Validación de la situacion de la bici en el registro y registro de la misma
        if valid.puede_salir(numero_serie, lista_registro) == False:
           
         reg_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         escribir_csv_dic(PATH_REGISTROS, [{"timestamp" : reg_tiempo, "accion": "OUT", "serie_cuadro": numero_serie, "dni_usuario": dni_usuario}], ["timestamp", "accion", "serie_cuadro", "dni_usuario"])
         print("OK: Salida registrada.") 
           
        
        else:
            print("La bici no está dentro")
     
# ----------------------------------
# 5. SUBMENÚ DE GESTIÓN
# gestionar_usuarios_y_bicis():
#   - Mostrar menú de gestión.
#   - Bucle controlado (no usar while True).
#   - Llamar a:
#       alta_usuario()
#       eliminar_usuario()
#       alta_bici()
#       eliminar_bici()
#   - Volver al menú principal cuando el usuario elija "0".
# ----------------------------------

def menu_gestion_usuarios_bicis():
    """Muestra el menu de gestion de usuarios y bicis
    """
    seguir = True

    while seguir:
        print("--- GESTION USUARIOS Y BICIS ---\n")
        print(" 1) Añadir usuario")
        print(" 2) Eliminar usuario")
        print(" 3) Añadir bici")
        print(" 4) Eliminar bici")
        print(" 0) Volver\n")
        print("--------------------------------")

        opcion = (input("Introduce la opción: "))
    
        if opcion in ["0", "1", "2", "3", "4"]:

            if opcion == "1":
                print("--- AÑADIR USUARIO ---")
                print("----------------------")
                añadir_usuario()
        

            elif opcion == "2":
                print("--- ELIMINAR USUARIO ---")
                print("----------------------")
                sql_ut.delete_usuario()
               
            elif opcion == "3":
                print("--- AÑADIR BICI ---")
                print("----------------------")
                añadir_bici()

            elif opcion == "4":
                print("--- ELIMINAR BICI ---")
                print("----------------------")
                sql_ut.delete_bici()
        
            elif opcion == "0":
                seguir = False
    
            else:
                print("ERROR: Valor no correcto")
             

# ----------------------------------
# 6. MENÚ PRINCIPAL
# menu_principal():
#   - Mostrar menú.
#   - Leer opción del usuario.
#   - Llamar a:
#       gestionar_usuarios_y_bicis()
#       registrar_entrada()
#       registrar_salida()
#   - Opción "0": pedir confirmación y salir.
# ----------------------------------

def mostrar_menu(pRunning):
    """Muestra el menu principal y llama a las funciones correspondientes
    """
    global running

    while pRunning:
        mostrar_menu_principal()
        opcion = input("Introduzca una opción:")

        if opcion == "1":
            menu_gestion_usuarios_bicis()

        elif opcion == "2":
           registrar_entrada()

        elif opcion == "3":
            registrar_salida()

        elif opcion == "0":
            respuesta = input("¿Seguro que quieres salir? (s/n): ")
            if respuesta == "s":
                pRunning = False
                continue
            

# ----------------------------------
# 7. FUNCIÓN main()
# main():
#   - Asegurar que CSVs existen (asegurar_csvs()).
#   - Crear variable running = True.
#   - Bucle principal para mostrar menú.
#   - Llamar a menu_principal().

#
# Esta función arranca todo el programa.
# ----------------------------------

def main():
    """Función principal que arranca el programa
    """   
    running = True
    mostrar_menu(running)

# ----------------------------------
# 8. PUNTO DE ENTRADA
# if __name__ == "__main__":
#     main()
#
# Los estudiantes deben escribir esta parte.
# ----------------------------------


if __name__ == "__main__": 
    
    ruta=Path(DB_PATH)

    if not ruta.exists():
        sql_ut.init_db()    
    
    conn = sql_ut.get_connection(DB_PATH)
    try:
        main()
    finally:
        conn.close()
    