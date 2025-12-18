# ECPY_Proyecto_BikeParking_G2
Proyecto Bike Parking G2
Este proyecto se trata de la gestion de un parking de bicicletas,tiene varias funciones que van desde dar el alta el usuario con su bicicleta, hasta poder eliminar tanto el usuario como la bicileta incluso saber cuantas bicis tenemos dentro del parking y de quien son. A traves del menu podremos meter una bici ya registrada o sacarla de dicho parking poniendo su codigo de bici y el DNI del dueño de dicha bici.

Para poder ejecutar el programa tienes que hacer los siguientes pasos:
    -Clonar con GitHub:
        -git clone https://github.com/amaiaDi/ECPY_Proyecto_BikeParking_G2.git
        -cd parking-bicis
        -O descargar el ZIP y descomprimirlo.

    -Ejecutar el archivo principal desde la carpeta del proyecto:
        -python app.py

El programa se iniciará automáticamente mostrando el menú principal.

Cuando inicias el programa te sale un menu con cuatro opciones:
    -Primera: Se usa para gestionar los usuarios y las bicis, que a su vez tiene cinco opciones que son:
        -Primera: Sirve para añadir un usuario.
        -Segunda: Se usa para eliminar el usuario.
        -Tercera: Añade las bicicletas.
        -Cuarta: Se encarga de eliminar dichas bicicletas.
    -Segunda: Una vez estas registrado como usuario y tienes una bici registrada, con esta opcion podras registrar que vas a meter dicha bici en el parking.
    -Tercera: En esta opción, una vez tengas ya una bici, dentro podras usarla para sacar la bici del parking.
    -Cuarta: Sirve para salir del programa.

Para poder hacer este programa hemos usado los siguientes ficheros csv:
    -leer_csv_dic:Este archivo se encarga de leer 
    los archivos csv de path.
    -scribir_csv_dic: Este archivo escribe diccionarios
    -asegurar_csvs: Asegura que los csv tengan cabecera.

    