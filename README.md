# Generative Index - Projecte d'Estructures de Dades

**Curs:** Estructures de Dades - Fall 2025  
**Grau:** Enginyeria de Dades  
**Universitat:** Universitat Autònoma de Barcelona

## Descripció

Aquest repositori conté l'**enunciat del projecte** per a l'assignatura d'Estructures de Dades del curs 2025/26. El projecte consisteix en implementar un gestor de col·leccions d'imatges generades amb Intel·ligència Artificial, anomenat **Generative Index**.

L'objectiu principal és aplicar estructures de dades complexes per optimitzar la gestió, cerca i visualització d'imatges generades amb models com Stable Diffusion, que inclouen metadades embegudes (prompts, paràmetres de generació, etc.).

## Estructura del repositori

``` .
├── README.md                    # Aquest fitxer
├── project_guide.md             # Enunciat complet de la pràctica
├── src/                         # Codi d'exemple i templates
│   ├── Submission_1/            # Primer lliurament (Gestió d'imatges generades)
│   │   ├── cfg.py                   # Configuració del projecte
│   │   ├── test-images.py           # Script de proves amb metadades PNG
│   │   ├── p1_main.py               # Template del main (opcional)
│   │   ├── ImageFiles.py            # Template: Gestió de llistat d'imatges
│   │   ├── ImageID.py               # Template: Generació d'identificadors UUID
│   │   ├── ImageData.py             # Template: Gestió de metadades
│   │   ├── ImageViewer.py           # Template: Visualització d'imatges
│   │   ├── Gallery.py               # Template: Gestió de galeries JSON
│   │   └── SearchMetadata.py        # Template: Cerca per metadades
│   └── Submission_2/            # Segon lliurament (Sistema de Recomanació)
│       ├── RecommenderSystem.py     # Sistema de recomanació amb CLIP embeddings
│       └── autograder_student.py    # Template de l'autograder per testing
│       
└── media/                       # Imatges i diagrames de la guia
```

## Contingut de l'enunciat

L'enunciat (`project_guide.md`) inclou:

### 1. **Introducció**
- Context de la IA generativa i gestió d'imatges
- Conceptes fonamentals: prompts, embeddings, similitud semàntica
- Visió general del projecte i objectius

### 2. **Codi d'exemple**
- Configuració del projecte (`cfg.py`)
- Script de proves per llegir metadades PNG
- Exemples d'ús i integració

### 3. **Primer lliurament (Submission_1)** - 7 funcionalitats
- **Func1:** Llistat d'imatges PNG
- **Func2:** Generació d'identificadors únics (UUID)
- **Func3:** Consulta de metadades embegudes
- **Func4:** Visualització d'imatges amb metadades
- **Func5:** Gestió i visualització de galeries JSON
- **Func6:** Cerca per criteris (prompts, models, dates, etc.)
- **Func7:** Creació dinàmica de galeries

### 4. **Segon lliurament (Submission_2)** - Competició de Recomanació
- **Fase 1:** Optimització de búsquedas de metadades (20 punts)
- **Fase 2:** Similitud d'imatges usant CLIP embeddings (40 punts)
- **Fase 3:** Camins de transició entre imatges (40 punts)
- Explicació de representacions numèriques (embeddings) i similitud semàntica
- Guia d'optimització i ús de estrutures de dades eficients

## Dataset

### Origen i Contingut
El projecte utilitza un subconjunt del dataset **DiffusionDB** amb imatges generades per usuaris reals amb Stable Diffusion. DiffusionDB és el primer dataset públic a gran escala de prompts text-to-image amb 14 milions d'imatges.

### Tamanys del Dataset
- **Lliurament 1:** 1,000 imatges (para testing local i desenvolupament)
- **Lliurament 2 (Competició):** 10,000 imatges (per a l'avaluació automàtica)

### Metadades
Les metadades estan embegudes directament dins els fitxers PNG (no en fitxers separats) utilitzant el sistema de *text chunks* del format PNG. Inclou:
- **Prompt:** Descripció textual usada per generar la imatge
- **Model:** Model de generació (SD1.5, SD2, SD3.5, Midjourney, DALLE2, Flux, etc.)
- **Seed, CFG_Scale, Steps, Sampler:** Paràmetres tècnics de generació
- **Created_Date:** Data de creació
- **Generated:** Indicador que és una imatge generada amb IA

### Recursos Adicionals per Lliurament 2
- **clip_vectors.json:** Vectors CLIP precalculats (embeddings de 512 dimensions) per a totes les 10,000 imatges
- **Dos conjunts d'imatges:**
  - *Full:* Imatges completes amb tota la qualitat visual (~2-3 GB)
  - *Lite:* Imatges simplificades (quadrat negre + metadades) para testing ràpid (~50-100 MB)

## Requisits tècnics

### Entorn
- Python 3.11
- Anaconda + Spyder OR VScode OR Pycharm

### Llibreries

#### Lliurament 1
- `json` - Manipulació de galeries

#### Lliurament 2
- **Python Standard Library únicament** - No es permeten llibreries externes com NumPy, SciPy, scikit-learn, etc.
- Estructures de dades integrades: `collections`, `heapq`, `json`
- Matemàtiques bàsiques: `math`, `random`

### Format d'imatges
PNG amb metadades embegudes usant text chunks

## Autoria

Aquest projecte ha estat dissenyat per a l'assignatura d'Estructures de Dades del Grau en Enginyeria de Dades 2025/26.

---

**Nota:** Aquest repositori conté només l'enunciat i materials de suport. Els estudiants hauran de desenvolupar la seva pròpia implementació seguint les indicacions de la guia.
