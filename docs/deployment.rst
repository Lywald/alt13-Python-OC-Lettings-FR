Déploiement et gestion de l'application
=======================================

Pipeline CI/CD
--------------

Le workflow ``.github/workflows/ci-cd.yml`` suit trois étapes :

1. ``quality`` contrôle Django, les migrations, le style, les tests, la
   couverture et la documentation ;
2. ``docker`` construit et publie l'image Docker après un ``push`` réussi sur
   ``master`` ;
3. ``deploy`` demande à Render de récupérer l'image exacte du commit.

Les images reçoivent les tags ``sha-<hash-du-commit>`` et ``latest``. Seule la
branche ``master`` publie et déploie une image ; les autres branches exécutent
uniquement les contrôles.

Configuration GitHub
--------------------

Définir dans **Settings > Secrets and variables > Actions** :

* variables : ``DOCKERHUB_USERNAME`` et ``DOCKERHUB_REPOSITORY`` ;
* secrets : ``DOCKERHUB_TOKEN`` et ``RENDER_DEPLOY_HOOK_URL``.

Configuration Render
--------------------

Créer un Web Service à partir de l'image Docker et utiliser :

.. code-block:: bash

   gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT

Définir les variables d'environnement suivantes :

.. code-block:: text

   SENTRY_DSN=<DSN du projet Sentry>
   SECRET_KEY=<clé longue et aléatoire>
   DEBUG=False
   ALLOWED_HOSTS=<nom-du-service>.onrender.com
   CSRF_TRUSTED_ORIGINS=https://<nom-du-service>.onrender.com

Procédure de déploiement
------------------------

1. Exécuter localement les contrôles présentés dans le :doc:`quickstart`.
2. Fusionner les changements validés dans ``master`` et pousser la branche.
3. Vérifier les jobs ``quality``, ``docker`` et ``deploy`` dans GitHub Actions.
4. Vérifier dans Render que l'image déployée porte le tag du commit attendu.
5. Contrôler ``/``, ``/admin/``, les listes, les détails et les fichiers
   statiques.
6. Contrôler les événements et journaux dans Sentry.

Retour en arrière
-----------------

Chaque image étant identifiée par le hash du commit, sélectionner dans Render
le dernier tag ``sha-...`` connu comme stable, puis redéployer cette image.
Après le redémarrage, répéter les contrôles fonctionnels.

Surveillance et maintenance
---------------------------

* Examiner régulièrement les événements Sentry et les journaux Render.
* Ne jamais enregistrer ``SENTRY_DSN``, ``SECRET_KEY`` ou le Deploy Hook dans
  Git.
* Après une modification de modèle, créer et tester les migrations avant le
  déploiement.
* Mettre à jour les dépendances dans une branche dédiée, puis exécuter toute la
  CI avant fusion.
* Vérifier le certificat HTTPS et les domaines autorisés après tout changement
  de nom de service.

Limite de persistance
---------------------

SQLite est actuellement inclus dans l'image Docker. Le système de fichiers
d'une instance Render gratuite est éphémère : des données saisies en production
peuvent disparaître après un redémarrage ou un déploiement. Pour conserver des
données de production, migrer vers PostgreSQL ou vers un stockage persistant.
