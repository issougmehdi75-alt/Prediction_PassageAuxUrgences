"""Orchestration utilisée par l'application : évaluer puis prévoir."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import modeles as M


@dataclass
class Prevision:
    modele: str
    previsions: pd.DataFrame          # ds, yhat, yhat_lower, yhat_upper
    scores: dict | None               # MAE/RMSE/MAPE hors-échantillon du modèle
    scores_baseline: dict | None      # idem pour la baseline de référence
    nom_baseline: str
    protocole: str                    # description lisible du backtest


def prevoir_journalier(df: pd.DataFrame, n_jours: int) -> Prevision:
    H = 14
    plis = M.plis_possibles(len(df), H, min_train=60, voulu=8)  # même protocole que evaluer_modeles.py
    scores = scores_b = None
    if plis > 0:
        bt = M.backtest(df, M.prevoir_mlp, "D", H, plis, "MLP")
        bt_b = M.backtest(df, M.prevoir_naif_saisonnier, "D", H, plis, "Naïf saisonnier")
        scores, scores_b = bt.scores, bt_b.scores
        sigma = M.sigma_horizon(bt.erreurs, n_jours, plafond=float(df["y"].std()))
        protocole = f"{plis} fenêtres de {H} jours (les {plis * H} derniers jours), prévision récursive"
    else:
        sigma = np.full(n_jours, float(df["y"].std()))
        protocole = "historique trop court pour un backtest : intervalle = ± 1,96 × écart-type de la série"

    X, y = M.construire_features(df)
    modele = M.fabrique_mlp().fit(X, y)
    yhat = M.prevision_recursive(modele, df, n_jours)
    fc = pd.DataFrame({
        "ds": pd.date_range(df["ds"].iloc[-1] + pd.Timedelta(days=1), periods=n_jours, freq="D"),
        "yhat": yhat,
        "yhat_lower": np.maximum(0, yhat - M.Z95 * sigma),
        "yhat_upper": yhat + M.Z95 * sigma,
    })
    return Prevision("MLP (réseau de neurones, scikit-learn)", fc, scores, scores_b,
                     "Naïf saisonnier (J-7)", protocole)


def prevoir_mensuel(df: pd.DataFrame, n_mois: int) -> Prevision:
    plis = M.plis_possibles(len(df), 1, min_train=8, voulu=6)
    scores = scores_b = None
    if plis > 0:
        scores = M.backtest(df, M.prevoir_prophet, "MS", 1, plis, "Prophet").scores
        scores_b = M.backtest(df, M.prevoir_moyenne_mobile, "MS", 1, plis, "MM3").scores
        protocole = f"prévision à 1 mois, répétée sur les {plis} derniers mois"
    else:
        protocole = "historique trop court pour un backtest"
    fc = M.prophet_avec_intervalles(df, n_mois, "MS")
    detail = ("avec saisonnalité annuelle" if len(df) >= 24
              else "tendance seule — saisonnalité annuelle désactivée (< 24 mois d'historique)")
    return Prevision(f"Prophet ({detail})", fc, scores, scores_b,
                     "Moyenne mobile 3 mois", protocole)
