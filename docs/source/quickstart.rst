.. _quickstart:

Démarrage rapide
================

Vous avez déjà installé le projet ? Lancez votre première prévision en moins de 2 minutes.

.. contents::
   :local:
   :depth: 1

----

En 5 étapes
-----------

.. code-block:: bash

   # 1. Activez votre environnement virtuel
   venv\Scripts\activate

   # 2. Lancez l'application
   streamlit run streamlit_app.py

**Dans le navigateur :**

3. Cliquez sur **"🔮 Prédiction"** dans la barre de navigation
4. Choisissez **Prévision MENSUELLE** ou **Prévision JOURNALIÈRE**
5. Chargez votre fichier Excel → choisissez la plage → cliquez **"Générer les prévisions"**

✅ Vos prévisions s'affichent avec intervalles de confiance et courbe interactive.

----

Tester avec les fichiers exemples
-----------------------------------

Si vous n'avez pas encore vos propres données :

1. Sur la page Prédiction, cliquez sur **"⬇️ Télécharger un exemple Excel"**
2. Sauvegardez le fichier téléchargé sur votre bureau
3. Rechargez-le immédiatement dans l'application via **"📤 Déposez votre fichier Excel"**

Cela vous permet de tester toutes les fonctionnalités sans données réelles.

----

Accéder à la version en ligne
------------------------------

L'application est déployée publiquement. Aucune installation requise :

.. code-block:: text

   https://prediction-passageauxurgences.streamlit.app

.. note::

   La version en ligne est identique à la version locale.
   Elle peut être légèrement plus lente lors du premier chargement (réveil du serveur).
