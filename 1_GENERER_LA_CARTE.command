#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "==============================================="
echo " Generation de la carte interactive D3S"
echo "==============================================="
echo

if [ ! -f "data/postes_d3s.xlsx" ]; then
  echo "ERREUR : le fichier data/postes_d3s.xlsx est introuvable."
  echo "Placez le fichier Excel source dans le dossier data et nommez-le postes_d3s.xlsx."
  echo
  read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
  exit 1
fi

if [ ! -f "data/referentiel_finess.csv" ]; then
  echo "ERREUR : le fichier data/referentiel_finess.csv est introuvable."
  echo "Ce fichier est necessaire pour ameliorer les coordonnees FINESS."
  echo
  read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
  exit 1
fi

if [ -x ".venv/bin/python" ] && ".venv/bin/python" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))'; then
  PYTHON=".venv/bin/python"
else
  if ! command -v python3 >/dev/null 2>&1; then
    echo "ERREUR : Python 3 est introuvable sur ce Mac."
    echo "Installez Python 3 depuis https://www.python.org/downloads/"
    echo "puis relancez ce script."
    echo
    read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
    exit 1
  fi

  if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 11))'; then
    echo "ERREUR : Python 3.11 ou plus recent est necessaire."
    echo "Installez une version recente depuis https://www.python.org/downloads/"
    echo
    read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
    exit 1
  fi

  echo "Premiere utilisation : creation de l'environnement Python local..."
  python3 -m venv .venv
  PYTHON=".venv/bin/python"
fi

echo "Installation ou verification des dependances..."
"$PYTHON" -m pip install -r requirements.txt
echo

echo "Generation de la carte..."
"$PYTHON" main.py
echo

echo "Verification des fichiers generes..."
"$PYTHON" scripts/check_build_output.py
echo

if [ -f "output/carte_d3s.html" ]; then
  echo "Carte generee : output/carte_d3s.html"
  open "output/carte_d3s.html"
else
  echo "ERREUR : la carte n'a pas ete generee."
  read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
  exit 1
fi

echo
echo "Termine. Pour un envoi direct, transmettez le dossier output complet."
echo
read -r -p "Appuyez sur Entree pour fermer cette fenetre..."
