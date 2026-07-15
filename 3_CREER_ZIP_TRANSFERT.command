#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

archive="ED3S_Carte_V3_transfert.zip"
temporary="${archive%.zip}.tmp.zip"

rm -f "$temporary"
zip -r -q "$temporary" . \
  -x '.git/*' '.venv/*' '__pycache__' '__pycache__/*' '*/__pycache__/*' '*.pyc' '.DS_Store' '*/.DS_Store' \
     '.pytest_cache/*' '.mypy_cache/*' '.ruff_cache/*' '*.zip' \
     'DEPLOIEMENT_RENDER.md' 'lves_d3s_promotion_2025_2026_logo.jpeg'
mv "$temporary" "$archive"

echo "Archive de transfert créée : $archive"
echo "Pensez à remplacer la plaquette provisoire avant l'envoi officiel."
