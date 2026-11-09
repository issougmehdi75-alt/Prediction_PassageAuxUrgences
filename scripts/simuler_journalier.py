"""Génère la série JOURNALIÈRE simulée à partir des totaux MENSUELS.

Pourquoi ?  L'hôpital ne nous a fourni que des totaux mensuels. Pour pouvoir
développer et tester le mode « prévision journalière », chaque total mensuel
est réparti aléatoirement sur les jours du mois.

Méthode (reproductible, graine fixée) :
    1. probabilité de chaque jour ∝ profil hebdomadaire (hypothèse, voir ci-dessous)
    2. tirage multinomial du total du mois sur ses jours
       -> la somme des jours redonne EXACTEMENT le total mensuel réel
       -> la variabilité jour à jour est de type Poisson (≈ ±√moyenne)

⚠️  Les données journalières sont donc SIMULÉES. Le profil hebdomadaire est
une HYPOTHÈSE de simulation (pic du lundi, creux du week-end, ordre de grandeur
habituel dans la littérature sur les urgences), PAS une observation : un
modèle qui « retrouve » une saisonnalité de 7 jours ne fait que retrouver
cette hypothèse. Utiliser --sans-profil pour une répartition uniforme.

Usage :  python scripts/simuler_journalier.py [--sans-profil] [--graine 42]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from urgences.donnees import FICHIER_JOURNALIER, FICHIER_MENSUEL, lire_excel  # noqa: E402
from urgences.simulation import PROFIL_HEBDO, simuler  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sans-profil", action="store_true", help="répartition uniforme (pas d'effet jour de semaine)")
    ap.add_argument("--graine", type=int, default=42)
    args = ap.parse_args()

    mensuel, err, _ = lire_excel(FICHIER_MENSUEL, "mensuel")
    if err:
        raise SystemExit(err)
    jour = simuler(mensuel, np.ones(7) if args.sans_profil else PROFIL_HEBDO, args.graine)

    # contrôle : la somme par mois doit redonner les totaux réels
    verif = jour.groupby(jour["ds"].dt.to_period("M"))["y"].sum().to_numpy()
    assert np.array_equal(verif, mensuel["y"].round().astype(int).to_numpy())

    sortie = jour.rename(columns={"ds": "Date", "y": "Passages"})
    sortie["Date"] = sortie["Date"].dt.date
    sortie.to_excel(FICHIER_JOURNALIER, index=False, sheet_name="Journalier (simulé)")
    print(f"{len(sortie)} jours écrits dans data/{FICHIER_JOURNALIER.name} (sommes mensuelles vérifiées)")


if __name__ == "__main__":
    main()
