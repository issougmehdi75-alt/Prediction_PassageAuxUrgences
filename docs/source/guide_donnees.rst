.. _guide_donnees:

Format des données
==================

L'application accepte uniquement des fichiers **Excel (.xlsx ou .xls)**.
Cette page explique le format exact attendu.

.. contents::
   :local:
   :depth: 2

----

Structure obligatoire
---------------------

Le fichier doit comporter **exactement 2 colonnes** :

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Colonne
     - Contenu
     - Exemples de valeurs valides
   * - **Colonne A**
     - Date
     - ``2024-01-01``, ``01/01/2024``, ``Janvier 2024``, ``Jan 2024``
   * - **Colonne B**
     - Nombre de passages (entier positif)
     - ``245``, ``7340``, ``1892``

.. note::

   Les en-têtes de colonnes (``Date``, ``Mois``, ``Passages``) sont détectés et ignorés
   automatiquement. Inutile de les supprimer.

----

Format mensuel
--------------

Pour la **prévision mensuelle** (modèle Prophet).

Exemple de fichier valide :

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Mois
     - Passages
   * - 2024-01-01
     - 7340
   * - 2024-02-01
     - 6850
   * - 2024-03-01
     - 7120
   * - 2024-04-01
     - 7400
   * - ...
     - ...

.. tip::

   - Minimum **6 mois** de données historiques requis
   - Idéalement **12 mois ou plus** pour que Prophet détecte la saisonnalité annuelle
   - Toutes les dates sont ramenées au **1er du mois** automatiquement

----

Format journalier
-----------------

Pour la **prévision journalière** (modèle MLP).

Exemple de fichier valide :

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Date
     - Passages
   * - 2024-01-01
     - 245
   * - 2024-01-02
     - 231
   * - 2024-01-03
     - 258
   * - 2024-01-04
     - 212
   * - ...
     - ...

.. tip::

   - Minimum **6 jours** de données (mais **30 jours ou plus** recommandés)
   - Plus vous avez de données, plus le MLP sera précis
   - Les données peuvent comporter des trous (jours manquants) — ils sont gérés

----

Formats de dates acceptés
--------------------------

L'application reconnaît automatiquement tous ces formats :

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Format
     - Exemple
   * - ``YYYY-MM-DD``
     - ``2024-01-15``
   * - ``DD/MM/YYYY``
     - ``15/01/2024``
   * - ``MM/DD/YYYY``
     - ``01/15/2024``
   * - ``DD-MM-YYYY``
     - ``15-01-2024``
   * - ``YYYY/MM/DD``
     - ``2024/01/15``
   * - Nom complet du mois + année
     - ``Janvier 2024``
   * - Nom abrégé du mois + année
     - ``Jan 2024``

----

Règles à respecter
-------------------

✅ **À faire :**

- 2 colonnes uniquement (Date + Passages)
- Données triées par ordre chronologique
- Valeurs numériques entières dans la colonne Passages
- Un en-tête optionnel sur la première ligne

❌ **À éviter :**

- Plus de 2 colonnes dans le fichier
- Cellules fusionnées
- Lignes vides au milieu des données
- Valeurs négatives ou textuelles dans la colonne Passages
- Dates dans un format non standard (ex: ``15 janv. 24``)
- Plusieurs feuilles dans le fichier (seule la première est lue)

----

Télécharger les exemples
-------------------------

Des fichiers exemples sont disponibles directement depuis l'application :

1. Allez sur la page **Prédiction**
2. Choisissez le type (Mensuel ou Journalier)
3. Dans le bloc "Format attendu", cliquez sur **"⬇️ Télécharger un exemple Excel"**

Ces fichiers contiennent des données réalistes et peuvent être utilisés pour tester
l'application immédiatement.
