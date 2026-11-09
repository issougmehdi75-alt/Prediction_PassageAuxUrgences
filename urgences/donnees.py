"""Lecture et validation des fichiers Excel de passages aux urgences."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FICHIER_MENSUEL = DATA_DIR / "passages_mensuels.xlsx"
FICHIER_JOURNALIER = DATA_DIR / "passages_journaliers_simules.xlsx"

MIN_MENSUEL = 8      # en dessous, aucun modèle mensuel n'a de sens
MIN_JOURNALIER = 60  # lags 14 j + validation sur plusieurs semaines

# Mois français (et abréviations courantes) -> numéro de mois.
# pandas ne reconnaît que les noms anglais : "Janvier 2024" donnait NaT.
_MOIS_FR = {
    "janvier": 1, "janv": 1, "jan": 1,
    "fevrier": 2, "fevr": 2, "fev": 2, "feb": 2,
    "mars": 3, "mar": 3,
    "avril": 4, "avr": 4, "apr": 4,
    "mai": 5, "may": 5,
    "juin": 6, "jun": 6,
    "juillet": 7, "juil": 7, "jul": 7,
    "aout": 8, "aou": 8, "aug": 8,
    "septembre": 9, "sept": 9, "sep": 9,
    "octobre": 10, "oct": 10,
    "novembre": 11, "nov": 11,
    "decembre": 12, "dec": 12,
}


def _sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _parse_mois_texte(s: str) -> pd.Timestamp | None:
    """Parse « Janvier 2024 », « janv. 2024 », « Jan-2024 »…"""
    m = re.fullmatch(r"([a-z]+)\.?[\s\-/]*(\d{4})", _sans_accents(s.strip().lower()))
    if not m or m.group(1) not in _MOIS_FR:
        return None
    return pd.Timestamp(year=int(m.group(2)), month=_MOIS_FR[m.group(1)], day=1)


def parse_date(valeur) -> pd.Timestamp | None:
    """Convertit une cellule Excel (datetime, texte ISO, jj/mm/aaaa, mois en lettres) en Timestamp."""
    if valeur is None or (isinstance(valeur, float) and pd.isna(valeur)):
        return None
    if isinstance(valeur, pd.Timestamp):
        return valeur
    if hasattr(valeur, "year") and hasattr(valeur, "month"):  # datetime / date
        return pd.Timestamp(valeur)
    s = str(valeur).strip()
    if not s:
        return None
    mois = _parse_mois_texte(s)
    if mois is not None:
        return mois
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%m/%Y", "%Y-%m"):
        try:
            return pd.to_datetime(s, format=fmt)
        except (ValueError, TypeError):
            continue
    return None


def _parse_nombre(valeur) -> float | None:
    if valeur is None:
        return None
    if isinstance(valeur, (int, float)):
        return None if pd.isna(valeur) else float(valeur)
    s = str(valeur).strip().replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def lire_excel(source, granularite: str = "mensuel") -> tuple[pd.DataFrame | None, str | None, list[str]]:
    """Lit un fichier Excel à 2 colonnes (date, passages).

    Retourne (df[ds, y], erreur, avertissements). Les lignes d'en-tête ou non
    numériques sont ignorées ; les doublons sont agrégés (somme) ; les trous
    du calendrier sont signalés.
    """
    avert: list[str] = []
    try:
        brut = pd.read_excel(source, header=None)
    except Exception as e:  # fichier corrompu, mauvais format…
        return None, f"Impossible de lire le fichier Excel : {e}", avert

    brut = brut.dropna(how="all", axis=1).dropna(how="all", axis=0)
    if brut.shape[1] < 2:
        return None, "Le fichier doit contenir 2 colonnes : Date et Nombre de passages.", avert
    if brut.shape[1] > 2:
        avert.append(f"{brut.shape[1]} colonnes détectées : seules les 2 premières sont utilisées.")

    lignes = []
    ignorees = 0
    for d, v in zip(brut.iloc[:, 0], brut.iloc[:, 1]):
        ds, y = parse_date(d), _parse_nombre(v)
        if ds is None or y is None or y < 0:
            ignorees += 1
            continue
        lignes.append((ds, y))

    if not lignes:
        return None, "Aucune ligne valide (date + nombre positif) n'a été trouvée.", avert
    if ignorees > 1:  # 1 ligne ignorée = l'en-tête, c'est normal
        avert.append(f"{ignorees} lignes ignorées (en-tête, date illisible ou valeur non numérique).")

    df = pd.DataFrame(lignes, columns=["ds", "y"])
    if granularite == "mensuel":
        df["ds"] = df["ds"].dt.to_period("M").dt.to_timestamp()
        freq, mini, unite = "MS", MIN_MENSUEL, "mois"
    else:
        df["ds"] = df["ds"].dt.normalize()
        freq, mini, unite = "D", MIN_JOURNALIER, "jours"

    n_avant = len(df)
    df = df.groupby("ds", as_index=False)["y"].sum().sort_values("ds").reset_index(drop=True)
    if len(df) < n_avant:
        avert.append(f"{n_avant - len(df)} dates en double ont été additionnées.")

    if len(df) < mini:
        return None, f"Seulement {len(df)} {unite} valides : minimum {mini} requis pour ce mode.", avert

    calendrier = pd.date_range(df["ds"].min(), df["ds"].max(), freq=freq)
    manquants = len(calendrier) - len(df)
    if manquants > 0:
        avert.append(f"{manquants} {unite} manquants dans la série : complétés par interpolation linéaire.")
        df = df.set_index("ds").reindex(calendrier).rename_axis("ds")
        df["y"] = df["y"].interpolate()
        df = df.reset_index()

    if granularite == "mensuel" and df["y"].median() < 500:
        avert.append("Valeurs faibles pour des totaux mensuels : s'agit-il de données journalières ?")
    if granularite == "journalier" and df["y"].median() > 2000:
        avert.append("Valeurs élevées pour des données journalières : s'agit-il de totaux mensuels ?")

    return df, None, avert


def charger_exemple(granularite: str) -> pd.DataFrame:
    """Charge le jeu de données fourni avec le projet."""
    chemin = FICHIER_MENSUEL if granularite == "mensuel" else FICHIER_JOURNALIER
    df, err, _ = lire_excel(chemin, granularite)
    if err:
        raise RuntimeError(f"{chemin.name} : {err}")
    return df
