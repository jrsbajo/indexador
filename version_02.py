# sistema para la indexación de documentos
# MEJORANDO EL SISTEMA DE CARGA DE VARIOS FICHEROS

# =====================================================================
# importar librerías
# =====================================================================
from PyPDF2 import PdfReader
import nltk
from collections import defaultdict
import sqlite3
import json
from fuzzywuzzy import process
import yaml

# =====================================================================

# -----------------------------------------------------------------------------------------------
# tratar documentos
# -----------------------------------------------------------------------------------------------

def extraer_de_pdf(path):
    """
    Convierte un archivo en PDF a un diccionario.

    Params
    ------
        file : str
            PATH al archivo.
    
    Devuelve
    --------
        indice : default dict (Collections)
            Diccionario con clave cada palabra y valor sus posiciones.
    """

    texto = ""
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        texto = ""

        # Leer cada página y extraer el texto
        for page in reader.pages:
            texto += page.extract_text()

        # Tokenización y creación del índice
        tokens = nltk.word_tokenize(texto.lower())
        indice = defaultdict(list)
        for posicion, token in enumerate(tokens):
            indice[token].append(posicion)

    return indice

# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# tratar con la base de datos
# -----------------------------------------------------------------------------------------------

def set_up_base_de_datos(path_bbdd):
    """
    Crear una base de datos SQLite.

    Params
    ------
        path_bbdd : str
            PATH a la base de datos.
    """

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(path_bbdd)
    c = conn.cursor()

    # Crear una nueva tabla (si aún no existe)
    c.execute('''CREATE TABLE IF NOT EXISTS indice (
        palabra TEXT,
        documento TEXT,
        posiciones TEXT,
        PRIMARY KEY (palabra, documento)
    )''',)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def almacenar_diccionario(path_bbdd, nombre_documento, diccionario):
    """
    En una base de datos SQLite, almacenar la información de un diccionario.

    Params
    ------
        path_bbdd : str
            PATH a la base de datos.
            La base de datos debe tener una tabla llamada "indice" con las columnas:
                - palabra   (PK)
                - documento (PK)
                - posiciones
        diccionario : dict
            Diccionario con clave cada palabra y valor sus posiciones.
    """

    conn = sqlite3.connect(path_bbdd)
    c = conn.cursor()

    name_table = "indice"
    for palabra, posiciones in diccionario.items():
        posiciones_json = json.dumps(posiciones)
        c.execute(f"INSERT OR REPLACE INTO {name_table} (palabra, documento, posiciones) VALUES (?, ?, ?)",
                  (palabra, nombre_documento, posiciones_json))

    conn.commit()
    conn.close()


# def obtener_de_base_de_datos(path_bbdd, nombre_documento):
#     """
#     Obtener los índices de 
#     """
#     conn = sqlite3.connect(path_bbdd)
#     c = conn.cursor()
#     c.execute("SELECT palabra, posiciones FROM indice WHERE documento = (?)", (nombre_documento))

#     indice_diccionario = {}
#     for row in c.fetchall():
#         indice_diccionario[row[0]] = list(map(int, row[1].split(',')))

#     conn.close()
#     return indice_diccionario

def retrieve_all_palabras(path_bbdd):
    conn = sqlite3.connect(path_bbdd)
    c = conn.cursor()

    c.execute("SELECT palabra FROM indice")
    data = c.fetchall()
    conn.close()

    return data

# -----------------------------------------------------------------------------------------------
# buscando palabra(s)
# -----------------------------------------------------------------------------------------------

def retrieve_palabra(path_bbdd, palabra):
    conn = sqlite3.connect(path_bbdd)
    c = conn.cursor()

    c.execute("SELECT posiciones, documento FROM indice WHERE palabra = ?", (palabra,))
    retrieved = {}
    for row in c:
        retrieved[row[1]] = row[0]
    conn.close()

    if retrieved.keys():
        for clave in retrieved:
            retrieved[clave] = list(map(int, retrieved[clave].strip('[]').split(',')))
    return retrieved


def check_palabras(path_bbdd, palabra):
    listado = retrieve_all_palabras(path_bbdd)
    coincidencias = process.extract(palabra, listado, limit=5)
    palabras = set()
    for palabra in coincidencias:
        if palabra[1] > 90:
            palabras.add(str(palabra[0]).strip('()').split(',')[0].strip("''"))
    return palabras


def buscar_palabra(path_bbdd, palabra):
    """
    Buscar una palabra en el índice de la base de datos.

    Params
    ------
        path_bbdd : str
            PATH a la base de datos.
        palabra : str
            Palabra a buscar.
    """
    # posiciones = retrieve_palabra(path_bbdd, palabra)

    listado = check_palabras(path_bbdd, palabra)
    print(f"Se han encontrado las siguientes coincidencias: {listado}")

    for palabra in listado:
        posiciones = retrieve_palabra(path_bbdd, palabra)

        print(f"La palabra {palabra} aparece en:")
        for clave in posiciones:
            print(f"    - archivo <{clave}>, posiciones {posiciones[clave]}")

# def buscar_palabra_fw(diccionario, palabra):

#     coincidencias = process.extract(palabra, diccionario.keys(), limit=5)

#     for palabra in coincidencias:
#         print(palabra)
#         if palabra[1] > 90:
#             return diccionario[palabra[0]]
#         else:
#             return "Palabra no encontrada."


# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# carga de datos
# -----------------------------------------------------------------------------------------------

def almacenar_documento(path_documento, nombre_documento):
    """
    Almacenar un documento en la base de datos.

    Params
    ------
        path_documento : str
            PATH al documento.
        nombre_documento : str
            Nombre del documento.
    """

    indice = extraer_de_pdf(path_documento)
    almacenar_diccionario(path_bbdd, nombre_documento, indice)


def cargar_desde_archivo_yaml(path):
    # estructura:
        # nombre_del_documento: path_al_documento
    with open(path, 'r') as file:
        archivo = yaml.safe_load(file)
        return archivo
    
def cargar_varios_pdf(path_litado):
    litado = cargar_desde_archivo_yaml(path_litado)
    for nombre_documento, path_documento in litado.items():
        try:
            almacenar_documento(path_documento, nombre_documento)
            print(f"Documento {nombre_documento} cargado correctamente en la base de datos.")
        except:
            print(f"Error al cargar el documento {nombre_documento} en la base de datos.")

# -----------------------------------------------------------------------------------------------


# ================================== VARIABLES ==================================

# path_documento_1  = "files/trabajo_final_pl_modelos_bayesianos.pdf" ; nombre_documento_1 = "trabajo_final_pl_modelos_bayesianos"
# path_documento_2  = "files/612_instruccionespractica.pdf" ; nombre_documento_2 = "612_instruccionespractica"
path_listado_documentos = "./pdfs.yaml"
path_bbdd       = "data/index_database.db"

palabra = "bayesiano"


# ============================ Ejecución del progama ============================

# set_up_base_de_datos(path_bbdd)

# almacenar_documento(path_documento_1, nombre_documento_1)
# almacenar_documento(path_documento_2, nombre_documento_2)

# cargar_varios_pdf(path_listado_documentos)

buscar_palabra(path_bbdd, palabra)

# listado = retrieve_all_palabras(path_bbdd)

