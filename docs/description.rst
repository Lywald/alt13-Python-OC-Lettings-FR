Description du projet
=====================

Orange County Lettings est un site web de démonstration destiné à présenter :

* une liste de locations et l'adresse associée à chaque bien ;
* une liste de profils et la ville favorite de chaque utilisateur ;
* une interface d'administration Django permettant de gérer ces données.

Le projet a été restructuré en trois modules :

``oc_lettings_site``
   Configuration globale, page d'accueil, routage principal et pages d'erreur.

``lettings``
   Modèles, vues, routes et gabarits des locations et des adresses.

``profiles``
   Modèle, vues, routes et gabarits des profils utilisateurs.

L'application est servie par Gunicorn en production. WhiteNoise distribue les
fichiers statiques, Sentry centralise les erreurs et GitHub Actions orchestre
les contrôles, la création de l'image Docker et le déploiement sur Render.
