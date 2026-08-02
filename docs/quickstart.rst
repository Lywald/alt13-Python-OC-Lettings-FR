Démarrage rapide
================

Après avoir activé l'environnement virtuel et installé les dépendances :

.. code-block:: bash

   python manage.py migrate
   python manage.py runserver

Ouvrir ensuite http://127.0.0.1:8000/ dans un navigateur. Les boutons
**Lettings** et **Profiles** permettent d'accéder aux deux parties publiques du
site.

Contrôles avant une modification
--------------------------------

.. code-block:: bash

   python manage.py check
   python manage.py makemigrations --check --dry-run
   flake8
   pytest --cov=. --cov-report=term-missing --cov-fail-under=80

Construction locale de la documentation
----------------------------------------

.. code-block:: bash

   pip install --requirement docs/requirements.txt
   python -m sphinx -W --keep-going -b html docs docs/_build/html

Le résultat est disponible dans ``docs/_build/html/index.html``.
