"""Modèles de prévision, baselines et évaluation hors-échantillon (backtest).

Principes appliqués (corrections par rapport à la v1) :

- les erreurs affichées sont mesurées HORS-ÉCHANTILLON, par validation à
  origine glissante (« rolling-origin backtest »), jamais sur les données
  ayant servi à l'entraînement ;
- le MLP est évalué en mode récursif, exactement comme il est utilisé pour
  prévoir (ses propres prévisions alimentent les lags) ;
- chaque modèle est comparé à des baselines naïves : un modèle qui ne bat
  pas la baseline n'apporte rien ;
- l'intervalle de prévision du MLP s'élargit avec l'horizon.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

for _nom in ("prophet", "cmdstanpy"):
    logging.getLogger(_nom).setLevel(logging.ERROR)
    logging.getLogger(_nom).propagate = False

Z95 = 1.96
LAGS = (1, 2, 3, 7, 14)
FENETRES = (7, 14)


# ──────────────────────────────────────────────────────────────
#  Métriques
# ──────────────────────────────────────────────────────────────
def metriques(y_true, y_pred) -> dict[str, float]:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    err = y_true - y_pred
    return {
        "MAE": float(np.mean(np.abs(err))),
        "RMSE": float(np.sqrt(np.mean(err**2))),
        "MAPE": float(np.mean(np.abs(err) / np.maximum(y_true, 1)) * 100),
    }


# ──────────────────────────────────────────────────────────────
#  Baselines
# ──────────────────────────────────────────────────────────────
def prevoir_naif(hist: pd.DataFrame, h: int, freq: str) -> np.ndarray:
    """Dernière valeur observée répétée."""
    return np.repeat(hist["y"].iloc[-1], h).astype(float)


def prevoir_naif_saisonnier(hist: pd.DataFrame, h: int, freq: str, saison: int = 7) -> np.ndarray:
    """Valeur du même jour la semaine précédente (journalier)."""
    der = hist["y"].iloc[-saison:].to_numpy(float)
    return np.array([der[i % saison] for i in range(h)])


def prevoir_moyenne_mobile(hist: pd.DataFrame, h: int, freq: str) -> np.ndarray:
    k = 7 if freq == "D" else 3
    return np.repeat(hist["y"].iloc[-k:].mean(), h).astype(float)


# ──────────────────────────────────────────────────────────────
#  Prophet
# ──────────────────────────────────────────────────────────────
def _prophet(hist: pd.DataFrame, freq: str, interval_width: float = 0.95):
    from prophet import Prophet

    for nom in ("prophet", "cmdstanpy"):  # Prophet réinstalle ses handlers à l'import
        logging.getLogger(nom).setLevel(logging.ERROR)

    if freq == "MS":
        # La saisonnalité annuelle ne peut pas être estimée avec moins de
        # 2 cycles complets : avec 17 mois elle sur-apprend le bruit.
        annuelle = len(hist) >= 24
        m = Prophet(
            yearly_seasonality=annuelle, weekly_seasonality=False, daily_seasonality=False,
            changepoint_prior_scale=0.05, interval_width=interval_width,
        )
    else:
        m = Prophet(
            yearly_seasonality=len(hist) >= 730, weekly_seasonality=True, daily_seasonality=False,
            changepoint_prior_scale=0.05, interval_width=interval_width,
        )
    m.fit(hist[["ds", "y"]])
    return m


def prevoir_prophet(hist: pd.DataFrame, h: int, freq: str) -> np.ndarray:
    m = _prophet(hist, freq)
    fut = m.make_future_dataframe(periods=h, freq=freq, include_history=False)
    return m.predict(fut)["yhat"].to_numpy()


def prophet_avec_intervalles(hist: pd.DataFrame, h: int, freq: str) -> pd.DataFrame:
    m = _prophet(hist, freq)
    fut = m.make_future_dataframe(periods=h, freq=freq, include_history=False)
    fc = m.predict(fut)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    fc[["yhat", "yhat_lower", "yhat_upper"]] = fc[["yhat", "yhat_lower", "yhat_upper"]].clip(lower=0)
    return fc.reset_index(drop=True)


# ──────────────────────────────────────────────────────────────
#  SARIMA (journalier, saison 7)
# ──────────────────────────────────────────────────────────────
def prevoir_sarima(hist: pd.DataFrame, h: int, freq: str) -> np.ndarray:
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    res = SARIMAX(
        hist["y"].to_numpy(float), order=(1, 1, 1), seasonal_order=(1, 0, 1, 7),
        enforce_stationarity=False, enforce_invertibility=False,
    ).fit(disp=False)
    return res.forecast(h)


# ──────────────────────────────────────────────────────────────
#  Modèles ML journaliers (features + prévision récursive)
# ──────────────────────────────────────────────────────────────
def _features_calendrier(d: pd.Timestamp) -> dict[str, float]:
    return {
        "dow_sin": np.sin(2 * np.pi * d.dayofweek / 7),
        "dow_cos": np.cos(2 * np.pi * d.dayofweek / 7),
        "month_sin": np.sin(2 * np.pi * (d.month - 1) / 12),
        "month_cos": np.cos(2 * np.pi * (d.month - 1) / 12),
        "weekend": float(d.dayofweek >= 5),
    }


def _features_ligne(d: pd.Timestamp, passe: np.ndarray) -> dict[str, float]:
    """Features pour la date d à partir des valeurs STRICTEMENT antérieures (pas de fuite)."""
    f = _features_calendrier(d)
    for lag in LAGS:
        f[f"lag_{lag}"] = passe[-lag]
    for w in FENETRES:
        f[f"roll_{w}"] = passe[-w:].mean()
    return f


def construire_features(df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    """Matrice X / cible y. Les 14 premiers jours (lags incomplets) sont exclus
    au lieu d'être remplis par bfill (qui injectait des valeurs futures)."""
    y = df["y"].to_numpy(float)
    debut = max(max(LAGS), max(FENETRES))
    lignes = [_features_ligne(df["ds"].iloc[i], y[:i]) for i in range(debut, len(df))]
    return pd.DataFrame(lignes), y[debut:]


