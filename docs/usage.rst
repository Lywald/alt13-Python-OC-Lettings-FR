Guide d'utilisation
===================

Consulter une location
----------------------

1. Ouvrir la page d'accueil.
2. Sélectionner **Lettings**.
3. Choisir un titre dans la liste.
4. Consulter l'adresse complète du bien.

Consulter un profil
-------------------

1. Ouvrir la page d'accueil.
2. Sélectionner **Profiles**.
3. Choisir un nom d'utilisateur.
4. Consulter son nom, son adresse électronique et sa ville favorite.

Administrer les données
-----------------------

1. Créer un compte administrateur si nécessaire :

   .. code-block:: bash

      python manage.py createsuperuser

2. Ouvrir ``/admin/`` et s'authentifier.
3. Ajouter ou modifier les utilisateurs, profils, adresses et locations.

Une location doit être associée à une adresse unique et un profil à un
utilisateur unique.

Diagnostiquer une erreur
------------------------

En développement, les journaux apparaissent dans la console qui exécute
``runserver``. En production, les erreurs applicatives de niveau ``ERROR`` sont
aussi envoyées à Sentry lorsque ``SENTRY_DSN`` est configuré.
