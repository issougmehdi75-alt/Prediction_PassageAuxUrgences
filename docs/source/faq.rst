.. _faq:

FAQ — Questions fréquentes
============================




Installation
------------

**Q : Pourquoi Python 3.11 et pas une version plus récente ?**

Prophet n'est pas encore compatible avec Python 3.12, 3.13 ou 3.14.
L'utiliser avec ces versions provoque des erreurs à l'installation.
Python 3.11 est la version la plus récente garantie compatible avec toutes les dépendances du projet.




**Q : J'ai l'erreur ``error: Microsoft Visual C++ is required``. Que faire ?**

Prophet compile du code C++ lors de l'installation.
Téléchargez et installez `Visual C++ Build Tools <https://visualstudio.microsoft.com/visual-cpp-build-tools/>`_,
puis relancez ``pip install prophet``.




**Q : L'installation prend très longtemps. Est-ce normal ?**

Oui. Prophet télécharge ``pystan`` et ``cmdstanpy`` qui compilent des binaires C++.
Comptez 5 à 15 minutes selon votre connexion et votre CPU. C'est normal.




Utilisation
-----------

**Q : Mon fichier Excel est bien formaté mais j'obtiens une erreur de date. Pourquoi ?**

Vérifiez que :

1. La colonne de dates ne contient pas de formats mixtes (ex : certaines cellules en ``JJ/MM/AAAA`` et d'autres en ``AAAA-MM-JJ``)
2. Les cellules de date ne sont pas au format numérique Excel (nombre de jours depuis 1900)
3. Il n'y a pas de cellules fusionnées dans la première colonne

Si le problème persiste, ouvrez votre fichier Excel, sélectionnez la colonne de dates,
faites ``Format de cellule`` → ``Texte``, et ressaisissez les dates au format ``AAAA-MM-JJ``.




**Q : Les prévisions pour les mois lointains semblent irréalistes. Pourquoi ?**

Avec seulement 17 mois de données, Prophet manque d'historique pour détecter
une saisonnalité annuelle complète. Plus vous lui fournissez de données historiques,
plus les prévisions éloignées seront fiables. Idéalement, utilisez 2 à 3 années de données.




**Q : Puis-je charger un fichier avec plus de 2 colonnes ?**

Non, l'application lit uniquement les 2 premières colonnes.
Assurez-vous que votre fichier ne contient que les colonnes Date et Passages,
ou que les colonnes Date et Passages sont bien les deux premières.




**Q : L'application est lente à générer les prévisions. Est-ce normal ?**

- **MLP journalier** : 3 à 10 secondes (entraînement du réseau)
- **Prophet mensuel** : 5 à 20 secondes (inférence bayésienne)

C'est normal. Si vous utilisez la version en ligne (Streamlit Cloud),
le serveur peut être en veille — le premier lancement peut prendre 30 à 60 secondes.




**Q : La courbe ne s'affiche pas après les prévisions.**

Ce problème était lié à une incompatibilité entre ``plotly.add_vline()`` et ``pandas >= 2.0``.
Il est corrigé dans la version actuelle du code (utilisation de ``add_shape`` à la place).

Assurez-vous d'utiliser la dernière version du fichier ``streamlit_app.py`` depuis GitHub.




Déploiement Streamlit Cloud
-----------------------------

**Q : L'application déployée affiche ``ModuleNotFoundError: No module named 'plotly'``.**

Votre ``requirements.txt`` sur GitHub ne contient pas ``plotly``.
Ajoutez ``plotly>=5.18.0`` dans le fichier et commitez — Streamlit Cloud redémarrera automatiquement.




**Q : Streamlit Cloud installe les paquets mais l'app plante quand même.**

Vérifiez la version Python utilisée par Streamlit Cloud dans votre ``requirements.txt``
ou dans le tableau de bord. Si c'est Python 3.12+, ajoutez un fichier ``.python-version``
à la racine du repo avec le contenu ``3.11``.




Résultats
---------

**Q : Que signifie la "Fiabilité" affichée sur les cartes ?**

C'est une estimation calculée comme :

.. code-block:: python

   fiabilite = max(0, int(100 - (mae / yhat * 100)))

Si la MAE est de 7 et la prévision est de 250, la fiabilité est ``100 - (7/250*100) ≈ 97%``.
C'est une approximation — à interpréter comme un indicateur de confiance relatif.




**Q : Pourquoi certains mois prévus par Prophet ont des valeurs négatives ou très basses ?**

Cela arrive quand Prophet extrapole trop loin sans suffisamment d'historique.
Avec 17 mois de données, les prévisions au-delà de 6 mois peuvent être instables.
La solution est de fournir plus d'historique.
