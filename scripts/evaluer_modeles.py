"""Calcule TOUTES les métriques affichées dans l'application et la documentation.

- tests de stationnarité (ADF, KPSS) sur les séries mensuelle et journalière
- backtest à origine glissante de chaque modèle (hors-échantillon)
- écrit le résultat dans results/metriques.json (lu par la page Introduction)

Usage :  python scripts/evaluer_modeles.py
Durée :  ~1 à 3 minutes (Prophet et SARIMA sont réentraînés à chaque pli).
"""

from __future__ import annotations

import json
import sys
import time
import warnings
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from urgences.donnees import charger_exemple  # noqa: E402
from urgences.modeles import MODELES_JOURNALIERS, MODELES_MENSUELS, backtest  # noqa: E402

warnings.filterwarnings("ignore")
SORTIE = Path(__file__).resolve().parent.parent / "results" / "metriques.json"

PROTOCOLE = {
    "journalier": {"horizon": 14, "plis": 8},   # 8 fenêtres de 14 jours = 112 derniers jours
    "mensuel": {"horizon": 1, "plis": 6},       # prévision à 1 mois, 6 derniers mois
}


def tests_stationnarite(y: np.ndarray, nom: str) -> list[dict]:
    from statsmodels.tsa.stattools import adfuller, kpss

    res = []
    for transfo, serie in (("niveau", y), ("différence d'ordre 1", np.diff(y))):
        adf = adfuller(serie, autolag="AIC")
        k = kpss(serie, regression="c", nlags="auto")
        res.append({
            "serie": nom, "transformation": transfo, "n": int(len(serie)),
            "adf_stat": round(float(adf[0]), 3), "adf_p": round(float(adf[1]), 4),
            "kpss_stat": round(float(k[0]), 3), "kpss_p": round(float(k[1]), 4),
            # ADF : H0 = racine unitaire ; KPSS : H0 = stationnaire
            "stationnaire": bool(adf[1] < 0.05 and k[1] > 0.05),
        })
    return res


def autocorrelations(y: np.ndarray, lags=(1, 7, 14)) -> dict[str, float]:
    from statsmodels.tsa.stattools import acf

    a = acf(y, nlags=max(lags), fft=True)
    return {str(l): round(float(a[l]), 3) for l in lags}


def evaluer(df, catalogue, freq, horizon, plis) -> list[dict]:
    lignes = []
    for nom, (fonction, baseline) in catalogue.items():
        t0 = time.time()
        r = backtest(df, fonction, freq, horizon, plis, nom)
        lignes.append({
            "modele": nom, "baseline": baseline,
            **{k: round(v, 2) for k, v in r.scores.items()},
            "duree_s": round(time.time() - t0, 1),
        })
        print(f"  {nom:<26} MAE={r.scores['MAE']:7.2f}  RMSE={r.scores['RMSE']:7.2f}  "
              f"MAPE={r.scores['MAPE']:5.2f}%  ({lignes[-1]['duree_s']} s)")
    return sorted(lignes, key=lambda d: d["MAE"])


def main() -> None:
    mensuel = charger_exemple("mensuel")
    journalier = charger_exemple("journalier")

    print("Tests de stationnarité…")
    stat = tests_stationnarite(mensuel["y"].to_numpy(float), "mensuelle") + \
        tests_stationnarite(journalier["y"].to_numpy(float), "journalière (simulée)")

    print("\nBacktest journalier :")
    pj = PROTOCOLE["journalier"]
    res_j = evaluer(journalier, MODELES_JOURNALIERS, "D", pj["horizon"], pj["plis"])

    # Plancher théorique : erreur de l'« oracle » qui connaît l'espérance de la
    # simulation, mesurée sur les mêmes jours que le backtest.
    from urgences.modeles import metriques
    from urgences.simulation import esperance
    n_test = pj["horizon"] * pj["plis"]
    oracle = esperance(mensuel).merge(journalier, on="ds", suffixes=("_att", "_obs")).tail(n_test)
    plancher = {k: round(v, 2) for k, v in metriques(oracle["y_obs"], oracle["y_att"]).items()}
    print(f"  {'Plancher théorique (oracle)':<26} MAE={plancher['MAE']:7.2f}")

    print("\nBacktest mensuel :")
    pm = PROTOCOLE["mensuel"]
    res_m = evaluer(mensuel, MODELES_MENSUELS, "MS", pm["horizon"], pm["plis"])

    sortie = {
        "genere_le": date.today().isoformat(),
        "donnees": {
            "mensuel": {"n": len(mensuel), "debut": str(mensuel["ds"].min().date()),
                        "fin": str(mensuel["ds"].max().date()),
                        "moyenne": round(float(mensuel["y"].mean()), 1)},
            "journalier": {"n": len(journalier), "debut": str(journalier["ds"].min().date()),
                           "fin": str(journalier["ds"].max().date()),
                           "moyenne": round(float(journalier["y"].mean()), 1),
                           "simule": True},
        },
        "protocole": PROTOCOLE,
        "stationnarite": stat,
        "acf_journalier": autocorrelations(journalier["y"].to_numpy(float)),
        "backtest_journalier": res_j,
        "plancher_journalier": plancher,
        "backtest_mensuel": res_m,
    }
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(json.dumps(sortie, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n→ {SORTIE}")


if __name__ == "__main__":
    main()
