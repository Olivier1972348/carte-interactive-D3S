"""Lecture du classeur Excel source."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def load_posts_excel(input_path: Path, sheet_name: str | None = "Postes") -> pd.DataFrame:
    """Lit l'onglet Postes si disponible, sinon le premier onglet du classeur."""
    if not input_path.exists():
        raise FileNotFoundError(f"Fichier Excel introuvable: {input_path}")

    with pd.ExcelFile(input_path, engine="openpyxl") as excel_file:
        available_sheets = excel_file.sheet_names
    if not available_sheets:
        raise ValueError(f"Aucun onglet trouve dans le classeur: {input_path}")

    if sheet_name and sheet_name not in available_sheets:
        raise ValueError(
            f"Onglet '{sheet_name}' introuvable dans {input_path}. "
            f"Onglets disponibles: {', '.join(available_sheets)}"
        )
    selected_sheet = sheet_name or available_sheets[0]

    logger.info("Lecture du fichier Excel: %s", input_path)
    logger.info("Onglet utilise: %s", selected_sheet)
    return pd.read_excel(input_path, sheet_name=selected_sheet, engine="openpyxl")
