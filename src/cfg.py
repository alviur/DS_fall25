# -*- coding: utf-8 -*-
"""
cfg.py : Dades de configuració de la pràctica i funcions auxiliars
Adaptat per a gestió d'imatges generades amb IA
"""

import platform
import sys
import os
import os.path
import uuid


#############################################################################
#
# Secció de CONFIGURACIÓ
#
#############################################################################

# Selecció del vostre PATH amb les imatges generades
#
ROOT_DIR  = r"generated_images"                      # Directori local
#ROOT_DIR = r"E:\_UAB\ED\IMAGE-CORPUS"              # Windows
#ROOT_DIR = r"/opt/_uab/ed/image-corpus"             # Linux
#ROOT_DIR = r"/Users/usuari/_uab/ed/image-corpus"    # MacOS
#
# Nota: En plataforma Windows cal utilitzar strings literals, doncs el símbol
#       backslash (\) s'utilitza per defecte com ESCAPE. Per definir un string
#       literal s'utilitza el prefix 'r'. Exemple: r"C:\Windows"
#

# Imatge per defecte per a fer proves
#
IMAGE_DEFAULT = "0b4993aa-093c-42a6-a90a-073dce964bf0.png"

# Mode de visualització
#
#DISPLAY_MODE = 0  # Només "imprimir per pantalla" metadades (sense mostrar imatge)
#DISPLAY_MODE = 1  # "Imprimir metadades" i "mostrar imatge"
#DISPLAY_MODE = 2  # Només "mostrar imatge" (visualització regular)
DISPLAY_MODE = 1

#############################################################################
#
# TOOLS: No modificar a partir d'aquest punt !!!
#
#############################################################################

_running_platform = platform.system()

if   _running_platform == "Windows" : _rsys = 1
elif _running_platform == "Linux"   : _rsys = 2
elif _running_platform == "Darwin"  : _rsys = 3
else                                : _rsys = 0

if _rsys > 0 :
    print("Running on: " + _running_platform + " ({})\n".format(_rsys))
else:
    print("ERROR: Platform unknown!")
    sys.exit(1)

if not os.path.isdir(ROOT_DIR):
    print("ERROR: ROOT_DIR inexistent!")
    sys.exit(1)


def get_root() -> str:
    """Retorna el local pathname complet de la col·lecció d'imatges."""
    return os.path.realpath(ROOT_DIR)

def get_uuid(filename: str = "") -> str:
    """Retorna el UUID d'un path."""
    return uuid.uuid5(uuid.NAMESPACE_URL, filename)

def get_canonical_pathfile(filename: str) -> str:
    """Retorna el pathname relatiu amb un format universal."""
    """Exemple: subdir1/subdir2/image01.png"""
    file = os.path.normpath(filename)
    file = os.path.relpath(file, ROOT_DIR)
    file = file.replace(os.sep, '/')
    return  file

def get_one_file(mode: int = 0) -> str:
    """Retorna el local pathname complet de la darrera imatge a la col·lecció."""
    """Si el valor és 1 retorna la imatge per defecte envers cercar-la."""
    """Funció d'exemple, no utilizar a la pràctica directament!"""
    file = os.path.realpath(os.path.join(ROOT_DIR, IMAGE_DEFAULT))
    print("get_one_file(): ", ROOT_DIR , IMAGE_DEFAULT, file )
    if mode != 1 :
        for root, dirs, files in os.walk(ROOT_DIR):
            for filename in files:
                if filename.lower().endswith(tuple(['.png', '.jpg', '.jpeg'])):
                    print("found:  " + os.path.join(root, filename))
                    file = os.path.join(root, filename)
    print("        select: " + file + "\n")
    return file