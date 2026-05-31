.. _index:

🏥 Prévision des Passages aux Urgences
========================================

.. image:: https://img.shields.io/badge/Python-3.11-blue?logo=python
   :alt: Python 3.11

.. image:: https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit
   :alt: Streamlit

.. image:: https://img.shields.io/badge/Modèle-Prophet%20%7C%20MLP-green
   :alt: Modèles

.. image:: https://img.shields.io/badge/Hôpital-Mohamed%20V%20Meknès-blue
   :alt: Hôpital

|

**Documentation officielle** de l'application de prévision des passages aux urgences de l'Hôpital Mohamed V de Meknès.

.. admonition:: 🎯 À propos de ce projet

   Cette application prédit le **nombre quotidien et mensuel de passages aux urgences**
   grâce à des modèles de séries temporelles avancés (Prophet et MLP), afin d'aider
   les équipes médicales à anticiper les pics d'affluence.

   - 🌐 **Application en ligne :** `prediction-passageauxurgences.streamlit.app <https://prediction-passageauxurgences.streamlit.app>`_
   - 💻 **Code source :** `GitHub <https://github.com/issougmehdi75-alt/Prediction_PassageAuxUrgences>`_
   -👨‍💼 **Auteurs :** Issoug El Mehdi & Ange Bado Yipene Cenacle — Projet Séries Temporelles 2024–2025

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
   :caption: 📊 Analyse & Résultats

   analyse_statistique
   performances

.. toctree::
   :maxdepth: 1
   :caption: 🔧 Maintenance

   faq
   changelog

----

Résumé rapide
-------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Langage**
     - Python 3.11
   * - **Framework**
     - Streamlit >= 1.30
   * - **Modèle mensuel**
     - Prophet (Facebook/Meta) — saisonnalité annuelle
   * - **Modèle journalier**
     - MLP (scikit-learn) — MAE ≈ 7 passages/jour
   * - **Intervalle de confiance**
     - 95%
   * - **Données source**
     - Registres Hôpital Mohamed V, Meknès (2024–2025)
   * - **Déploiement**
     - Streamlit Cloud
