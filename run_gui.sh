#!/bin/bash
# Script de lancement de l'interface GUI

cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer la GUI
python3 gui.py
