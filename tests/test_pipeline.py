from __future__ import annotations

import tempfile
import unittest
import subprocess
from pathlib import Path

import pandas as pd

from src.config_loader import load_config
from src.data_cleaner import standardize_posts
from src.data_loader import load_posts_excel
from src.html_renderer import json_for_html


class PipelineTests(unittest.TestCase):
    def test_mac_generator_script_has_valid_bash_syntax(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["bash", "-n", str(project_root / "1_GENERER_LA_CARTE.command")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_minimal_excel_uses_finess_date_and_excludes_inactive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "finess.csv"
            reference.write_text(
                "numero_finess_et;coord;sourcecoordet;raison_sociale\n"
                "012345678;48.5, 2.2;FINESS test;HOPITAL TEST\n",
                encoding="utf-8",
            )
            config = load_config()
            config["finess_reference_csv_path"] = reference
            raw = pd.DataFrame(
                [
                    {
                        "Actif ?": "Oui", "Poste": "Direction", "Catégorie": "Chef d'établissement",
                        "Établissement(s)": "Hôpital test", "FINESS": "012345678",
                        "Date de parution": "2026-07-15",
                    },
                    {
                        "Actif ?": "Non", "Poste": "Ancien poste", "Catégorie": "Directeur adjoint",
                        "Établissement(s)": "Hôpital test", "FINESS": "012345678",
                        "Date de parution": "2026-07-15",
                    },
                ]
            )
            result = standardize_posts(raw, config)

        self.assertEqual(result.rows_read, 2)
        self.assertEqual(result.inactive_count, 1)
        self.assertEqual(result.valid_count, 1)
        post = result.valid_posts.iloc[0]
        self.assertEqual(post["mois_parution"], "7")
        self.assertEqual(post["annee_parution"], "2026")
        self.assertEqual(post["raison_sociale_finess"], "HOPITAL TEST")
        self.assertAlmostEqual(post["latitude"], 48.5)

    def test_manual_coordinates_work_without_finess_or_coordinate_headers_pair(self) -> None:
        config = load_config()
        config["finess_reference_csv_path"] = None
        raw = pd.DataFrame(
            [{"Poste": "Direction", "Catégorie": "Directeur adjoint", "Établissement(s)": "EHPAD test", "Latitude": "48,1", "Longitude": "2,3"}]
        )
        result = standardize_posts(raw, config)
        self.assertEqual(result.valid_count, 1)

    def test_json_is_safe_inside_script_tag(self) -> None:
        encoded = json_for_html({"value": "</script><script>alert(1)</script>"})
        self.assertNotIn("</script>", encoded)
        self.assertIn("\\u003c", encoded)

    def test_missing_configured_sheet_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.xlsx"
            pd.DataFrame([{"Poste": "x"}]).to_excel(path, sheet_name="Autre", index=False)
            with self.assertRaisesRegex(ValueError, "Onglet 'Postes' introuvable"):
                load_posts_excel(path, "Postes")

    def test_missing_required_business_column_fails(self) -> None:
        config = load_config()
        raw = pd.DataFrame([{"Poste": "Direction", "Catégorie": "Directeur adjoint"}])
        with self.assertRaisesRegex(ValueError, "etablissements"):
            standardize_posts(raw, config)


if __name__ == "__main__":
    unittest.main()
