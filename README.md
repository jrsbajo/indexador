# Project Name

## Description
Provide a brief description of your project here.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Funcionamiento](#funcionamiento)
- [Motivation](#motivation)
- [Contact](#contact)

## Installation
1. Clone the repository
2. Install Python and libraries. The necessary resources are in the "requirements.txt" file.


## Usage
Execute the ```main.py``` file. Next, you will visualize a menu with multiple options.

If is the **first time** that you use the app, you will need to execute the setting up of the database.

> Select option 0 into the main menu.

**For following uses**:

**To index a new PDF file**
> Select option 1 from the main menu.

> Provide the *path* to the YAML format file in which you will have written the name following a key:value structure such that name:relative_path.

**To index a new PDF file**
> Select option 2 from the main menu.

> Type the word to search through all indexed files.


## Funcionamiento

To understand how the app works, you can refer to the `indexador.py` file. This file contains the main code for the indexing application. It provides functions for indexing new PDF files and searching through the indexed files.

To index a new PDF file, one or more, you can use the `cargar_varios_pdf()` function. This function takes a YAML format file as input, which contains the name and relative path of the PDF file to be indexed. Also, you can use `almacenar_documento()` to index only one PDF file providing directly the path and the name of the document in the call to the function.

To search through the indexed files, you can use the `buscar_palabra()` function. This function prompts the user to enter a word to search for, and it returns a list of matching files.

For more details on the implementation and usage of the app, please refer to the `indexador.py` file.

## Motivation

## Contact
