.. _changelog:

Historique des versions
========================




Version 1.0.0 — Mai 2025
--------------------------

🎉 **Version initiale — Projet académique**

**Fonctionnalités :**

- Page Introduction avec pipeline, tableau comparatif, graphique des performances et tests statistiques
- Page Prédiction avec upload Excel, slider de plage et export des résultats
- Modèle Prophet pour les prévisions mensuelles
- Modèle MLP (MAE ≈ 7) pour les prévisions journalières
- Intervalles de confiance à 95%
- Courbe interactive Plotly (historique + prévisions + bornes)
- Téléchargement des prévisions en Excel
- Sidebar bleue avec informations du projet
- Fichiers exemples téléchargeables (mensuel 17 mois, journalier 60 jours)

**Corrections de bugs :**

- ✅ Compatibilité pandas 3.0 : remplacement de ``fillna(method=...)`` par ``.bfill().ffill()``
- ✅ Compatibilité pandas 2.0+ : remplacement de ``fig.add_vline(x=Timestamp)`` par ``fig.add_shape()`` + ``fig.add_annotation()``
- ✅ Suppression de ``infer_datetime_format=True`` (supprimé dans pandas 3.0)
- ✅ Parsing de dates multi-formats avec tentatives successives de formats explicites
- ✅ Remplacement de LightGBM (MAE ≈ 47) par MLP (MAE ≈ 7) pour le journalier

**Modèles testés et écartés :**

- LightGBM → remplacé par MLP (MAE 47 vs 7)
- LSTM, GRU → insuffisance de données (< 1000 observations)
- SARIMA+GARCH → MAE trop élevée (≈ 100), modèle linéaire
- XGBoost → bon mais dépassé par MLP
