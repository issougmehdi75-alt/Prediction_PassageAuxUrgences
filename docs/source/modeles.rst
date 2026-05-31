.. _modeles:

Documentation des modèles
==========================

Présentation technique des deux modèles retenus pour l'application.

.. contents::
   :local:
   :depth: 2

----

Choix des modèles
-----------------

Après avoir testé 6 modèles sur les données de l'hôpital, deux ont été retenus :

.. list-table::
   :widths: 20 30 25 25
   :header-rows: 1

   * - Usage
     - Modèle
     - MAE
     - Raison du choix
   * - **Mensuel**
     - Prophet (Facebook/Meta)
     - Excellent
     - Gère nativement les tendances et saisonnalités annuelles
   * - **Journalier**
     - MLP (scikit-learn)
     - ≈ 7 passages/jour
     - Meilleure précision, pas de dépendance lourde (TensorFlow)

----

Modèle 1 — Prophet (Prévision mensuelle)
-----------------------------------------

Présentation
^^^^^^^^^^^^

`Prophet <https://facebook.github.io/prophet/>`_ est un modèle de séries temporelles
développé par l'équipe Core Data Science de **Meta (Facebook)**, publié en 2017.

Il décompose la série temporelle en trois composantes :

.. math::

   y(t) = g(t) + s(t) + h(t) + \epsilon_t

Où :

- :math:`g(t)` : **tendance** (croissance linéaire ou logistique)
- :math:`s(t)` : **saisonnalité** (annuelle, hebdomadaire, journalière)
- :math:`h(t)` : **effets des jours fériés** (optionnel)
- :math:`\epsilon_t` : **résidu** (bruit aléatoire)

Configuration utilisée
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from prophet import Prophet

   model = Prophet(
       yearly_seasonality=True,    # Saisonnalité annuelle activée
       weekly_seasonality=False,   # Désactivée (données mensuelles)
       daily_seasonality=False,    # Désactivée (données mensuelles)
       interval_width=0.95,        # Intervalle de confiance à 95%
       changepoint_prior_scale=0.3 # Flexibilité de la tendance
   )
   model.fit(df)  # df avec colonnes 'ds' (date) et 'y' (passages)

   future = model.make_future_dataframe(periods=n_months, freq="MS")
   forecast = model.predict(future)

Paramètre clé — ``changepoint_prior_scale``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ce paramètre contrôle la flexibilité de la tendance :

- **Valeur faible (0.01–0.1)** : tendance rigide, moins sensible aux changements brusques
- **Valeur 0.3 (utilisée)** : équilibre entre flexibilité et stabilité
- **Valeur élevée (0.5+)** : tendance très flexible, risque de surapprentissage

Sorties du modèle
^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Colonne
     - Description
   * - ``yhat``
     - Prévision centrale
   * - ``yhat_lower``
     - Borne inférieure de l'IC à 95%
   * - ``yhat_upper``
     - Borne supérieure de l'IC à 95%
   * - ``trend``
     - Composante tendance uniquement
   * - ``yearly``
     - Composante saisonnalité annuelle

Avantages
^^^^^^^^^

- ✅ Gère automatiquement les tendances et saisonnalités
- ✅ Robuste aux données manquantes et aux valeurs aberrantes
- ✅ Intervalles de confiance natifs
- ✅ Pas besoin de stationnarisation préalable

Limites
^^^^^^^

- ❌ Nécessite un historique suffisant (minimum 6 mois, idéalement 2 ans)
- ❌ Moins adapté aux données journalières à forte variabilité

----

Modèle 2 — MLP (Prévision journalière)
-----------------------------------------

Présentation
^^^^^^^^^^^^

Le **Multi-Layer Perceptron (MLP)** est un réseau de neurones artificiels composé de
plusieurs couches denses entièrement connectées. L'implémentation utilise
`MLPRegressor <https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html>`_
de **scikit-learn**.

