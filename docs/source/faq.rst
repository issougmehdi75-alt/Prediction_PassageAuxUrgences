.. _faq:

FAQ
===

**Les données journalières sont-elles réelles ?**
   Non. Seuls les totaux mensuels sont réels ; la série journalière est simulée en conservant
   exactement ces totaux (voir :ref:`simulation`).

**Pourquoi l'erreur affichée est-elle plus élevée que dans la v1 (MAE ≈ 7) ?**
   Parce qu'elle est maintenant mesurée hors-échantillon, en prévision récursive, comme le modèle est
   réellement utilisé. Le plancher théorique des données simulées est 12,2 : un MAE de 7 n'est pas
   atteignable honnêtement sur ces données.

**Pourquoi Prophet n'utilise-t-il pas de saisonnalité annuelle ?**
   Elle nécessite au moins deux cycles complets ; avec 17 mois elle modéliserait le bruit. Elle s'active
   automatiquement à partir de 24 mois d'historique.

**Le MLP est-il vraiment le meilleur modèle journalier ?**
   Il est à égalité avec Ridge et SARIMA (écarts < 2 %). Tous battent nettement les modèles naïfs.

**Pourquoi l'intervalle s'élargit-il ?**
   En prévision récursive, les erreurs s'accumulent : la prévision à 30 jours est plus incertaine qu'à
   1 jour. La v1 utilisait une largeur constante, ce qui sous-estimait l'incertitude.

**Mon fichier est refusé.**
   Vérifiez : 2 colonnes (date, passages), au moins 8 mois ou 60 jours, dates dans un format
   reconnu (voir :ref:`guide_donnees`).

**« Janvier 2024 » n'était pas reconnu.**
   Corrigé en v2 : les mois en français (avec ou sans accents, abrégés ou non) sont acceptés.

**Les résultats disparaissaient après le téléchargement.**
   Corrigé en v2 : ils sont conservés dans ``st.session_state``.

**Comment recalculer les métriques après avoir changé les données ?**
   ``python scripts/evaluer_modeles.py`` puis relancer l'application.
