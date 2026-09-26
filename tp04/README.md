# Particle System

## Demo

![Demo](docs/demo.gif)

## Fonctionnement

Les particules ont une position, une vitesse et une force.

À chaque update :

- les différents fields appliquent leurs forces
- on calcule l'accélération
- on met à jour la vitesse
- puis la position

La simulation utilise un Euler semi-implicite.

Les particules peuvent aussi être générées progressivement pendant la simulation.

## Build

```bash
mkdir build
cd build
cmake ..
make
```

Puis :

```bash
./ParticlesSystem
```

## Contrôles

`P` permet de lancer la simulation.
`F` permet d'afficher / masquer les fields.

## Réutilisation de code

J'ai repris et adapté une partie du code venant de mon projet `fluid-simulator`, principalement pour éviter de refaire certaines bases que j'avais déjà.

Repo : [fluid-simulator](https://github.com/JustARandomBadDev/fluid-simulator)
