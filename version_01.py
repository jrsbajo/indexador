# sistema para la indexación de documentos

# =====================================================================
# importar librerías
# =====================================================================
from PyPDF2 import PdfReader
import nltk
from collections import defaultdict
import sqlite3
import json
from fuzzywuzzy import process

# =====================================================================
# leer un archivo PDF

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


def set_up_base_de_datos(db_path):
    """
    Crear una base de datos SQLite.

    Params
    ------
        db_path : str
            PATH a la base de datos.
    """

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
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


def almacenar_diccionario(db_path, nombre_documento, diccionario):
    """
    En una base de datos SQLite, almacenar la información de un diccionario.

    Params
    ------
        db_path : str
            PATH a la base de datos.
            La base de datos debe tener una tabla llamada "indice" con las columnas:
                - palabra   (PK)
                - documento (PK)
                - posiciones
        diccionario : dict
            Diccionario con clave cada palabra y valor sus posiciones.
    """

    # Conectar con la base de datos SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Insertar datos del diccionario en la tabla
    name_table = "indice"
    for palabra, posiciones in diccionario.items():
        # Convertir la lista de posiciones en una cadena JSON para su almacenamiento
        posiciones_json = json.dumps(posiciones)
        c.execute(f"INSERT INTO {name_table} (palabra, documento, posiciones) VALUES (?, ?, ?)",
                  (palabra, nombre_documento, posiciones_json))
        # OR REPLACE 
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def obtener_de_base_de_datos(db_path, nombre_documento):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Obtener todos los registros de la tabla
    c.execute("SELECT palabra, posiciones FROM indice WHERE documento = (?)", (nombre_documento))

    # Construir el diccionario
    indice_diccionario = {}
    for row in c.fetchall():
        # Asumiendo que 'positions' es una cadena de números separados por comas
        indice_diccionario[row[0]] = list(map(int, row[1].split(',')))

    conn.close()
    return indice_diccionario


def buscar_palabra_db(db_path, palabra):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT posiciones, documento FROM indice WHERE palabra = ?", (palabra,))
    # resultado = c.fetchone()
    retrieved = {}
    # print(resultado)
    for row in c:
        retrieved[row[1]] = row[0]
    conn.close()

    # print(retrieved)

    if retrieved.keys():
        for clave in retrieved:
            retrieved[clave] = list(map(int, retrieved[clave].strip('[]').split(',')))
    return retrieved


def buscar_palabra_fw(diccionario, palabra):

    coincidencias = process.extract(palabra, diccionario.keys(), limit=5)

    for palabra in coincidencias:
        print(palabra)
        if palabra[1] > 90:
            return diccionario[palabra[0]]
        else:
            return "Palabra no encontrada."



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

    # Extraer el índice del documento
    indice = extraer_de_pdf(path_documento)

    # Almacenar el índice en la base de datos
    almacenar_diccionario(path_bbdd, nombre_documento, indice)


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

    # Buscar la palabra en la base de datos
    posiciones = buscar_palabra_db(path_bbdd, palabra)

    print(f"La palabra {palabra} aparece en:")
    for clave in posiciones:
        print(f"    - archivo <{clave}>, posiciones {posiciones[clave]}")

# ================================== VARIABLES ==================================

path_documento_1  = "files/trabajo_final_pl_modelos_bayesianos.pdf" ; nombre_documento_1 = "trabajo_final_pl_modelos_bayesianos"
path_documento_2  = "files/612_instruccionespractica.pdf" ; nombre_documento_2 = "612_instruccionespractica"
path_bbdd       = "data/index_database.db"

palabra = "bayesiano"

# ============================ Ejecución del progama ============================

# set_up_base_de_datos(path_bbdd)

# almacenar_documento(path_documento_1, nombre_documento_1)
# almacenar_documento(path_documento_2, nombre_documento_2)

buscar_palabra(path_bbdd, palabra)