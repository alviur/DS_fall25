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
│   ├── cfg.py                   # Configuració del projecte
│   └── test-images.py           # Script de proves
└── media/                       # Imatges i diagrames de la guia
``` 

## Contingut de l'enunciat

L'enunciat (`project_guide.md `) inclou:

1. **Introducció** al context de la IA generativa i gestió d'imatges
2. **Codi d'exemple** per treballar amb metadades PNG
3. **Primer lliurament** amb 7 funcionalitats a implementar:
   - Llistat d'imatges PNG
   - Generació d'identificadors únics (UUID)
   - Consulta de metadades embegudes
   - Visualització d'imatges
   - Gestió de galeries JSON
   - Cerca per criteris
   - Creació dinàmica de galeries

## Dataset

El projecte utilitza un subconjunt del dataset **DiffusionDB** amb imatges generades per usuaris reals amb Stable Diffusion. Les metadades estan embegudes directament dins els fitxers PNG.

## Requisits tècnics

- Python 3.11
- Anaconda + Spyder OR VScode OR Pycharm
- Llibreries: `pillow`, `json`
- Format d'imatges: PNG amb metadades embegudes

## Autoria

Aquest projecte ha estat dissenyat per a l'assignatura d'Estructures de Dades del Grau en Enginyeria de Dades 2025/26.

---

**Nota:** Aquest repositori conté només l'enunciat i materials de suport. Els estudiants hauran de desenvolupar la seva pròpia implementació seguint les indicacions de la guia.
