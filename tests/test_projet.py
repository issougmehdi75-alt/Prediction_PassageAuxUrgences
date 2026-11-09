"""Tests rapides : python -m pytest -q"""

import sys
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from urgences import modeles as M  # noqa: E402
from urgences.donnees import charger_exemple, lire_excel, parse_date  # noqa: E402
from urgences.simulation import simuler  # noqa: E402


def _excel(df: pd.DataFrame) -> BytesIO:
    b = BytesIO()
    df.to_excel(b, index=False)
    b.seek(0)
    return b


@pytest.mark.parametrize("texte,attendu", [
    ("Janvier 2024", "2024-01-01"), ("févr. 2025", "2025-02-01"), ("Décembre 2023", "2023-12-01"),
    ("2024-03-15", "2024-03-15"), ("15/03/2024", "2024-03-15"), ("Jan 2024", "2024-01-01"),
])
def test_parse_date(texte, attendu):
    assert parse_date(texte) == pd.Timestamp(attendu)


def test_lecture_mois_en_francais():
    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre"]
    df, err, _ = lire_excel(_excel(pd.DataFrame({"Mois": [f"{m} 2024" for m in mois], "Passages": range(7000, 7010)})))
    assert err is None and len(df) == 10 and df["ds"].iloc[7] == pd.Timestamp("2024-08-01")


def test_trous_et_doublons_journaliers():
    dates = list(pd.date_range("2024-01-01", periods=80, freq="D"))
    dates = dates[:10] + dates[12:] + [dates[20]]  # 2 jours manquants + 1 doublon
    df, err, avert = lire_excel(_excel(pd.DataFrame({"Date": dates, "Passages": 240})), "journalier")
    assert err is None and len(df) == 80
    assert any("manquants" in a for a in avert) and any("double" in a for a in avert)


def test_trop_peu_de_lignes():
    _, err, _ = lire_excel(_excel(pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=5, freq="MS"), "y": 1})))
    assert err and "minimum" in err


def test_simulation_conserve_totaux_mensuels():
    mensuel = charger_exemple("mensuel")
    jour = simuler(mensuel)
    sommes = jour.groupby(jour["ds"].dt.to_period("M"))["y"].sum().to_numpy()
    assert np.array_equal(sommes, mensuel["y"].round().astype(int).to_numpy())


def test_features_sans_fuite():
    """Les features de la ligne i ne doivent dépendre que des valeurs < i."""
    df = pd.DataFrame({"ds": pd.date_range("2024-01-01", periods=40, freq="D"), "y": np.arange(40.0)})
    X, y = M.construire_features(df)
    assert (X["lag_1"].to_numpy() == y - 1).all()
    df2 = df.copy()
    df2.loc[30:, "y"] = 1e6  # modifier le futur ne change pas les features du passé
    X2, _ = M.construire_features(df2)
    pd.testing.assert_frame_equal(X.iloc[:17], X2.iloc[:17])


def test_backtest_et_intervalle_croissant():
    df = charger_exemple("journalier")
    r = M.backtest(df, M.prevoir_naif_saisonnier, "D", 14, 3)
    assert r.erreurs.shape == (3, 14) and r.scores["MAE"] > 0
    s = M.sigma_horizon(r.erreurs, 30, plafond=1e9)
    assert (np.diff(s) > 0).all()
