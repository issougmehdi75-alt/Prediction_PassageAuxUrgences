.. _guide_interface:

Guide de l'interface
====================

La navigation se fait par les onglets en haut de page : **Introduction** et **Prédiction**.
La barre latérale rappelle l'objectif, les modèles et le format de fichier attendu.

Page Introduction
-----------------

1. **Objectif et données** — avec le statut de chaque série (*réel* / *simulé*).
2. **Indicateurs clés** — taille des historiques, erreur du MLP, gain par rapport au modèle naïf.
3. **Série mensuelle observée**.
4. **Démarche** — données, analyse statistique, modélisation, évaluation.
5. **Comparaison des modèles** — journalier (graphique + tableau, avec plancher théorique) et mensuel.
6. **Tests de stationnarité** — statistiques et p-values ADF / KPSS calculées.
7. **Limites et perspectives**.

Toutes les valeurs proviennent de ``results/metriques.json`` (voir :ref:`performances`).

Page Prédiction
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Rôle
   * - Type de prévision
     - *Mensuelle* (Prophet) ou *Journalière* (MLP)
   * - Source des données
     - *Données du projet* ou *Mon fichier Excel* (exemple téléchargeable)
   * - 1 · Données
     - période, moyenne, min/max, graphique ; avertissements éventuels (trous, doublons…)
   * - 2 · Horizon
     - 1–12 mois ou 1–60 jours
   * - 3 · Résultats
     - total et pic prévus, erreur attendue (MAE / MAPE hors-échantillon), gain vs modèle naïf,
       graphique, tableau, export Excel

Lecture du graphique de prévision
---------------------------------

- **bleu** : valeurs observées ;
- **orange** : prévision ;
- **zone orange claire** : intervalle de prévision à 95 % ;
- **ligne pointillée grise** : dernière observation.

Les résultats restent affichés après le téléchargement du fichier Excel. Ils sont recalculés si
l'on change de mode, de fichier ou d'horizon.
