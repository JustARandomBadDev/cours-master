# TP02 - Motion Descriptors

## Run

### Animation

```bash
python src/main.py
```

### Stats

```bash
python src/stats.py
```

## Parsing

Le parser gère toujours les fichiers de markers, mais il peut aussi lire les fichiers de squelette `_s_`.

Pour chaque articulation et chaque frame, il récupère une position `(X, Y, Z)` et une orientation en quaternion `(QX, QY, QZ, QW)`. Une frame de squelette est donc stockée comme ça :

```python
{
    "Hips": ((x, y, z), (qx, qy, qz, qw)),
    "Spine": ((x, y, z), (qx, qy, qz, qw)),
    ...
}
```

## Skeleton

Les articulations sont définis dans `bones.py`. `Skeleton` utilise ces liens pour construire un petit volume 3D entre chaque paire d'articulations.

Vu que les positions des fichiers sont en millimètres, lles sont converties en mètres, recentrées par rapport à la position de `Hips`, puis les axes sont adaptés pour l'affichage.

Dans `main.py`, les fichiers sont d'abord récupérés avec le scraper. Le premier fichier de squelette trouvé est parsé puis affiché et animé avec le renderer OpenGL. L'animation est jouée à 200 frames par seconde, ce qui correspond à la fréquence des séquences testées.

## Motion descriptors

Le fichier `stats.py` parcourt tous les fichiers de squelette disponibles. Il lit leur fréquence d'acquisition et utilise les positions converties en mètres.

### Low-level

* la vitesse
* l'accélération
* le jerk

### High-level

* la quantité de mouvement, avec la somme des vitesses des articulations
* la vitesse du centroïde de toutes les articulations
* le volume de la boîte englobante du squelette

## Statistics

Pour chaque séquence et chaque descripteur, le programme affiche la moyenne, le minimum, le maximum et la médiane sur toutes les frames.