Architecture du réseau
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Entrée (17 features)
        ↓
   Couche cachée 1 : 128 neurones — activation ReLU
        ↓
   Couche cachée 2 : 64 neurones  — activation ReLU
        ↓
   Couche cachée 3 : 32 neurones  — activation ReLU
        ↓
   Sortie : 1 valeur (nombre de passages prédit)

Feature Engineering
^^^^^^^^^^^^^^^^^^^

Le MLP n'a pas de mémoire temporelle native. Pour compenser, 17 features sont construites
à partir de chaque date :

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Feature
     - Type
     - Description
   * - ``lag_1``, ``lag_2``, ``lag_3``
     - Temporelle
     - Valeurs des 1, 2, 3 jours précédents
   * - ``lag_7``, ``lag_14``
     - Temporelle
     - Valeurs J-7 et J-14 (mémoire hebdomadaire)
   * - ``roll_7``, ``roll_14``
     - Statistique
     - Moyenne glissante sur 7 et 14 jours
   * - ``dow_sin``, ``dow_cos``
     - Cyclique
     - Encodage circulaire du jour de la semaine
   * - ``month_sin``, ``month_cos``
     - Cyclique
     - Encodage circulaire du mois
   * - ``dayofweek``
     - Calendaire
     - Lundi = 0, Dimanche = 6
   * - ``dayofmonth``
     - Calendaire
     - Jour dans le mois (1–31)
   * - ``month``
     - Calendaire
     - Mois (1–12)
   * - ``quarter``
     - Calendaire
     - Trimestre (1–4)
   * - ``dayofyear``
     - Calendaire
     - Jour dans l'année (1–366)

.. note::

   L'encodage cyclique (sin/cos) est essentiel pour que le réseau comprenne
   que le lundi suit le dimanche, et que janvier succède à décembre.

Configuration et entraînement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sklearn.neural_network import MLPRegressor
   from sklearn.preprocessing import MinMaxScaler

   # Normalisation des données
   scaler_X = MinMaxScaler()
   scaler_y = MinMaxScaler()

   # Modèle
   model = MLPRegressor(
       hidden_layer_sizes=(128, 64, 32),
       activation="relu",
       max_iter=1000,
       random_state=42,
       early_stopping=True,       # Arrêt si pas d'amélioration
       validation_fraction=0.1,   # 10% pour la validation
       learning_rate_init=0.001,  # Taux d'apprentissage Adam
       n_iter_no_change=20        # Patience = 20 epochs
   )

   # Découpage train/validation : 85% / 15%
   split = max(int(len(df) * 0.85), len(df) - 30)

Prévision itérative
^^^^^^^^^^^^^^^^^^^^

Pour prédire plusieurs jours en avance, le modèle utilise une **stratégie itérative** :

.. code-block:: text

   Jour 1 : prédire J+1 à partir de l'historique réel
   Jour 2 : prédire J+2 à partir de l'historique réel + prédiction J+1
   Jour 3 : prédire J+3 à partir de l'historique réel + prédictions J+1, J+2
   ...

Cela permet de prédire jusqu'à 90 jours mais induit une accumulation d'erreur
sur les longues horizons de prévision.

Intervalles de confiance
^^^^^^^^^^^^^^^^^^^^^^^^^

Les bornes sont calculées à partir de l'écart-type des résidus sur l'ensemble de validation :

.. math::

   IC_{95\%} = \hat{y} \pm 1.96 \times \sigma_{résidus}

Avantages
^^^^^^^^^

- ✅ MAE ≈ 7 passages/jour (meilleur résultat parmi tous les modèles testés)
- ✅ Capture les patterns non-linéaires complexes
- ✅ Aucune dépendance à TensorFlow/Keras
- ✅ Rapide à entraîner (quelques secondes)

Limites
^^^^^^^

- ❌ Accumulation d'erreur sur les longues prévisions (> 30 jours)
- ❌ Nécessite suffisamment de données pour bien généraliser
- ❌ Pas de mémoire séquentielle native (contrairement à LSTM/GRU)
