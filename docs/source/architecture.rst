.. _architecture:

Architecture
============

Arborescence
------------

.. code-block:: text

   ├── streamlit_app.py            interface : pages Introduction et Prédiction
   ├── urgences/                   logique métier (testable sans Streamlit)
   │   ├── donnees.py              lecture/validation Excel, dates françaises
   │   ├── modeles.py              baselines, SARIMA, Prophet, Ridge, GBM, MLP, backtest, intervalles
   │   ├── prevision.py            orchestration « évaluer puis prévoir »
   │   ├── simulation.py           désagrégation mensuel → journalier
   │   ├── graphiques.py           figures Plotly et palette
   │   └── style.py                CSS
   ├── scripts/
   │   ├── simuler_journalier.py   génère data/passages_journaliers_simules.xlsx
   │   └── evaluer_modeles.py      génère results/metriques.json
   ├── data/                       jeux de données du projet
   ├── results/metriques.json      métriques affichées sur la page Introduction
   ├── tests/test_projet.py        tests pytest
   └── .streamlit/config.toml      thème

Flux de la page Prédiction
--------------------------

.. code-block:: text

   Excel ──► donnees.lire_excel ──► df[ds, y] + avertissements
                                       │
                                       ▼
                     prevision.prevoir_mensuel / prevoir_journalier
                        1. backtest du modèle et de la baseline  → MAE, MAPE
                        2. estimation de σ(h) (journalier)
                        3. entraînement sur tout l'historique
                        4. prévision + intervalle 95 %
                                       │
                                       ▼
                     graphiques.figure_prevision · tableau · export Excel

Choix techniques
----------------

- **Séparation interface / logique** : ``urgences/`` n'importe pas Streamlit et est couvert par les tests.
- **Cache** : ``st.cache_data`` sur la lecture des fichiers et le calcul des prévisions (pas de
  réentraînement si les paramètres n'ont pas changé).
- **État** : le résultat est conservé dans ``st.session_state`` avec une clé (mode, horizon, empreinte
  des données). Il reste affiché quand on clique sur « Télécharger » (Streamlit relance le script)
  et disparaît si les entrées changent.
- **Métriques précalculées** : la page Introduction lit ``results/metriques.json`` au lieu de valeurs
  écrites à la main.
- **Palette** : bleu ``#2a78d6`` = observé, orange ``#eb6834`` = prévu, gris = modèles de référence ;
  paire validée pour les daltonismes (protanopie, deutéranopie, tritanopie).
- **Thème** : ``.streamlit/config.toml`` (clair, barre latérale bleu nuit) plutôt que des surcharges CSS
  fragiles.
