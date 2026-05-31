.. _guide_predictions:

Générer des prévisions
======================

Guide étape par étape pour obtenir vos prévisions depuis la page **Prédiction**.

.. contents::
   :local:
   :depth: 2

----

Étape 1 — Choisir le type de prévision
----------------------------------------

Au sommet de la page, sélectionnez :

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Utilisation
   * - ``📅 Prévision MENSUELLE``
     - Prévisions mois par mois — utilise le modèle **Prophet**. Idéal pour la planification budgétaire et RH à moyen terme.
   * - ``📆 Prévision JOURNALIÈRE``
     - Prévisions jour par jour — utilise le modèle **MLP**. Idéal pour la gestion opérationnelle quotidienne.

----

Étape 2 — Charger votre fichier Excel
---------------------------------------

1. Cliquez sur **"📤 Déposez votre fichier Excel"** ou glissez-déposez le fichier
2. Le système valide automatiquement le fichier et affiche :

   - ✅ Un message de succès avec le nombre de lignes lues et la plage de dates
   - ❌ Un message d'erreur détaillé si le format est incorrect

3. Un **aperçu des données** et un **graphique de l'historique** s'affichent pour confirmer la lecture.

.. warning::

   Si vous obtenez une erreur de format, consultez la section :ref:`guide_donnees`
   pour connaître le format exact attendu.

----

Étape 3 — Choisir la plage de prévision
-----------------------------------------

Un **slider interactif** vous permet de sélectionner :

- **Mode mensuel** : de 1 à 24 mois à prédire
- **Mode journalier** : de 1 à 90 jours à prédire

La plage de dates prévues s'affiche en temps réel sous le slider :

.. code-block:: text

   📅 Les prévisions iront du 01/03/2024 au 14/03/2024 (14 jours)

.. important::

   L'application prédit **uniquement le futur** : les dates proposées commencent
   toujours **après la dernière date de votre fichier historique**.

----

Étape 4 — Générer les prévisions
----------------------------------

Cliquez sur le bouton **"🔮 Générer les prévisions"**.

Un message de chargement s'affiche pendant l'entraînement du modèle
(quelques secondes pour MLP, 5 à 15 secondes pour Prophet).

----

Comprendre les résultats
--------------------------

Cartes de résultats
^^^^^^^^^^^^^^^^^^^

Les 4 premières périodes prévues s'affichent sous forme de cartes :

.. code-block:: text

   📅 Mar 2024
   ──────────
   7 245
   [6 890 – 7 600]
   Fiabilité : 94%

- **Nombre central** : prévision principale du modèle
- **[Borne basse – Borne haute]** : intervalle de confiance à 95%
- **Fiabilité** : estimation de la précision basée sur la MAE

Courbe interactive
^^^^^^^^^^^^^^^^^^

Le graphique Plotly affiche :

- 🔵 **Historique** : ligne bleue foncée, les données réelles de votre fichier
- 🔮 **Prévisions** : ligne rouge pointillée avec marqueurs diamant
- 🔵 **Zone IC 95%** : bande bleue translucide autour des prévisions
- ⬆️ **Borne haute** : ligne verte en tirets
- ⬇️ **Borne basse** : ligne orange en tirets
- ❙ **Ligne grise** : séparation entre historique et futur

**Interactions disponibles :**

- Zoom : molette de la souris ou sélection d'une zone
- Déplacement : clic + glisser
- Info-bulle : survolez un point pour voir la valeur exacte
- Masquer une série : cliquez sur son nom dans la légende

Tableau des prévisions
^^^^^^^^^^^^^^^^^^^^^^^

Tableau récapitulatif complet avec toutes les périodes prévues, les bornes et la fiabilité.

----

Exporter les résultats
------------------------

Cliquez sur **"📥 Télécharger les prévisions (Excel)"** pour obtenir un fichier avec :

- **Feuille "Prévisions"** : tableau complet des prédictions (Date, Prévision, Borne basse, Borne haute, Fiabilité)
- **Feuille "Historique"** : vos données d'entrée originales

Ce fichier peut être partagé avec les équipes médicales ou intégré dans des rapports.
