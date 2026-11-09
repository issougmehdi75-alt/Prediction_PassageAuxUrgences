.. _modeles:

Modèles
=======

Protocole d'évaluation
----------------------

Toutes les erreurs sont mesurées par **backtest à origine glissante** :

.. code-block:: text

   pli 1 : [====== entraînement ======][test 14 j]
   pli 2 : [======== entraînement ========][test 14 j]
   ...
   pli 8 : [============== entraînement ==============][test 14 j]

Pour chaque pli, le modèle est réentraîné sur tout le passé puis prévoit la fenêtre suivante
**sans jamais voir ses valeurs**. Les modèles ML sont évalués en mode **récursif** (leurs propres
prévisions alimentent les lags), exactement comme en production.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Mode
     - Script d'évaluation (``evaluer_modeles.py``)
     - Application (« erreur attendue »)
   * - Journalier
     - 8 plis × 14 jours (112 derniers jours)
     - 8 plis × 14 jours (112 derniers jours), si l'historique le permet
   * - Mensuel
     - 6 prévisions à 1 mois
     - 6 prévisions à 1 mois

Modèles de référence (baselines)
--------------------------------

- **Naïf** : dernière valeur répétée.
- **Naïf saisonnier (J-7)** : valeur du même jour la semaine précédente.
- **Moyenne mobile** : moyenne des 7 derniers jours / 3 derniers mois.

Un modèle n'est utile que s'il bat ces références.

MLP — modèle journalier
-----------------------

.. code-block:: python

   TransformedTargetRegressor(            # cible standardisée
       make_pipeline(StandardScaler(),
                     MLPRegressor(hidden_layer_sizes=(64, 32), activation="relu",
                                  alpha=1e-2, learning_rate_init=1e-3,
                                  early_stopping=True, validation_fraction=0.15,
                                  n_iter_no_change=30, random_state=42)),
       transformer=StandardScaler())

**Features** (toutes calculées à partir des valeurs strictement antérieures) :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Description
   * - ``lag_1, lag_2, lag_3``
     - passages des 3 jours précédents
   * - ``lag_7, lag_14``
     - même jour 1 et 2 semaines avant
   * - ``roll_7, roll_14``
     - moyenne des 7 / 14 jours précédents
   * - ``dow_sin, dow_cos``
     - encodage cyclique du jour de la semaine
   * - ``month_sin, month_cos``
     - encodage cyclique du mois
   * - ``weekend``
     - 1 le samedi et le dimanche

Les 14 premiers jours (lags incomplets) sont exclus de l'entraînement. En v1 ils étaient complétés par
``bfill()``, ce qui injectait des valeurs futures dans les features.

L'architecture a été réduite de (128, 64, 32) à (64, 32) avec une régularisation L2 : avec ~500
observations, le réseau plus grand sur-apprenait sans gain mesurable.

Prophet — modèle mensuel
------------------------

.. code-block:: python

   Prophet(yearly_seasonality=len(hist) >= 24,   # désactivée avec moins de 2 ans
           weekly_seasonality=False, daily_seasonality=False,
           changepoint_prior_scale=0.05, interval_width=0.95)

Avec 17 mois, la saisonnalité annuelle (série de Fourier d'ordre 10) ne peut pas être estimée :
elle modéliserait le bruit. Elle s'active automatiquement dès 24 mois d'historique.
``changepoint_prior_scale`` passe de 0,3 à 0,05 (valeur par défaut) pour éviter une tendance trop flexible.

Autres modèles comparés
-----------------------

- **SARIMA(1,1,1)(1,0,1)₇** (statsmodels) : d = 1 d'après les tests de stationnarité, saison de 7 jours.
- **Prophet journalier** : saisonnalité hebdomadaire.
- **Ridge** : régression linéaire régularisée sur les mêmes features que le MLP.
- **Gradient Boosting** (``HistGradientBoostingRegressor``) : mêmes features.

Résultats : voir :ref:`performances`.
