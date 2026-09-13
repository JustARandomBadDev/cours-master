# TP01 - Read and Manipulate Mocap Data

## Parsing

Les fichiers `.tsv` contiennent d'abord plusieurs lignes de métadonnées, puis la liste des markers, puis les positions `X Y Z` pour chaque frame.

J'ai donc fait un parser qui lit le fichier, récupère les noms des markers, puis stocke chaque frame sous la forme :

```python
{
    "HeadL": (x, y, z),
    "HeadTop": (x, y, z),
    ...
}
```

## Calcul des positions moyennes

J'ai utilisé une seule fonction `average_position()` qui prend :

* une liste de frames ;
* une liste de markers.

Ça permet de gérer avec la même fonction :

* un marker ;
* une partie du corps ;
* tout le corps ;
* une seule frame ;
* tout le mouvement.

Par exemple, pour une seule frame il suffit de passer :

```python
[data[100]]
```

et pour tout le mouvement :

```python
data
```

La position moyenne est calculée simplement en faisant la moyenne des coordonnées `X`, `Y` et `Z` de tous les markers sélectionnés.
