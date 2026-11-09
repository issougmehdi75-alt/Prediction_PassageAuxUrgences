.. _performances:

Performances
============

Toutes les valeurs sont produites par ``python scripts/evaluer_modeles.py`` et stockées dans
``results/metriques.json``.

Métriques
---------

.. math::

   \text{MAE} = \frac1n\sum|y_i-\hat y_i| \qquad
   \text{RMSE} = \sqrt{\frac1n\sum(y_i-\hat y_i)^2} \qquad
   \text{MAPE} = \frac{100}{n}\sum\frac{|y_i-\hat y_i|}{y_i}

Prévision journalière
---------------------

Backtest sur les 112 derniers jours (8 fenêtres de 14 jours, prévision récursive à 1–14 jours).
**Données simulées** (voir :ref:`simulation`).

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 15 15

   * - Modèle
     - MAE
     - RMSE
     - MAPE
     - Type
   * - Ridge (features)
     - 14,1
     - 17,3
     - 5,6 %
     - modèle
   * - **MLP** (retenu)
     - **14,2**
     - **17,7**
     - **5,8 %**
     - modèle
   * - SARIMA(1,1,1)(1,0,1)₇
     - 14,4
     - 17,6
     - 5,8 %
     - modèle
   * - Moyenne mobile 7 j
     - 15,0
     - 20,0
     - 6,0 %
     - référence
   * - Prophet
     - 15,2
     - 18,6
     - 6,0 %
     - modèle
   * - Gradient Boosting
     - 15,6
     - 19,3
     - 6,2 %
     - modèle
   * - Naïf saisonnier (J-7)
     - 18,9
     - 23,8
     - 7,6 %
     - référence
   * - Naïf (veille)
     - 19,1
     - 25,3
     - 7,4 %
     - référence
   * - *Plancher théorique (oracle)*
     - *12,2*
     -
     -
     -

**Plancher théorique.** Comme la série est simulée, on connaît la valeur attendue de chaque jour
(total mensuel × poids du jour). L'erreur de cette prévision « oracle » (12,2) est la meilleure
erreur atteignable : le reste est du bruit aléatoire. Les meilleurs modèles (≈ 14,2) en sont proches ;
une erreur inférieure au plancher signalerait une fuite de données.

Interprétation
~~~~~~~~~~~~~~

- Le MLP réduit l'erreur de **25 %** par rapport au naïf saisonnier.
- MLP, Ridge et SARIMA sont **statistiquement équivalents** : moins de 2 % d'écart, sur 112 jours.
  Le MLP est conservé pour l'application ; Ridge serait un choix tout aussi valable et plus simple.
- Le Gradient Boosting est légèrement moins bon : avec ~500 observations et un signal surtout
  linéaire (niveau + effet jour de semaine), il a peu d'avantage.

.. note::

   La v1 annonçait un MAE ≈ 7 pour le MLP. Cette valeur est inférieure au plancher théorique
   des données actuelles et ne peut pas être reproduite ; elle provenait probablement d'une
   évaluation non hors-échantillon ou d'une autre simulation. Elle a été retirée.

Prévision mensuelle
-------------------

Prévision à 1 mois répétée sur les 6 derniers mois.

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Modèle
     - MAE
     - MAPE
     - Type
   * - Moyenne mobile 3 mois
     - 197
     - 2,6 %
     - référence
   * - **Prophet** (retenu)
     - 210
     - 2,8 %
     - modèle
   * - Naïf (mois précédent)
     - 392
     - 5,2 %
     - référence

Avec 6 points de test, la différence entre Prophet et la moyenne mobile n'est pas significative.
Prophet est conservé pour ses intervalles d'incertitude et parce qu'il exploitera la saisonnalité
annuelle avec un historique plus long.

Reproduire
----------

.. code-block:: bash

   python scripts/evaluer_modeles.py   # ~10 secondes