def fabrique_mlp(graine: int = 42):
    from sklearn.compose import TransformedTargetRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    mlp = MLPRegressor(
        hidden_layer_sizes=(64, 32), activation="relu", alpha=1e-2,
        learning_rate_init=1e-3, max_iter=2000, early_stopping=True,
        validation_fraction=0.15, n_iter_no_change=30, random_state=graine,
    )
    return TransformedTargetRegressor(regressor=make_pipeline(StandardScaler(), mlp), transformer=StandardScaler())


def fabrique_gbm(graine: int = 42):
    from sklearn.ensemble import HistGradientBoostingRegressor

    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                         l2_regularization=1.0, random_state=graine)


def fabrique_ridge(graine: int = 42):
    from sklearn.linear_model import RidgeCV
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    return make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 20)))


def prevision_recursive(modele, hist: pd.DataFrame, h: int) -> np.ndarray:
    passe = list(hist["y"].to_numpy(float))
    d = hist["ds"].iloc[-1]
    preds = []
    for _ in range(h):
        d = d + pd.Timedelta(days=1)
        x = pd.DataFrame([_features_ligne(d, np.asarray(passe))])
        p = max(0.0, float(modele.predict(x)[0]))
        preds.append(p)
        passe.append(p)
    return np.array(preds)


def _prevoir_ml(fabrique) -> Callable:
    def f(hist: pd.DataFrame, h: int, freq: str) -> np.ndarray:
        X, y = construire_features(hist)
        m = fabrique().fit(X, y)
        return prevision_recursive(m, hist, h)
    return f


prevoir_mlp = _prevoir_ml(fabrique_mlp)
prevoir_gbm = _prevoir_ml(fabrique_gbm)
prevoir_ridge = _prevoir_ml(fabrique_ridge)


# ──────────────────────────────────────────────────────────────
#  Catalogue
# ──────────────────────────────────────────────────────────────
MODELES_JOURNALIERS: dict[str, tuple[Callable, bool]] = {
    # nom: (fonction, est_baseline)
    "Naïf (veille)": (prevoir_naif, True),
    "Naïf saisonnier (J-7)": (prevoir_naif_saisonnier, True),
    "Moyenne mobile 7 j": (prevoir_moyenne_mobile, True),
    "SARIMA(1,1,1)(1,0,1)₇": (prevoir_sarima, False),
    "Prophet": (prevoir_prophet, False),
    "Ridge (features)": (prevoir_ridge, False),
    "Gradient Boosting": (prevoir_gbm, False),
    "MLP": (prevoir_mlp, False),
}

MODELES_MENSUELS: dict[str, tuple[Callable, bool]] = {
    "Naïf (mois précédent)": (prevoir_naif, True),
    "Moyenne mobile 3 mois": (prevoir_moyenne_mobile, True),
    "Prophet": (prevoir_prophet, False),
}


# ──────────────────────────────────────────────────────────────
#  Backtest à origine glissante
# ──────────────────────────────────────────────────────────────
@dataclass
class ResultatBacktest:
    modele: str
    horizon: int
    n_plis: int
    erreurs: np.ndarray            # (n_plis, horizon) : réel - prévu
    reels: np.ndarray
    prevus: np.ndarray
    scores: dict[str, float] = field(default_factory=dict)


def backtest(df: pd.DataFrame, fonction: Callable, freq: str, horizon: int, n_plis: int,
             nom: str = "") -> ResultatBacktest:
    """Pour chaque pli k : entraîne sur tout ce qui précède l'origine, prévoit
    `horizon` pas, compare au réel. Les plis sont consécutifs et ne se chevauchent pas."""
    n = len(df)
    erreurs, reels, prevus = [], [], []
    for k in range(n_plis, 0, -1):
        origine = n - k * horizon
        hist, test = df.iloc[:origine], df.iloc[origine:origine + horizon]
        p = np.asarray(fonction(hist, horizon, freq), float)
        reels.append(test["y"].to_numpy(float))
        prevus.append(p)
        erreurs.append(reels[-1] - p)
    r = ResultatBacktest(nom, horizon, n_plis, np.array(erreurs), np.array(reels), np.array(prevus))
    r.scores = metriques(r.reels.ravel(), r.prevus.ravel())
    return r


def sigma_horizon(erreurs: np.ndarray, h_max: int, plafond: float) -> np.ndarray:
    """Écart-type de l'erreur en fonction de l'horizon h.

    Hypothèse : Var(e_h) = c²·h (l'incertitude s'accumule avec la récursion).
    c est estimé par maximum de vraisemblance sur les erreurs du backtest,
    puis σ(h) est plafonné par l'écart-type de la série (une prévision ne
    peut raisonnablement pas être plus incertaine que la série elle-même).
    """
    _, H = erreurs.shape
    h = np.arange(1, H + 1)
    c = np.sqrt(np.sum(erreurs**2) / (erreurs.shape[0] * h.sum()))
    return np.minimum(c * np.sqrt(np.arange(1, h_max + 1)), plafond)


def plis_possibles(n: int, horizon: int, min_train: int, voulu: int) -> int:
    return int(max(0, min(voulu, (n - min_train) // horizon)))
