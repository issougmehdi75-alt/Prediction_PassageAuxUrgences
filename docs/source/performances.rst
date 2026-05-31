.. _performances:

Performances des modèles
=========================

Comparaison détaillée des 6 modèles testés sur les données de l'Hôpital Mohamed V.

.. contents::
   :local:
   :depth: 2

----

Métriques d'évaluation
-----------------------

MAE — Mean Absolute Error
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|

La MAE représente l'erreur absolue moyenne en **nombre de passages**.
Une MAE de 7 signifie que le modèle se trompe en moyenne de **7 patients par jour**.

MASE — Mean Absolute Scaled Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   MASE = \frac{MAE}{\frac{1}{n-1} \sum_{i=2}^{n} |y_i - y_{i-1}|}

Erreur normalisée par rapport à une prévision naïve (répéter la dernière valeur).
Un MASE < 1 signifie que le modèle est meilleur que la prévision naïve.

Intervalle de confiance à 95%
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La plage dans laquelle la valeur réelle a 95% de chances de tomber.

----

Tableau récapitulatif
----------------------

.. list-table::
   :widths: 5 20 20 15 15 25
   :header-rows: 1

   * - Rang
     - Modèle
     - Type
     - MAE journalier
     - MASE
     - Remarque
   * - 🥇 1
     - **MLP**
     - Réseau de neurones
     - **≈ 7**
     - **< 1**
     - ⭐ Retenu pour le journalier
   * - 🥈 2
     - **Prophet**
     - Statistique bayésien
     - Excellent (mensuel)
     - Très bon
     - ⭐ Retenu pour le mensuel
   * - 🥉 3
     - **XGBoost**
     - Gradient Boosting
     - ≈ 22
     - Bon
     - Bon mais dépassé par MLP
   * - 4
     - **LightGBM**
     - Gradient Boosting
     - ≈ 47
     - Moyen
     - Rapide mais moins précis
   * - 5
     - **LSTM**
     - Deep Learning
     - ≈ 55
     - Moyen
     - Manque de données
   * - 5
     - **GRU**
     - Deep Learning
     - ≈ 58
     - Moyen
     - Manque de données
   * - 6
     - **SARIMA+GARCH**
     - Statistique classique
     - ≈ 100
     - > 1
     - Modèle linéaire insuffisant

----

Analyse par modèle
-------------------

MLP — Meilleur modèle (MAE ≈ 7)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le MLP surpasse tous les autres modèles grâce à :

1. **Feature engineering riche** : 17 features capturant la saisonnalité hebdomadaire et mensuelle
2. **Normalisation MinMaxScaler** : s'affranchit de la non-stationnarité
3. **Architecture optimale** : 3 couches cachées (128-64-32) avec early stopping

.. admonition:: Résultat clé

   MAE ≈ 7 passages/jour signifie que sur une journée avec 245 passages réels,
   le modèle prédit entre 238 et 252. **Erreur < 3%.**

Prophet — Meilleur modèle mensuel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prophet excelle sur les données mensuelles car :

- La saisonnalité annuelle est bien détectée avec 17 mois de données
- La tendance haussière est correctement modélisée
- Les intervalles de confiance sont natifs et bien calibrés

XGBoost — 3e place (MAE ≈ 22)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bon modèle de référence avec les mêmes features que MLP.
La différence avec MLP s'explique par la capacité du réseau de neurones à
capturer des interactions non-linéaires plus complexes.

LSTM / GRU — 5e place (MAE ≈ 55–58)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ces modèles séquentiels ont théoriquement un avantage sur les données temporelles,
mais ils nécessitent de **grandes quantités de données** (> 1000 observations).
Avec seulement ~520 jours, ils surapprentissent.

SARIMA+GARCH — Dernier (MAE ≈ 100)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le modèle statistique classique échoue ici car :

- Les relations entre variables sont **non-linéaires**
- La stationnarisation par différenciation perd de l'information
- GARCH (modélisation de la volatilité) n'apporte pas de valeur sur ce type de données

----

Courbe des performances
------------------------

Visualisation disponible sur la **page Introduction** de l'application :

.. code-block:: text

   MAE
   100 |  ████  SARIMA
    58 |  ██    GRU
    55 |  ██    LSTM
    47 |  █     LightGBM
    22 |  █     XGBoost
     7 |  ▌     MLP  ← 🏆 Meilleur
       └──────────────────────────

----

Limites et perspectives
------------------------

**Limites actuelles :**

- Seulement 17 mois de données mensuelles → Prophet manque d'historique pour les mois éloignés
- Accumulation d'erreur du MLP sur les prévisions > 30 jours
- Pas de prise en compte des événements exceptionnels (épidémies, jours fériés marocains)

**Améliorations possibles :**

- Enrichir l'historique avec les données des années précédentes
- Ajouter les jours fériés marocains dans Prophet
- Tester XGBoost avec les mêmes features que MLP (différence attendue faible)
- Entraîner LSTM/GRU avec 3+ années de données journalières
