"""Réduit le référentiel FINESS aux colonnes réellement utilisées par la carte."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = PROJECT_ROOT / "data" / "referentiel_finess.csv"
USEFUL_COLUMNS = ["numero_finess_et", "coord", "sourcecoordet", "raison_sociale"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_PATH)
    return parser.parse_args()


def compact(input_path: Path, output_path: Path) -> None:
    with input_path.open("rb") as stream:
        header = stream.readline()
    separator = ";" if b";" in header else ","
    frame = pd.read_csv(
        input_path, sep=separator, dtype=str, usecols=USEFUL_COLUMNS,
        engine="c", on_bad_lines="skip"
    ).fillna("")
    finess_digits = frame["numero_finess_et"].str.replace(r"\D", "", regex=True)
    frame = frame[finess_digits.ne("") & frame["coord"].ne("")].copy()
    frame["numero_finess_et"] = finess_digits.loc[frame.index].str.zfill(9)
    frame = frame.drop_duplicates("numero_finess_et", keep="first")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(suffix=".csv", dir=output_path.parent, delete=False) as handle:
        temporary_path = Path(handle.name)
    try:
        frame.to_csv(temporary_path, sep=";", index=False, encoding="utf-8-sig")
        os.replace(temporary_path, output_path)
        os.chmod(output_path, 0o644)
    finally:
        temporary_path.unlink(missing_ok=True)
    print(f"Référentiel compact créé: {output_path} ({len(frame)} FINESS)")


def main() -> int:
    args = parse_args()
    compact(args.input.resolve(), args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
