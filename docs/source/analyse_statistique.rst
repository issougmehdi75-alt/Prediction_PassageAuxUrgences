.. _analyse_statistique:

Analyse statistique
===================

Valeurs calculées par ``scripts/evaluer_modeles.py`` (statsmodels).

Tests de stationnarité
----------------------

- **ADF** (Dickey-Fuller augmenté) : H₀ = racine unitaire. p < 0,05 → stationnaire.
- **KPSS** : H₀ = stationnaire. p > 0,05 → stationnaire.

Les deux tests sont complémentaires ; une série est jugée stationnaire si les deux concluent dans
ce sens. Les p-values KPSS sont tabulées et bornées à [0,01 ; 0,10].

.. list-table::
   :header-rows: 1
   :widths: 22 22 8 12 10 12 10

   * - Série
     - Transformation
     - n
     - ADF stat
     - ADF p
     - KPSS stat
     - KPSS p
   * - mensuelle
     - niveau
     - 17
     - −4,468
     - 0,0002
     - 0,291
     - ≥ 0,10
   * - mensuelle
     - différence ordre 1
     - 16
     - −4,745
     - 0,0001
     - 0,259
     - ≥ 0,10
   * - journalière (simulée)
     - niveau
     - 517
     - −3,768
     - 0,0033
     - 0,848
     - ≤ 0,01
   * - journalière (simulée)
     - différence ordre 1
     - 516
     - −7,595
     - < 0,0001
     - 0,020
     - ≥ 0,10

Conclusions
-----------

- **Série mensuelle** : stationnaire en niveau d'après les deux tests. Avec 17 points, la puissance
  des tests est faible : ce résultat est à confirmer sur un historique plus long.
- **Série journalière** : ADF rejette la racine unitaire mais KPSS rejette la stationnarité en
  niveau — situation typique d'une série dont le niveau varie (ici, il suit les totaux mensuels).
  Après une différenciation d'ordre 1, les deux tests concluent à la stationnarité → **d = 1**
  dans SARIMA.

Autocorrélation (série journalière)
-----------------------------------

.. list-table::
   :header-rows: 1

   * - Lag
     - 1
     - 7
     - 14
   * - ACF
     - 0,19
     - 0,41
     - 0,31

L'autocorrélation au lag 7 est plus forte qu'au lag 1 : effet « jour de la semaine ».
**Attention :** cet effet est introduit par le profil hebdomadaire de la simulation
(voir :ref:`simulation`) ; ce n'est pas une observation sur données réelles.

.. note::

   La v1 présentait des cartes « Stat < Valeur critique » identiques pour ADF, KPSS et Phillips-Perron,
   sans valeurs. Elles sont remplacées par les statistiques réellement calculées. Phillips-Perron a été
   retiré (redondant avec ADF, et non disponible dans statsmodels).
