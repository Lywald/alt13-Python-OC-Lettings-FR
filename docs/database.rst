Base de données et modèles
==========================

Le projet utilise SQLite. La base locale est configurée dans
``oc_lettings_site/settings.py`` sous le nom ``oc-lettings-site.sqlite3``.

Relations
---------

::

   django.contrib.auth.User  1 ───── 1  Profile
   Address                   1 ───── 1  Letting

Les deux relations utilisent ``OneToOneField`` avec suppression en cascade :
la suppression d'un utilisateur supprime son profil, et celle d'une adresse
supprime la location associée.

Address
-------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Champ
     - Type
     - Contraintes
   * - ``id``
     - ``BigAutoField``
     - clé primaire
   * - ``number``
     - ``PositiveIntegerField``
     - maximum 9999
   * - ``street``
     - ``CharField(64)``
     -
   * - ``city``
     - ``CharField(64)``
     -
   * - ``state``
     - ``CharField(2)``
     - longueur minimale 2
   * - ``zip_code``
     - ``PositiveIntegerField``
     - maximum 99999
   * - ``country_iso_code``
     - ``CharField(3)``
     - longueur minimale 3

Letting
-------

============= ======================== ================================
Champ         Type                     Contraintes
============= ======================== ================================
``id``        ``BigAutoField``         clé primaire
``title``     ``CharField(256)``
``address``   ``OneToOneField``        référence unique vers ``Address``
============= ======================== ================================

Profile
-------

================= ======================== ================================
Champ             Type                     Contraintes
================= ======================== ================================
``id``            ``BigAutoField``         clé primaire
``user``          ``OneToOneField``        référence unique vers ``User``
``favorite_city`` ``CharField(64)``        valeur vide autorisée
================= ======================== ================================

Migrations
----------

Après une modification de modèle :

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

Les fichiers de migration doivent être relus et ajoutés au même commit que la
modification de modèle. La CI vérifie qu'aucune migration ne manque avec :

.. code-block:: bash

   python manage.py makemigrations --check --dry-run
