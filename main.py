"""Point d'entree de generation de la carte D3S."""

from __future__ import annotations

import logging
import sys

from src.config_loader import load_config
from src.data_cleaner import export_control_csv, standardize_posts
from src.data_loader import load_posts_excel
from src.html_renderer import render_map_html
from src.utils import setup_logging


logger = logging.getLogger(__name__)


def main() -> int:
    """Execute le pipeline complet de generation."""
    setup_logging()
    try:
        config = load_config()
        raw_posts = load_posts_excel(config["input_excel_path"], config.get("sheet_name"))
        clean_result = standardize_posts(raw_posts, config)
        export_control_csv(clean_result, config)
        render_map_html(clean_result.valid_posts, config)

        logger.info("Resume de generation")
        logger.info("Lignes lues: %s", clean_result.rows_read)
        logger.info("Postes inactifs ou retires exclus: %s", clean_result.inactive_count)
        logger.info("Postes valides avec coordonnees: %s", clean_result.valid_count)
        logger.info("Postes sans coordonnees exploitables: %s", clean_result.missing_coords_count)
        logger.info("Doublons supprimes: %s", clean_result.duplicates_removed)
        logger.info("Carte HTML: %s", config["output_html_path"])
        return 0
    except Exception as exc:
        logger.exception("Generation interrompue: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
