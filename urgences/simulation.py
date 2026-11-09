"""Désagrégation aléatoire des totaux mensuels en valeurs journalières.

Voir scripts/simuler_journalier.py pour la justification et l'usage.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# lundi … dimanche : HYPOTHÈSE de simulation (pas une observation)
PROFIL_HEBDO = np.array([1.08, 1.03, 1.00, 0.99, 1.00, 0.94, 0.96])


def _probas_mois(debut_mois: pd.Timestamp, profil: np.ndarray) -> tuple[pd.DatetimeIndex, np.ndarray]:
    jours = pd.date_range(debut_mois, debut_mois + pd.offsets.MonthEnd(0), freq="D")
    p = profil[jours.dayofweek]
    return jours, p / p.sum()


def simuler(mensuel: pd.DataFrame, profil: np.ndarray = PROFIL_HEBDO, graine: int = 42) -> pd.DataFrame:
    """Tirage multinomial : la somme des jours = total mensuel exact."""
    rng = np.random.default_rng(graine)
    lignes = []
    for ds, total in zip(mensuel["ds"], mensuel["y"].round().astype(int)):
        jours, p = _probas_mois(ds, profil)
        lignes += list(zip(jours, rng.multinomial(total, p)))
    return pd.DataFrame(lignes, columns=["ds", "y"])


def esperance(mensuel: pd.DataFrame, profil: np.ndarray = PROFIL_HEBDO) -> pd.DataFrame:
    """Valeur attendue de chaque jour sous le processus de simulation.

    Sert d'« oracle » : aucun modèle ne peut, en moyenne, faire mieux que cette
    prévision, car l'écart restant est du bruit aléatoire pur.
    """
    lignes = []
    for ds, total in zip(mensuel["ds"], mensuel["y"].round().astype(int)):
        jours, p = _probas_mois(ds, profil)
        lignes += list(zip(jours, total * p))
    return pd.DataFrame(lignes, columns=["ds", "y"])
