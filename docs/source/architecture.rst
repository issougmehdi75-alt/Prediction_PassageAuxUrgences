.. _architecture:

Architecture du code
====================

Organisation et structure du code source de l'application.

.. contents::
   :local:
   :depth: 2

----

Structure des fichiers
-----------------------

.. code-block:: text

   Prediction_PassageAuxUrgences/
   │
   ├── streamlit_app.py              # Application principale (784 lignes)
   ├── requirements.txt              # Dépendances Python
   ├── README.md                     # Documentation rapide
   ├── .readthedocs.yaml             # Configuration Read the Docs
   │
   ├── data/
   │   ├── exemple_journalier.xlsx   # Données exemple (60 jours)
   │   └── exemple_mensuel.xlsx      # Données exemple (17 mois)
   │
   └── docs/                         # Documentation Sphinx
       ├── requirements_docs.txt
       └── source/
           ├── conf.py
           ├── index.rst
           └── *.rst

----

Organisation de ``streamlit_app.py``
--------------------------------------

Le fichier est organisé en sections clairement délimitées :

.. code-block:: text

   streamlit_app.py
   │
   ├── [1] Configuration page (set_page_config)
   ├── [2] CSS personnalisé (markdown HTML)
   ├── [3] Sidebar (barre latérale bleue)
   ├── [4] Navigation (2 boutons : Introduction / Prédiction)
   │
   ├── [5] PAGE INTRODUCTION
   │   ├── Cartes Objectif & Données
   │   ├── Pipeline (5 étapes)
   │   ├── Tableau comparatif des modèles
   │   ├── Graphique Plotly performances
   │   └── Tests statistiques
   │
   └── [6] PAGE PRÉDICTION
       ├── Fonctions utilitaires
       │   ├── lire_excel()          ← Lecture & validation du fichier
       │   ├── generer_exemple_excel() ← Génère les fichiers exemples
       │   ├── predict_monthly()     ← Modèle Prophet
       │   ├── predict_daily_mlp()   ← Modèle MLP
       │   └── plot_forecast()       ← Graphique Plotly
       │
       ├── Étape 1 : Upload Excel
       ├── Étape 2 : Slider plage
       └── Étape 3 : Résultats + Export

----

Fonctions principales
----------------------

``lire_excel(uploaded_file, granularity)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lit et valide un fichier Excel uploadé.

**Paramètres :**

- ``uploaded_file`` : objet fichier Streamlit (BytesIO)
- ``granularity`` : ``"monthly"`` ou ``"daily"``

**Retourne :** ``(DataFrame, None)`` si succès, ``(None, str_erreur)`` si échec

**Pipeline interne :**

1. Lecture avec ``pd.read_excel(header=None)``
2. Suppression des lignes/colonnes vides
3. Filtrage des lignes non-numériques (en-têtes)
4. Tentative de parsing de date sur 7 formats différents
5. Conversion numérique de la colonne passages
6. Tri chronologique et reset d'index

``predict_monthly(df, n_months)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Entraîne Prophet et génère ``n_months`` prévisions mensuelles.

**Paramètres :**

- ``df`` : DataFrame avec colonnes ``ds`` (datetime) et ``y`` (int)
- ``n_months`` : nombre de mois à prédire (1–24)

**Retourne :** ``(DataFrame forecast, float mae)``

``predict_daily_mlp(df, n_days)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Entraîne le MLP et génère ``n_days`` prévisions journalières par itération.

**Paramètres :**

- ``df`` : DataFrame avec colonnes ``ds`` (datetime) et ``y`` (int)
- ``n_days`` : nombre de jours à prédire (1–90)

**Retourne :** ``(DataFrame forecast, float mae)``

``plot_forecast(df_hist, df_fc, is_monthly, mae)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Génère la figure Plotly avec historique + prévisions + intervalles.

**Note technique :**

.. code-block:: python

   # ✅ FIX pandas >= 2.0 : add_vline() est incompatible avec pd.Timestamp
   # Solution : add_shape() + add_annotation() avec str(date)
   last_x = str(df_hist["ds"].max().date())
   fig.add_shape(type="line", x0=last_x, x1=last_x, ...)
   fig.add_annotation(x=last_x, ...)

----

Gestion des dépendances
------------------------

Les imports lourds (Prophet, sklearn) sont effectués **à l'intérieur des fonctions**
pour éviter de ralentir le démarrage de l'application :

.. code-block:: python

   def predict_monthly(df, n_months):
       from prophet import Prophet              # Import local
       from sklearn.metrics import mean_absolute_error
       ...

   def predict_daily_mlp(df, n_days):
       from sklearn.neural_network import MLPRegressor  # Import local
       from sklearn.preprocessing import MinMaxScaler
       ...

Cela permet à Streamlit de charger l'interface instantanément, sans attendre
que tous les modèles soient importés.
