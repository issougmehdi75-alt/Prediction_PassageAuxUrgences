.. _analyse_statistique:

Analyse statistique
===================

Résultats des analyses statistiques préliminaires conduites sur les données
de l'Hôpital Mohamed V avant de choisir les modèles de prédiction.

.. contents::
   :local:
   :depth: 2

----

Description des données
------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Source**
     - Registres de l'Hôpital Mohamed V, Meknès
   * - **Période**
     - Janvier 2024 — Mai 2025
   * - **Granularité initiale**
     - Mensuelle (agrégats mensuels des passages)
   * - **Désagrégation**
     - Répartition uniforme par jour dans le mois (mensuel → journalier)
   * - **Variable cible**
     - Nombre de passages aux urgences (entier positif)
   * - **Observations mensuelles**
     - 17 mois
   * - **Observations journalières**
     - ~520 jours (après désagrégation)

----

Analyse préliminaire
---------------------

Statistiques descriptives
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sur les données mensuelles :

- **Minimum** : ~6 000 passages/mois
- **Maximum** : ~8 000 passages/mois
- **Moyenne** : ~7 200 passages/mois
- **Écart-type** : ~450 passages/mois

Tendances observées
^^^^^^^^^^^^^^^^^^^

- Légère **tendance haussière** sur la période d'observation
- **Saisonnalité** : variation cyclique avec des pics en hiver (janvier) et été (juillet–août)
- **Variabilité** : coefficients de variation faibles — série relativement stable

----

Tests de stationnarité
-----------------------

La stationnarité est une propriété fondamentale pour les modèles ARIMA et statistiques.
Une série est stationnaire si sa moyenne, variance et autocovariance sont constantes dans le temps.

Test ADF — Augmented Dickey-Fuller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le test ADF vérifie la présence d'une racine unitaire (non-stationnarité).

- **Hypothèse nulle H₀** : la série a une racine unitaire (non-stationnaire)
- **Hypothèse alternative H₁** : la série est stationnaire

**Résultat :**

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Série originale
     - Après différenciation (d=1)
   * - Statistique > Valeur critique → H₀ non rejetée
     - Statistique < Valeur critique → **H₀ rejetée** ✅
   * - p-value > 0.05 → Non-stationnaire
     - p-value < 0.05 → **Stationnaire** ✅

Test KPSS
^^^^^^^^^^

Le test KPSS vérifie la stationnarité en testant l'hypothèse inverse.

- **Hypothèse nulle H₀** : la série est stationnaire
- **Hypothèse alternative H₁** : la série a une racine unitaire

**Résultat :** H₀ non rejetée (p > 0.05) → ✅ **Stationnaire confirmé** après différenciation

Test Phillips-Perron
^^^^^^^^^^^^^^^^^^^^^

Variante robuste du test ADF, moins sensible aux observations aberrantes.

**Résultat :** Cohérent avec ADF → ✅ **Stationnaire après différenciation**

Conclusion sur la stationnarité
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Conclusion

   La série est **non-stationnaire à l'origine** (présence d'une tendance légère)
   mais devient **stationnaire après une différenciation d'ordre 1 (d=1)**.

   → Paramètre retenu pour SARIMA : **d = 1**

----

Analyse ACF / PACF
-------------------

Les fonctions d'autocorrélation (ACF) et d'autocorrélation partielle (PACF)
permettent d'identifier les ordres p et q du modèle ARIMA.

**Observations :**

- **ACF** : décroissance géométrique — présence d'autocorrélations significatives aux lags 1, 7, 14
- **PACF** : coupure nette après le lag 1–2 → suggère un composante AR d'ordre 1 ou 2
- **Saisonnalité détectée** : pics aux multiples de 7 → **saisonnalité hebdomadaire (S=7)**

Ces observations ont orienté la configuration de SARIMA (p=1, d=1, q=1)(P=1, D=1, Q=1, S=7).

----

Décomposition de la série
--------------------------

La décomposition STL (Seasonal-Trend decomposition using Loess) révèle :

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Composante
     - Observation
   * - **Tendance**
     - Légère hausse progressive du nombre de passages sur 2024–2025
   * - **Saisonnalité**
     - Cycle hebdomadaire prononcé (moins de passages le week-end)
   * - **Résidu**
     - Bruit aléatoire de faible amplitude — série bien structurée

----

Justification du choix des modèles
-------------------------------------

Ces analyses statistiques ont guidé les choix suivants :

1. **Prophet pour le mensuel** : la tendance douce et la saisonnalité annuelle correspondent exactement aux composantes que Prophet est conçu pour modéliser.

2. **MLP avec feature engineering pour le journalier** : la saisonnalité hebdomadaire détectée par ACF/PACF est capturée via les features ``lag_7``, ``lag_14``, ``dow_sin``, ``dow_cos``. Le MLP s'affranchit de la contrainte de stationnarité grâce à la normalisation MinMaxScaler.

3. **SARIMA écarté** : MAE ≈ 100, trop élevée. Le modèle linéaire ne capture pas la non-linéarité des flux journaliers.

4. **LSTM/GRU écartés** : bons résultats théoriques mais nécessitent beaucoup plus de données (>1000 observations) que les 17 mois disponibles.
