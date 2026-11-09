.. _installation:

Installation
============

Prérequis
---------

- Python **3.10 ou plus** (testé avec 3.13)
- ``pip`` et ``git``

Étapes
------

.. code-block:: bash

   git clone https://github.com/issougmehdi75-alt/Prediction_PassageAuxUrgences.git
   cd Prediction_PassageAuxUrgences
   python -m venv .venv
   source .venv/bin/activate          # Windows : .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run streamlit_app.py

L'application s'ouvre sur ``http://localhost:8501``.

Dépendances
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Paquet
     - Rôle
   * - ``streamlit`` ≥ 1.46
     - interface (``st.navigation``, ``st.segmented_control``, thème de la barre latérale)
   * - ``pandas``, ``numpy``
     - manipulation des séries
   * - ``plotly``
     - graphiques interactifs
   * - ``prophet``
     - modèle mensuel (installe CmdStan automatiquement)
   * - ``scikit-learn``
     - MLP, Ridge, Gradient Boosting
   * - ``statsmodels``
     - SARIMA, tests ADF / KPSS
   * - ``openpyxl``
     - lecture / écriture Excel

Outils de développement
-----------------------

.. code-block:: bash

   pip install -r requirements-dev.txt
   python -m pytest -q                      # tests
   python scripts/simuler_journalier.py     # régénérer la série journalière
   python scripts/evaluer_modeles.py        # recalculer results/metriques.json

Déploiement sur Streamlit Community Cloud
-----------------------------------------

1. Pousser le dépôt sur GitHub.
2. Sur `share.streamlit.io <https://share.streamlit.io>`_ : *New app* → choisir le dépôt, la branche
   ``main`` et le fichier ``streamlit_app.py``.
3. Le thème est lu automatiquement dans ``.streamlit/config.toml``.

Problèmes fréquents
-------------------

**Prophet ne s'installe pas (Windows)** — utiliser Python 3.11+ et une version récente de ``pip`` ;
``prophet`` ≥ 1.1 fournit des roues précompilées.

**Port 8501 occupé** — ``streamlit run streamlit_app.py --server.port 8502``.
