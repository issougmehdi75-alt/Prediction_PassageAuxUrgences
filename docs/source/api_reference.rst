.. _api_reference:

Référence des fonctions
========================

Documentation complète de chaque fonction du fichier ``streamlit_app.py``.

----

``lire_excel``
--------------

.. code-block:: python

   lire_excel(uploaded_file, granularity="monthly") -> tuple[pd.DataFrame | None, str | None]

Lit, valide et nettoie un fichier Excel uploadé par l'utilisateur.

**Paramètres**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``uploaded_file``
     - ``BytesIO``
     - Objet fichier retourné par ``st.file_uploader``
   * - ``granularity``
     - ``str``
     - ``"monthly"`` (ramène au 1er du mois) ou ``"daily"`` (conserve la date exacte)

**Retourne**

- ``(DataFrame, None)`` : si le fichier est valide. Le DataFrame a les colonnes ``ds`` (datetime) et ``y`` (float).
- ``(None, str)`` : si une erreur est détectée. La chaîne contient le message d'erreur à afficher.

**Erreurs possibles**

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Condition
     - Message retourné
   * - Fichier illisible
     - ``"❌ Impossible de lire le fichier Excel : ..."``
   * - Moins de 2 colonnes
     - ``"❌ Le fichier doit contenir 2 colonnes..."``
   * - Aucune valeur numérique
     - ``"❌ Aucune valeur numérique trouvée..."``
   * - Dates non reconnues
     - ``"❌ La colonne de dates n'est pas reconnue..."``
   * - Moins de 6 lignes valides
     - ``"❌ Seulement N lignes valides. Minimum 6 requis."``

----

``generer_exemple_excel``
--------------------------

.. code-block:: python

   generer_exemple_excel(is_monthly: bool) -> BytesIO

Génère un fichier Excel exemple téléchargeable.

**Paramètres**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``is_monthly``
     - ``bool``
     - ``True`` → génère 17 mois de données. ``False`` → génère 60 jours de données.

**Retourne** : objet ``BytesIO`` prêt pour ``st.download_button``

----

``predict_monthly``
--------------------

.. code-block:: python

   predict_monthly(df: pd.DataFrame, n_months: int) -> tuple[pd.DataFrame, float]

Entraîne Prophet et génère des prévisions mensuelles.

**Paramètres**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``df``
     - ``pd.DataFrame``
     - Données historiques avec colonnes ``ds`` (datetime) et ``y`` (float)
   * - ``n_months``
     - ``int``
     - Nombre de mois futurs à prédire (1–24)

**Retourne** : tuple ``(forecast_df, mae)``

- ``forecast_df`` : DataFrame avec colonnes ``ds``, ``yhat``, ``yhat_lower``, ``yhat_upper``
- ``mae`` : float, erreur absolue moyenne sur les données d'entraînement

----

``predict_daily_mlp``
----------------------

.. code-block:: python

   predict_daily_mlp(df: pd.DataFrame, n_days: int) -> tuple[pd.DataFrame, float]

Entraîne le MLP avec feature engineering et génère des prévisions journalières par itération.

**Paramètres**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``df``
     - ``pd.DataFrame``
     - Données historiques avec colonnes ``ds`` (datetime) et ``y`` (float)
   * - ``n_days``
     - ``int``
     - Nombre de jours futurs à prédire (1–90)

**Retourne** : tuple ``(forecast_df, mae)``

- ``forecast_df`` : DataFrame avec colonnes ``ds``, ``yhat``, ``yhat_lower``, ``yhat_upper``
- ``mae`` : float, erreur absolue moyenne sur l'ensemble de validation (15% des données)

**Sous-fonction interne** : ``make_features(dates, y_series, history_y, idx)``

Construit les 17 features temporelles pour une liste de dates.

----

``plot_forecast``
-----------------

.. code-block:: python

   plot_forecast(df_hist: pd.DataFrame, df_fc: pd.DataFrame,
                 is_monthly: bool, mae: float) -> go.Figure

Génère la figure Plotly avec 5 traces et une ligne de séparation historique/futur.

**Paramètres**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``df_hist``
     - ``pd.DataFrame``
     - Données historiques (colonnes ``ds``, ``y``)
   * - ``df_fc``
     - ``pd.DataFrame``
     - Prévisions (colonnes ``ds``, ``yhat``, ``yhat_lower``, ``yhat_upper``)
   * - ``is_monthly``
     - ``bool``
     - Adapte le titre (mois vs jours)
   * - ``mae``
     - ``float``
     - Affiché dans le titre du graphique

**Retourne** : objet ``plotly.graph_objects.Figure``

**Traces incluses :**

1. Historique (lignes bleues)
2. Bande IC 95% (zone remplie translucide)
3. Prévisions (rouge pointillé, marqueurs diamant)
4. Borne haute (vert tirets)
5. Borne basse (orange tirets)

.. note::

   La ligne verticale de séparation est implémentée avec ``add_shape`` et non
   ``add_vline``, pour compatibilité avec pandas >= 2.0.
