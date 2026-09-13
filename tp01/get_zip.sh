#!/bin/sh
set -e

pandoc README.md -o rapport.pdf \
  -V geometry:margin=3cm

zip rendu.zip fichier.pdf main.py