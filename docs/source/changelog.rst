.. _changelog:

Historique des versions
=======================

Version 2.0.0 — novembre 2026
-----------------------------

**Méthodologie**

- Erreurs mesurées **hors-échantillon** par backtest à origine glissante (la MAE de Prophet était
  calculée sur les données d'entraînement ; celle du MLP en prévision à 1 pas avec les vrais lags).
- Ajout de **modèles de référence** (naïf, naïf saisonnier, moyenne mobile) et du **plancher théorique**.
- Comparaison recalculée : SARIMA, Prophet, Ridge, Gradient Boosting, MLP — mêmes données, même protocole.
  Les valeurs non reproductibles (MAE ≈ 7, rangs XGBoost / LightGBM / LSTM / GRU) ont été retirées.
- Suppression de la fuite de données dans les features (``bfill`` sur les lags).
- Intervalle du MLP **croissant avec l'horizon** (au lieu de ± 1,96 σ constant).
- Indicateur « Fiabilité % » remplacé par la MAE / MAPE hors-échantillon et le gain vs référence.
- Prophet : saisonnalité annuelle désactivée sous 24 mois, ``changepoint_prior_scale`` 0,3 → 0,05.
- Tests ADF / KPSS **réellement calculés** (au lieu de cartes génériques).
- Série journalière : simulation documentée et reproductible (tirage multinomial conservant les
  totaux mensuels, profil hebdomadaire explicite) ; limites affichées dans l'application.

**Application**

- Résultats conservés après le téléchargement Excel.
- Mois en français reconnus (« Janvier 2024 », « févr. 2025 »…).
- Contrôles : doublons, jours / mois manquants, colonnes en trop, valeurs incohérentes.
- Option « Données du projet » pour tester sans fichier ; exemples téléchargeables = vrais jeux du projet.
- Export Excel enrichi (feuille Évaluation).
- Cache des calculs ; navigation ``st.navigation``.

**Visualisation**

- Palette unique validée pour le daltonisme : bleu = observé, orange = prévu, gris = références.
- Graphique de prévision simplifié (une bande d'incertitude au lieu de bandes + 2 courbes de bornes).
- Comparaison des modèles en barres horizontales avec plancher théorique.
- Thème Streamlit (``config.toml``), dates et nombres au format français.

**Projet**

- Code découpé en package ``urgences/`` + scripts + tests ``pytest``.
- Fichiers hérités du modèle Streamlit supprimés (``gdp_data.csv``, ``CODEOWNERS``).
- README et documentation alignés sur le code ; dépendances bornées.

Version 1.0.0 — mai 2025
------------------------

Version initiale : pages Introduction et Prédiction, Prophet (mensuel), MLP (journalier),
upload Excel, intervalles à 95 %, export Excel.
