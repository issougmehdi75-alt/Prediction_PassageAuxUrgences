.. _quickstart:

Démarrage rapide
================

En 1 minute, sans fichier
-------------------------

1. Lancer ``streamlit run streamlit_app.py``.
2. Ouvrir la page **Prédiction**.
3. Laisser **Mensuelle** et **Données du projet** sélectionnés.
4. Cliquer sur **Générer les prévisions**.

Vous obtenez 6 mois de prévisions avec leur intervalle à 95 %, l'erreur attendue et un export Excel.

Avec vos données
----------------

1. Choisir **Mon fichier Excel**, télécharger l'exemple pour voir le format.
2. Préparer un fichier à deux colonnes : date | nombre de passages.
3. Déposer le fichier, choisir l'horizon, générer.

.. code-block:: text

   Mois           Passages
   Janvier 2024   7340
   Février 2024   6850
   ...

Voir :ref:`guide_donnees` pour les formats acceptés.
