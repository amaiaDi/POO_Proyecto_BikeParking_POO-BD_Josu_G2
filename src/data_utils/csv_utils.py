import csv
import os

def leer_csv_dic(ppathCSV):
    """Esta funcón se encarga de leer 
    los archivos csv de path

    Args:
        ppathCSV (str): Ruta al archivo csv del que leemos

    Returns:
        _type_: El contenido del csv, que es una lista de diccionarios
    """
    try:
        with open(ppathCSV, mode='r', encoding='utf-8') as file:
            lector = csv.DictReader(file)
            return list(lector)
    except FileNotFoundError:
        print(f"No se ha encontrado el archivo{ppathCSV}.")
        return


def escribir_csv_dic(ppathCSV, listdic, pnombre_campos):
    """Esta funcion escribe diccionarios

    Args:
        ppathCSV (str): Ruta al archivo csv del que escribimos
        listdic lst(dict): Son los datos a escribir en el archivo csv
        pnombre_campos (lst): Es una lista con los nombres de los campos en el csv

    Returns:
        _type_: None
    """
    try:
        
        with open(ppathCSV, mode='a', encoding='utf-8') as file:
            escribir = csv.DictWriter(file, fieldnames=pnombre_campos)
            escribir.writerows(listdic)
            return 
    except FileNotFoundError:
        print(f"No se ha encontrado el archivo {ppathCSV}.")
        return

    

def asegurar_csvs(ppathCSV, pnombre_campos, encoding='utf-8'):
    """Asegura que los csv tengan cabecera

    Args:
        ppathCSV (str): Ruta al archivo csv del que escribimos
        pnombre_campos (lst): Es una lista con los nombres de los campos
        encoding (str): Defaults to 'utf-8'. Codificacion del archivo csv
    Return:
        True: Indica que existe el archivo csv correcto
        False: Indica que no existe un archivo csv correcto
        
    """

    if os.path.exists(ppathCSV) != True:
        with open(ppathCSV, "w", newline="", encoding="utf-8") as f:
            # Crear un DictWriter con los campos
            escritor = csv.DictWriter(f, fieldnames = pnombre_campos)
    
            # Escribir la cabecera
            escritor.writeheader()
            return True
        
    else:
        try:
            with open(ppathCSV, mode='r', encoding='utf-8') as file:
                lector = csv.DictReader(file)
                primera_fila = next(lector)
                lst_primera_fila = list(primera_fila)
                if lst_primera_fila == pnombre_campos:
                    return True
                else:
                    return False
                return list(lector)
        except FileNotFoundError:
            print(f"No se ha encontrado el archivo{ppathCSV}.")
            return 

    



    
