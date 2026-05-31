.. _installation:

Installation
============

Ce guide vous accompagne pas à pas pour installer et lancer l'application
sur **Windows**, depuis zéro.

.. contents::
   :local:
   :depth: 2

----

Prérequis système
-----------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Composant
     - Requis
   * - **Système d'exploitation**
     - Windows 10 ou Windows 11 (64-bit)
   * - **Python**
     - **3.11.x** (obligatoire — voir ci-dessous)
   * - **pip**
     - 23.0 ou supérieur (inclus avec Python)
   * - **RAM**
     - 4 Go minimum, 8 Go recommandé
   * - **Espace disque**
     - ~2 Go (modèles + dépendances)
   * - **Connexion Internet**
     - Requise pour l'installation

.. warning::

   ⚠️ **Utilisez impérativement Python 3.11.**

   - Python **3.12 / 3.13 / 3.14** : Prophet n'est **pas encore compatible** avec ces versions.
   - Python **3.9 / 3.10** : peuvent fonctionner mais non testés — risque d'incompatibilités pandas.
   - Python **2.x** : totalement incompatible.

----

Étape 1 — Installer Python 3.11
--------------------------------

1. Allez sur le site officiel : https://www.python.org/downloads/release/python-3119/

2. Téléchargez **"Windows installer (64-bit)"** :

   .. code-block:: text

      Fichier : python-3.11.9-amd64.exe

3. Lancez l'installateur. Sur le premier écran :

   .. important::

      ✅ Cochez **"Add Python 3.11 to PATH"** avant de cliquer sur Install Now.
      C'est l'étape la plus importante — sans ça, rien ne fonctionnera.

4. Cliquez sur **"Install Now"** et attendez la fin.

5. Vérifiez l'installation. Ouvrez l'**Invite de commandes** (``Win + R`` → tapez ``cmd`` → Entrée) :

   .. code-block:: bash

      python --version

   Vous devez voir :

   .. code-block:: text

      Python 3.11.9

   .. code-block:: bash

      pip --version

   Vous devez voir quelque chose comme :

   .. code-block:: text

      pip 23.x.x from ... (python 3.11)

----

Étape 2 — Télécharger le projet
--------------------------------

**Option A — Avec Git (recommandé)**

Si vous avez Git installé (`https://git-scm.com/download/win`) :

.. code-block:: bash

   git clone https://github.com/issougmehdi75-alt/Prediction_PassageAuxUrgences.git
   cd Prediction_PassageAuxUrgences

**Option B — Sans Git**

1. Allez sur https://github.com/issougmehdi75-alt/Prediction_PassageAuxUrgences
2. Cliquez sur **Code** → **Download ZIP**
3. Extrayez le ZIP dans un dossier (ex: ``C:\Projets\Prediction_PassageAuxUrgences``)
4. Ouvrez l'Invite de commandes et naviguez dans ce dossier :

   .. code-block:: bash

      cd C:\Projets\Prediction_PassageAuxUrgences

----

Étape 3 — Créer un environnement virtuel
------------------------------------------

Un environnement virtuel isole les dépendances du projet.
C'est **fortement recommandé** pour éviter les conflits avec d'autres projets Python.

.. code-block:: bash

   python -m venv venv

Activez-le :

.. code-block:: bash

   venv\Scripts\activate

Votre terminal devrait afficher ``(venv)`` au début de la ligne :

.. code-block:: text

   (venv) C:\Projets\Prediction_PassageAuxUrgences>

.. note::

   Pour désactiver l'environnement virtuel plus tard : tapez ``deactivate``

----

Étape 4 — Installer les dépendances
-------------------------------------

Assurez-vous que votre ``requirements.txt`` contient exactement :

.. code-block:: text

   streamlit>=1.30.0
   pandas>=2.0.0
   numpy>=1.24.0
   plotly>=5.18.0
   prophet>=1.1.5
   scikit-learn>=1.3.0
   openpyxl>=3.1.0

Puis installez :

.. code-block:: bash

   pip install -r requirements.txt

L'installation prend **5 à 10 minutes** (Prophet télécharge des dépendances lourdes).

Vérifiez que tout est installé :

.. code-block:: bash

   pip list

Vous devez voir dans la liste : ``streamlit``, ``prophet``, ``plotly``, ``scikit-learn``, ``pandas``, ``numpy``, ``openpyxl``.

----

Étape 5 — Lancer l'application
--------------------------------

.. code-block:: bash

   streamlit run streamlit_app.py

L'application s'ouvre automatiquement dans votre navigateur sur :

.. code-block:: text

   http://localhost:8501

Si elle ne s'ouvre pas automatiquement, copiez cette URL dans votre navigateur.

.. tip::

   Pour arrêter l'application : appuyez sur ``Ctrl + C`` dans le terminal.

----

Dépannage fréquent
-------------------

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - Erreur
     - Solution
   * - ``'python' n'est pas reconnu``
     - Réinstallez Python en cochant "Add to PATH"
   * - ``ModuleNotFoundError: No module named 'plotly'``
     - Ajoutez ``plotly>=5.18.0`` dans ``requirements.txt`` et relancez ``pip install -r requirements.txt``
   * - ``ModuleNotFoundError: No module named 'prophet'``
     - Lancez ``pip install prophet`` dans votre environnement virtuel activé
   * - ``error: Microsoft Visual C++ is required``
     - Installez `Visual C++ Build Tools <https://visualstudio.microsoft.com/visual-cpp-build-tools/>`_
   * - L'app s'ouvre mais plante immédiatement
     - Vérifiez que vous êtes sur Python 3.11 avec ``python --version``
   * - ``Address already in use`` au lancement
     - Lancez sur un autre port : ``streamlit run streamlit_app.py --server.port 8502``
