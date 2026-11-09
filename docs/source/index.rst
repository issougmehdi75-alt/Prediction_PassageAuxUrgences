.. _index:

🏥 Prévision des passages aux urgences
=======================================

.. image:: https://img.shields.io/badge/Python-3.10%2B-blue?logo=python
   :alt: Python 3.10+

.. image:: https://img.shields.io/badge/Streamlit-1.46%2B-red?logo=streamlit
   :alt: Streamlit

.. image:: https://img.shields.io/badge/Modèles-Prophet%20%7C%20MLP-2a78d6
   :alt: Modèles

|

Documentation de l'application de prévision des passages aux urgences de l'Hôpital Mohamed V de Meknès.

.. admonition:: 🎯 À propos

   L'application prévoit le nombre de passages aux urgences **par mois** (Prophet) et **par jour** (MLP),
   avec un intervalle d'incertitude à 95 % et une **erreur attendue mesurée hors-échantillon**.

   - 🌐 **Application :** `prediction-passageauxurgences.streamlit.app <https://prediction-passageauxurgences.streamlit.app>`_
   - 💻 **Code source :** `GitHub <https://github.com/issougmehdi75-alt/Prediction_PassageAuxUrgences>`_
   - 👨‍💼 **Auteurs :** Issoug El Mehdi & Bado Ange Yipene Cenacle — Projet Séries Temporelles 2024–2025

.. warning::

   Les données **mensuelles** sont réelles ; les données **journalières** sont **simulées** à partir
   des totaux mensuels (voir :ref:`guide_donnees`). Les performances journalières doivent être lues
   dans ce cadre.

----

.. toctree::
   :maxdepth: 2
   :caption: 🚀 Démarrage rapide
   :numbered:

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: 📖 Guide utilisateur

   guide_interface
   guide_donnees
   guide_predictions

.. toctree::
   :maxdepth: 2
   :caption: 🤖 Documentation technique

   modeles
   architecture
   api_reference

.. toctree::
   :maxdepth: 2
   :caption: 📊 Analyse & résultats

   analyse_statistique
   performances

.. toctree::
   :maxdepth: 1
   :caption: 🔧 Maintenance

   faq
   changelog

----

Résumé
------

.. list-table::
   :widths: 30 70

   * - **Modèle mensuel**
     - Prophet — erreur à 1 mois : MAPE 2,8 % (6 prévisions)
   * - **Modèle journalier**
     - MLP (scikit-learn) — MAE 14,2 passages/jour, MAPE 5,8 % (backtest 112 jours, données simulées)
   * - **Gain vs modèle naïf**
     - −25 % d'erreur (journalier, vs « même jour J-7 »)
   * - **Intervalle**
     - 95 %, s'élargissant avec l'horizon
   * - **Déploiement**
     - Streamlit Community Cloud
