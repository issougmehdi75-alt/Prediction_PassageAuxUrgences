.. _guide_interface:

Interface utilisateur
=====================

L'application est composée de **2 pages** accessibles via la barre de navigation en haut.

.. contents::
   :local:
   :depth: 2

----

Navigation
----------

Deux boutons permettent de basculer entre les pages :

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Bouton
     - Description
   * - ``📖 Introduction``
     - Présentation complète du projet, des modèles et des performances
   * - ``🔮 Prédiction``
     - Interface interactive pour générer des prévisions

----

Page Introduction
-----------------

Cette page présente le contexte académique et technique du projet.

Objectif & Données
^^^^^^^^^^^^^^^^^^

Deux cartes résument :

- **L'objectif** : prédire les passages pour optimiser les ressources humaines et matérielles
- **Les données** : registres de l'Hôpital Mohamed V, période 2024–2025

Pipeline du projet
^^^^^^^^^^^^^^^^^^

5 blocs décrivent les étapes du travail de recherche :

1. **Chargement & Prétraitement** — nettoyage, gestion des valeurs manquantes, désagrégation mensuelle → journalière
2. **Analyse statistique** — tests ADF, KPSS, Phillips-Perron, ACF/PACF
3. **Modèles statistiques** — Prophet, SARIMA+GARCH
4. **Machine Learning** — XGBoost, LightGBM, MLP avec feature engineering
5. **Deep Learning** — RNN, LSTM, GRU avec optimisation Optuna

Tableau comparatif des modèles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Comparaison des 6 modèles testés sur la MAE (Mean Absolute Error) journalière.

Graphique des performances
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Diagramme en barres interactif (Plotly) montrant la MAE de chaque modèle.
**Plus la barre est basse, meilleur est le modèle.**

Tests statistiques
^^^^^^^^^^^^^^^^^^

Résumé des 3 tests de stationnarité avec leurs conclusions.

----

Page Prédiction
---------------

C'est la page principale pour l'utilisation quotidienne.

Cartes d'information
^^^^^^^^^^^^^^^^^^^^^

4 cartes rappellent en permanence :

- Le modèle mensuel utilisé (Prophet)
- Le modèle journalier utilisé (MLP — MAE ≈ 7)
- Le niveau de confiance (95%)
- L'outil de visualisation (Plotly)

Sélecteur de mode
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   📅 Prévision MENSUELLE    ←→    📆 Prévision JOURNALIÈRE

Ce choix détermine :

- Le **modèle** utilisé (Prophet vs MLP)
- Le **format Excel** attendu (dates mensuelles vs journalières)
- L'**unité du slider** (mois vs jours)

Barre latérale (Sidebar)
^^^^^^^^^^^^^^^^^^^^^^^^^

La sidebar bleue affiche en permanence :

- L'identité du projet (Hôpital Mohamed V, Meknès)
- L'objectif
- Les modèles utilisés
- Le format attendu du fichier Excel
- Le classement des performances des modèles
- Le nom de l'auteur
