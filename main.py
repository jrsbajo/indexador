from indexador import set_up_base_de_datos, cargar_varios_pdf, buscar_palabra
from time import sleep

# ================================== VARIABLES ==================================
# path_listado_documentos = "./pdfs.yaml"
PATH_BBDD       = "data/index_database.db"

palabra = "bayesiano"
# ============================ Ejecución del progama ============================


def todo():
    print()
    valor = input("¿Qué desea hacer? \n0. Configurar la base de datos \n1. Cargar documentos\n2. Buscar palabra\n> ")

    if valor == "0":
        try:
            set_up_base_de_datos(PATH_BBDD)
            print("Se ha configurado la base de datos correctamente.", end="\n\n")
        except:
            print("Se ha producido algún error al configurar la base de datos.", end="\n\n")

    elif valor == "1":
        path_listado_documentos = input("Introduzca el path al archivo yaml con el listado de documentos: ")
        if path_listado_documentos == "":
            path_listado_documentos = "./pdfs.yaml"
            print(f"Se estableció la ruta por defecto: '{path_listado_documentos}'")

        cargar_varios_pdf(PATH_BBDD, path_listado_documentos)

    elif valor == "2":
        palabra = input("Introduzca la palabra a buscar: ")
        buscar_palabra(PATH_BBDD, palabra)


if __name__ == "__main__":
    print("======================================")
    print("Bienvenido al indexador de documentos.")
    print("======================================", end="\n\n")

    while True:
        todo()
        sleep(0.5)