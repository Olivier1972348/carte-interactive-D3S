"""Generation du fichier HTML autonome a partir du template Jinja2."""

from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.utils import ensure_parent_dir


logger = logging.getLogger(__name__)


def render_map_html(posts: pd.DataFrame, config: dict[str, Any]) -> None:
    """Rend la carte HTML avec les donnees integrees en JSON."""
    template_path = config["template_path"]
    if not template_path.exists():
        raise FileNotFoundError(f"Template HTML introuvable: {template_path}")

    records = posts.where(pd.notna(posts), None).to_dict(orient="records")
    posts_json = json_for_html(records)
    category_colors_json = json_for_html(config["category_colors"])

    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
    )
    template = env.get_template(template_path.name)
    html = template.render(
        posts_json=posts_json,
        category_colors_json=category_colors_json,
        total_posts=len(records),
        title=config["title"],
        subtitle=config["subtitle"],
        institution_label=config["institution_label"],
        default_missing_value=config["default_missing_value"],
        map_center_lat=config["map_center_lat"],
        map_center_lon=config["map_center_lon"],
        map_zoom=config["map_zoom"],
        marker_cluster_enabled=str(config["marker_cluster_enabled"]).lower(),
    )

    output_path = config["output_html_path"]
    ensure_parent_dir(output_path)
    output_path.write_text(html, encoding="utf-8")
    logger.info("HTML genere: %s", output_path)

    index_path = config.get("output_index_html_path") or output_path.with_name("index.html")
    if index_path != output_path:
        ensure_parent_dir(index_path)
        index_path.write_text(html, encoding="utf-8")
        logger.info("HTML index genere: %s", index_path)

    copy_static_assets(config, output_path.parent)


def json_for_html(value: Any) -> str:
    """Encode du JSON sans permettre de fermer le bloc script HTML."""
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def copy_static_assets(config: dict[str, Any], output_dir: Path) -> None:
    """Copie les assets statiques utiles au site publie."""
    static_dir = config["project_root"] / "static"
    if not static_dir.exists():
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for source_path in static_dir.iterdir():
        if source_path.is_file():
            destination_path = output_dir / source_path.name
            shutil.copy2(source_path, destination_path)
            logger.info("Asset statique copie: %s", destination_path)
