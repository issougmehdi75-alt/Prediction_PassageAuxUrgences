.. _guide_predictions:

Lire les prévisions
===================

Indicateurs affichés
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Indicateur
     - Signification
   * - Total / moyenne prévus
     - somme et moyenne des prévisions sur l'horizon choisi
   * - Pic prévu
     - période où la prévision est la plus élevée
   * - Erreur attendue (MAE)
     - erreur absolue moyenne **hors-échantillon** : le modèle est réentraîné sur le passé et
       évalué sur des périodes qu'il n'a pas vues (voir :ref:`modeles`)
   * - MAPE
     - même erreur exprimée en % des valeurs réelles
   * - vs modèle naïf
     - variation d'erreur par rapport à la référence (*naïf saisonnier J-7* en journalier,
       *moyenne mobile 3 mois* en mensuel). Négatif = le modèle fait mieux.

.. note::

   La v1 affichait une « fiabilité » calculée comme ``100 − MAE / prévision × 100``. Ce n'était
   pas une probabilité et la MAE de Prophet était mesurée sur les données d'entraînement : cet
   indicateur a été remplacé par la MAE et la MAPE hors-échantillon.

Intervalle à 95 %
-----------------

- **Mensuel** : intervalle fourni par Prophet (incertitude de tendance et bruit d'observation).
- **Journalier** : :math:`\hat y_h \pm 1{,}96\,\sigma(h)` avec :math:`\sigma(h) = \min(c\sqrt{h},\ \sigma_y)`.
  :math:`c` est estimé sur les erreurs du backtest, :math:`\sigma_y` est l'écart-type de la série.
  L'intervalle s'élargit donc avec l'horizon : une prévision à 30 jours est plus incertaine qu'à 1 jour.

Bonnes pratiques
----------------

- Privilégier les horizons courts : l'erreur augmente avec l'horizon (prévision récursive).
- Raisonner sur l'intervalle, pas seulement sur la valeur centrale, pour dimensionner les équipes.
- Les prévisions sont indicatives et ne remplacent pas le jugement des équipes.

Export Excel
------------

Le fichier exporté contient trois feuilles : **Prévisions** (date, prévision, bornes 95 %),
**Historique** (données utilisées) et **Évaluation** (modèle, protocole, MAE / RMSE / MAPE du modèle
et de la référence).
