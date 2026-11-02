# TP02

## Installation

Le projet utilise `uv`.

```bash
uv sync
```

## Lancement

Mettre les fichiers CSV dans `data/` puis lancer :

```bash
uv run python src/main.py data
```

## Données

Le dataset contient :

- 600 segments
- 29 415 frames
- 223 segments pour la main gauche
- 377 segments pour la main droite
- 32 signes différents

Les classes ne sont pas équilibrées. Certaines comme `Pi`, `5` ou `Personne` sont beaucoup plus présentes que d'autres.

## Features

Les positions absolues des articulations ne sont pas utilisées directement car la position de la main dans l'espace peut changer sans changer sa configuration.

Pour chaque frame, les features utilisées sont donc les distances entre le poignet et les autres articulations de la main.

On obtient ainsi une représentation qui dépend principalement de la forme de la main et beaucoup moins de sa position dans l'espace.

## Classification

Les données sont séparées avec 80 % pour l'entraînement et 20 % pour le test.

Les classifieurs utilisés sont :

- Logistic Regression
- K-NN
- Naive Bayes
- SVM

Les performances obtenues sont :

| Classifieur         | Accuracy | Precision | Recall |     F1 |
| ------------------- | -------: | --------: | -----: | -----: |
| Logistic Regression |   0.9165 |    0.9201 | 0.9165 | 0.9123 |
| K-NN                |   0.9910 |    0.9911 | 0.9910 | 0.9910 |
| Naive Bayes         |   0.7104 |    0.8024 | 0.7104 | 0.7070 |
| SVM                 |   0.8404 |    0.8323 | 0.8404 | 0.8106 |

Les matrices de confusion sont sauvegardées dans :

```text
confusion_matrices.png
```

## Résultats

K-NN donne les meilleurs résultats avec environ 99 % d'accuracy.

La Logistic Regression fonctionne aussi bien avec environ 92 %.

Le SVM est un peu moins bon avec environ 84 % et Naive Bayes est le moins performant avec environ 71 %.

Les distances entre les articulations semblent donc suffisantes pour bien différencier une grande partie des configurations de mains.

Les résultats sont quand même à prendre avec des pincettes vu que les classes sont assez déséquilibrées et les frames provenant d'un même segment sont très proches les unes des autres.

## Structure

```txt
.
├── data/
├── src/
│   ├── main.py
│   └── tsv_parser.py
├── pyproject.toml
└── README.md
```
