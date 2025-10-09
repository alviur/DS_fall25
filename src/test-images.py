# -*- coding: utf-8 -*-
"""
test-images.py : Script de proves per visualitzar imatges generades amb IA
"""

import cfg      # Necessari per a la pràctica !!
                # Mireu el contingut de l'arxiu

import os.path
import sys
import numpy    #  installed in anaconda by default
import time
from PIL import Image      # $ pip install pillow


# STEP 1: Cerca de les imatges al filesystem
print("Cercant imatges dins [" + cfg.get_root() + "]\n")
uri_file = cfg.get_one_file(0)  # Aquesta funció és només de proves!

if not os.path.isfile(uri_file):
    print("ERROR: Imatge inexistent!")
    sys.exit(1)


# STEP 2: Obtenció de les metadades
try:
    img = Image.open(uri_file)
    metadata = cfg.read_png_metadata(uri_file)
except Exception as e:
    print(f"ERROR: No es pot llegir la imatge: {e}")
    sys.exit(1)

print("Metadades trobades:")
print(metadata)
print('')

if not metadata:
    print("WARNING: Imatge sense metadades generades!")

# Extracció de metadades específiques d'IA generada
try:
    prompt = metadata.get('Prompt', 'None')
except:
    prompt = "None"

try:
    seed = metadata.get('Seed', 'None')
except:
    seed = "None"

try:
    cfg_scale = metadata.get('CFG_Scale', 'None')
except:
    cfg_scale = "None"

try:
    steps = metadata.get('Steps', 'None')
except:
    steps = "None"

try:
    sampler = metadata.get('Sampler', 'None')
except:
    sampler = "None"

try:
    model = metadata.get('Model', 'None')
except:
    model = "None"

try:
    generated = metadata.get('Generated', 'None')
except:
    generated = "None"

try:
    uuid_val = metadata.get('UUID', 'None')
except:
    uuid_val = "None"

try:
    created_date = metadata.get('Created_Date', 'None')
except:
    created_date = "None"

try:
    width = img.width
    height = img.height
except:
    width = -1
    height = -1


# STEP 3: Generació del identificador únic (compatible amb l'original)
name_file = cfg.get_canonical_pathfile(uri_file)
image_uuid = cfg.get_uuid(name_file)


# STEP 4: Visualització
if (cfg.DISPLAY_MODE < 2):
    print("Visualitzant [{}]".format(uri_file))
    print(" Dimensions: {}x{} pixels".format(width, height))
    print(" Prompt:     {}".format(prompt[:100] + "..." if len(prompt) > 100 else prompt))
    print(" Model:      {}".format(model))
    print(" Seed:       {}".format(seed))
    print(" CFG Scale:  {}".format(cfg_scale))
    print(" Steps:      {}".format(steps))
    print(" Sampler:    {}".format(sampler))
    print(" Generated:  {}".format(generated))
    print(" Created:    {}".format(created_date))
    print(" UUID (calc):{}".format(image_uuid))
    print(" Arxiu:      {}".format(name_file))

if (cfg.DISPLAY_MODE > 0):
    # Mostrar la imatge (simple display)
    print("\nMostrant imatge...")

    try:
        # Simple display using PIL
        img.show()
        print("Imatge mostrada. Premi Enter per continuar...")
        input()
    except Exception as e:
        print(f"No es pot mostrar la imatge: {e}")
        print("Potser necessiteu instal·lar un visualitzador d'imatges.")


# END
print("\nFinal!")
