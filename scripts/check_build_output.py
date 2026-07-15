"""Controle minimal du site statique genere."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"

REQUIRED_FILES = [
    OUTPUT_DIR / "index.html",
    OUTPUT_DIR / "carte_d3s.html",
    OUTPUT_DIR / "promotion-logo.jpeg",
    OUTPUT_DIR / "plaquette-promo.pdf",
]

REQUIRED_MARKERS = [
    "Carte interactive des avis de vacance D3S",
    "Constance Pascal",
    "Consulter Plaquette Promo",
    'id="map"',
    "tile.openstreetmap.fr/osmfr",
    "dna.d3s@edu.ehesp.fr",
]


def main() -> int:
    missing_files = [path for path in REQUIRED_FILES if not path.exists()]
    if missing_files:
        for path in missing_files:
            print(f"Fichier attendu absent: {path}")
        return 1

    index_html = (OUTPUT_DIR / "index.html").read_text(encoding="utf-8")
    missing_markers = [marker for marker in REQUIRED_MARKERS if marker not in index_html]
    if missing_markers:
        for marker in missing_markers:
            print(f"Marqueur HTML attendu absent: {marker}")
        return 1

    if (OUTPUT_DIR / "index.html").read_text(encoding="utf-8") != (
        OUTPUT_DIR / "carte_d3s.html"
    ).read_text(encoding="utf-8"):
        print("index.html et carte_d3s.html ne contiennent pas le meme HTML.")
        return 1

    plaquette = OUTPUT_DIR / "plaquette-promo.pdf"
    if plaquette.stat().st_size < 10_000:
        print(
            "AVERTISSEMENT: plaquette-promo.pdf semble être un fichier provisoire; "
            "le remplacer avant diffusion officielle."
        )

    print("Controle du site statique OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
