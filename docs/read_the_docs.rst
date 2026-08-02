Publication sur Read the Docs
=============================

Le fichier ``.readthedocs.yaml`` à la racine configure une construction Sphinx
reproductible avec Ubuntu 22.04 et Python 3.8. Read the Docs installe les
dépendances de l'application puis celles de ``docs/requirements.txt`` et traite
les avertissements Sphinx comme des erreurs.

Première publication
--------------------

1. Construire la documentation localement et corriger tous les avertissements.
2. Ajouter ``docs/``, ``.readthedocs.yaml`` et les autres changements au dépôt,
   puis les pousser sur GitHub.
3. Se connecter à https://readthedocs.org/ avec le compte GitHub qui administre
   le dépôt.
4. Installer l'application GitHub de Read the Docs pour ce dépôt si elle n'est
   pas déjà autorisée.
5. Dans le tableau de bord, choisir **Add project**, sélectionner le dépôt,
   vérifier les informations proposées, puis continuer.
6. Lorsque Read the Docs demande le fichier de configuration, confirmer que
   ``.readthedocs.yaml`` existe.
7. Ouvrir le premier build, vérifier toutes ses étapes, puis ouvrir la version
   ``latest`` de la documentation.

Mises à jour
------------

L'intégration GitHub déclenche ensuite automatiquement une nouvelle
construction après chaque changement envoyé au dépôt. Les erreurs sont
consultables dans l'onglet **Builds** du projet Read the Docs.

Avant chaque publication, la commande locale de référence est :

.. code-block:: bash

   python -m sphinx -W --keep-going -b html docs docs/_build/html

Si le dépôt est importé manuellement sans l'application GitHub, ajouter aussi
l'intégration webhook indiquée par Read the Docs afin de déclencher les builds
à chaque mise à jour.
