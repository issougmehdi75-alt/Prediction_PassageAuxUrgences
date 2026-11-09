.. _guide_donnees:

Guide des données
=================

Données du projet
-----------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 25 25

   * - Fichier
     - Statut
     - Période
     - Taille
   * - ``data/passages_mensuels.xlsx``
     - réel
     - janv. 2024 → mai 2025
     - 17 mois, moyenne 7 409 / mois
   * - ``data/passages_journaliers_simules.xlsx``
     - **simulé**
     - 01/01/2024 → 31/05/2025
     - 517 jours, moyenne 244 / jour

.. _simulation:

Simulation de la série journalière
----------------------------------

L'hôpital n'a fourni que des totaux mensuels. Pour construire et tester le mode journalier,
chaque total mensuel :math:`T_m` est réparti sur les jours du mois par un **tirage multinomial** :

.. math::

   (y_1, \dots, y_{J}) \sim \mathcal{M}\left(T_m;\ p_1, \dots, p_J\right),
   \qquad p_j = \frac{w_{\text{jour}(j)}}{\sum_k w_{\text{jour}(k)}}

- :math:`\sum_j y_j = T_m` : les **totaux mensuels réels sont conservés exactement** ;
- la variabilité jour à jour est de type Poisson (:math:`\approx \pm\sqrt{244} \approx 15`) ;
- :math:`w` est un **profil hebdomadaire supposé** (lundi 1,08 · mardi 1,03 · mer. 1,00 · jeu. 0,99 ·
  ven. 1,00 · sam. 0,94 · dim. 0,96).

.. warning::

   Le profil hebdomadaire est une **hypothèse de simulation**, pas une observation. Si un modèle
   « découvre » une saisonnalité de 7 jours, il retrouve cette hypothèse. Pour une répartition
   uniforme : ``python scripts/simuler_journalier.py --sans-profil``.

La simulation est reproductible (graine 42) ; le script vérifie que la somme par mois redonne
les totaux réels.

Format des fichiers importés
----------------------------

- **Colonne A** : date ; **colonne B** : nombre de passages.
- Dates acceptées : cellule date Excel, ``2024-01-01``, ``01/01/2024``, ``01-01-2024``,
  ``2024/01/01``, ``Janvier 2024``, ``janv. 2024``, ``Jan 2024`` (mois en français ou en anglais,
  avec ou sans accents).
- Nombres : ``245``, ``245,0``, ``7 340``.

Contrôles automatiques
----------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Situation
     - Comportement
   * - Ligne d'en-tête, ligne non numérique
     - ignorée (signalée si plus d'une)
   * - Plus de 2 colonnes
     - seules les 2 premières sont utilisées (avertissement)
   * - Date en double
     - valeurs additionnées (avertissement)
   * - Jour / mois manquant
     - complété par interpolation linéaire (avertissement)
   * - Moins de 8 mois / 60 jours
     - erreur : historique insuffisant
   * - Valeurs incohérentes avec le mode
     - avertissement (ex. totaux mensuels chargés en mode journalier)
