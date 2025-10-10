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
ROOT_DIR  = r"../generated_images"                                   # Github
#ROOT_DIR = r"E:\_UAB\ED\DS_fall25-main\generated_images"            # Windows
#ROOT_DIR = r"/opt/_uab/ed/DS_fall25-main/generated_images"          # Linux
#ROOT_DIR = r"/Users/usuari/_uab/ed/DS_fall25-main/generated_images" # MacOS
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


def read_png_metadata(filename):
    """
    Llegeix les metadades embegudes en un arxiu PNG.
    
    Suporta chunks tEXt i iTXt (Unicode).
    
    Args:
        filename (str): Path a l'arxiu PNG
        
    Returns:
        dict: Diccionari amb les metadades. Retorna {} si no n'hi ha.
              Si hi ha error, retorna None.
    
    Exemple:
        metadata = read_png_metadata("image.png")
        if metadata:
            prompt = metadata.get('Prompt', 'None')
            model = metadata.get('Model', 'None')
    """
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    metadata = {}
    
    try:
        with open(filename, 'rb') as f:
            # Verificar signatura PNG
            signature = f.read(8)
            if signature != PNG_SIGNATURE:
                print(f"ERROR: {filename} no és un PNG vàlid")
                return None
            
            # Llegir chunks
            while True:
                # Llegir length del chunk (4 bytes, big-endian)
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    break  # EOF
                
                length = int.from_bytes(length_bytes, byteorder='big')
                
                # Llegir tipus del chunk (4 bytes ASCII)
                chunk_type_bytes = f.read(4)
                if len(chunk_type_bytes) < 4:
                    break
                
                chunk_type = chunk_type_bytes.decode('ascii', errors='ignore')
                
                # Llegir dades del chunk
                if length > 0:
                    chunk_data = f.read(length)
                    if len(chunk_data) < length:
                        break  # EOF inesperat
                else:
                    chunk_data = b''
                
                # Llegir CRC (4 bytes) - no el validem però l'hem de saltar
                crc = f.read(4)
                if len(crc) < 4:
                    break
                
                # Processar chunks de text
                if chunk_type == 'tEXt':
                    # Format: keyword\0text
                    try:
                        null_pos = chunk_data.index(b'\x00')
                        keyword = chunk_data[:null_pos].decode('latin-1')
                        text = chunk_data[null_pos + 1:].decode('latin-1')
                        metadata[keyword] = text
                    except (ValueError, UnicodeDecodeError) as e:
                        # Si hi ha error, ignorem aquest chunk
                        pass
                
                elif chunk_type == 'iTXt':
                    # Format: keyword\0compression_flag\0compression_method\0language\0translated_keyword\0text
                    try:
                        null_pos = chunk_data.index(b'\x00')
                        keyword = chunk_data[:null_pos].decode('latin-1')
                        rest = chunk_data[null_pos + 1:]
                        
                        # Saltem compression flag (1 byte) i compression method (1 byte)
                        if len(rest) >= 2:
                            compression_flag = rest[0]
                            rest = rest[2:]
                            
                            # Saltem language tag (fins al següent \0)
                            if b'\x00' in rest:
                                null_pos = rest.index(b'\x00')
                                rest = rest[null_pos + 1:]
                                
                                # Saltem translated keyword (fins al següent \0)
                                if b'\x00' in rest:
                                    null_pos = rest.index(b'\x00')
                                    text_data = rest[null_pos + 1:]
                                    
                                    # Si està comprimit, no el processem (necessitaria zlib)
                                    if compression_flag == 0:
                                        text = text_data.decode('utf-8', errors='ignore')
                                        metadata[keyword] = text
                    except (ValueError, UnicodeDecodeError) as e:
                        # Si hi ha error, ignorem aquest chunk
                        pass
                
                # Si trobem IEND, hem acabat
                elif chunk_type == 'IEND':
                    break
        
        return metadata
    
    except FileNotFoundError:
        print(f"ERROR: Arxiu {filename} no trobat")
        return None
    except IOError as e:
        print(f"ERROR llegint {filename}: {e}")
        return None
    except Exception as e:
        print(f"ERROR inesperat processant {filename}: {e}")
        return None


def get_png_dimensions(filename):
    """
    Llegeix les dimensions d'un arxiu PNG del chunk IHDR.
    
    Args:
        filename (str): Path a l'arxiu PNG
        
    Returns:
        tuple: (width, height) o (None, None) si hi ha error
    """
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    
    try:
        with open(filename, 'rb') as f:
            # Verificar signatura
            signature = f.read(8)
            if signature != PNG_SIGNATURE:
                return (None, None)
            
            # El primer chunk ha de ser IHDR
            length_bytes = f.read(4)
            if len(length_bytes) < 4:
                return (None, None)
            
            chunk_type = f.read(4)
            if chunk_type != b'IHDR':
                return (None, None)
            
            # IHDR conté: width (4), height (4), bit_depth (1), ...
            ihdr_data = f.read(8)  # Només necessitem els primers 8 bytes
            
            width = int.from_bytes(ihdr_data[0:4], byteorder='big')
            height = int.from_bytes(ihdr_data[4:8], byteorder='big')
            
            return (width, height)
    
    except Exception as e:
        print(f"ERROR llegint dimensions de {filename}: {e}")
        return (None, None)


