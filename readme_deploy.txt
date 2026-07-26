MAINTENANCE DU DEPLOIEMENT RENDER
================================

Derniere mise a jour : 26 juillet 2026

1. OBJECTIF
-----------

L'application Django est livree sous forme d'image Docker publiee sur Docker
Hub, puis executee par un Web Service Render cree a partir d'une image
existante.

Image Docker configuree dans Render :

    docker.io/ycosy/oc-lettings:latest

Le tag "latest" sert a creer le service. La future pipeline GitHub Actions
devra publier un tag propre a chaque commit, par exemple "sha-<commit>", puis
demander a Render de deployer ce tag exact. Cela permet de savoir quelle
version tourne en production et facilite les retours en arriere.


2. CONFIGURATION DU WEB SERVICE RENDER
--------------------------------------

Configuration choisie ou recommandee :

    Nom du service : oc-lettings
    Region : Frankfurt (proche des utilisateurs europeens)
    Type d'instance : Free pour la demonstration
    Health Check Path : /

Docker Command configure dans Render :

    gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT

Pourquoi :

    - Gunicorn est le serveur WSGI de production installe dans l'image.
    - 0.0.0.0 rend le serveur accessible au proxy Render.
    - Render fournit la variable PORT au conteneur.
    - La commande Render remplace le CMD du Dockerfile uniquement sur Render.

Le champ Pre-Deploy Command reste vide pour le moment. Les fichiers statiques
sont deja collectes pendant la construction de l'image Docker.


3. VARIABLES D'ENVIRONNEMENT RENDER
-----------------------------------

Variables attendues :

    SENTRY_DSN=<DSN du projet Sentry>
    SECRET_KEY=<longue valeur aleatoire et confidentielle>
    DEBUG=False
    ALLOWED_HOSTS=oc-lettings.onrender.com
    CSRF_TRUSTED_ORIGINS=https://oc-lettings.onrender.com

Ne jamais enregistrer les valeurs reelles de SENTRY_DSN ou SECRET_KEY dans Git,
le Dockerfile, le README ou l'image Docker.

Si Render attribue un autre nom de domaine au service, mettre a jour
ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS avec le domaine reel.


4. MODIFICATIONS APPORTEES A settings.py
----------------------------------------

SECRET_KEY :

    La cle est maintenant lue depuis la variable d'environnement SECRET_KEY.
    En developpement uniquement, une cle non confidentielle de secours permet
    de lancer le projet sans fichier .env. En production, si DEBUG=False et si
    la variable est absente, Django s'arrete immediatement avec une erreur
    explicite.

DEBUG :

    DEBUG est lu depuis l'environnement. Les valeurs 1, true, yes et on
    activent le mode debug, sans distinction entre majuscules et minuscules.
    Toute autre valeur, notamment False, le desactive.

ALLOWED_HOSTS :

    Les domaines autorises sont lus depuis une liste separee par des virgules.
    En developpement, localhost, 127.0.0.1 et [::1] sont autorises par defaut.
    En production, l'absence de la variable provoque une erreur au demarrage
    afin d'eviter un deploiement qui repondrait uniquement en HTTP 400.

CSRF_TRUSTED_ORIGINS :

    Le projet utilise Django 3.0. Cette version attend des noms d'hotes sans
    "https://". Le code accepte toutefois la valeur complete configuree dans
    Render et retire automatiquement le schema. Si Django est mis a niveau
    vers une version recente, verifier ce comportement dans la documentation
    de la nouvelle version.

HTTPS :

    SECURE_PROXY_SSL_HEADER indique a Django que Render a recu la requete en
    HTTPS avant de la transmettre a Gunicorn.
    SECURE_SSL_REDIRECT redirige les eventuelles requetes HTTP vers HTTPS
    lorsque DEBUG est desactive.
    SECURE_REFERRER_POLICY limite l'envoi de l'en-tete Referer a la meme
    origine.
    SESSION_COOKIE_SECURE et CSRF_COOKIE_SECURE sont actives lorsque DEBUG est
    desactive afin que les cookies sensibles soient envoyes uniquement en
    HTTPS.

    HSTS n'est pas active pour le premier deploiement. Il ne faut l'activer
    qu'apres avoir valide le domaine HTTPS definitif, car un mauvais reglage
    HSTS peut rendre le site inaccessible pendant la duree de la politique.


5. APRES UNE MODIFICATION DU CODE
---------------------------------

settings.py est inclus dans l'image Docker. Une modification locale ne change
donc pas le conteneur deja publie. Il faut obligatoirement :

    1. executer les controles et les tests ;
    2. reconstruire l'image Docker ;
    3. pousser la nouvelle image vers Docker Hub ;
    4. demander a Render de deployer la nouvelle image ;
    5. verifier /, /admin/ et le chargement des fichiers statiques.

Lors de la mise en place de GitHub Actions, le Deploy Hook Render devra etre
enregistre dans le secret GitHub RENDER_DEPLOY_HOOK_URL. Le hook ne doit jamais
etre publie dans le depot.


6. LIMITATIONS CONNUES
----------------------

Le projet utilise actuellement une base SQLite incluse dans l'image.
Le systeme de fichiers d'une instance Render Free est ephemere : les donnees
ajoutees ou modifiees depuis l'administration peuvent disparaitre lors d'une
mise en veille, d'un redemarrage ou d'un nouveau deploiement.

Pour une production avec des donnees persistantes, migrer vers PostgreSQL ou
utiliser une solution de stockage persistant compatible avec l'offre Render.

Une instance Free peut egalement se mettre en veille apres une periode
d'inactivite. La premiere requete suivante peut donc etre plus lente.


7. COHERENCE DES MODELES ET DES MIGRATIONS DANS LA CI
-----------------------------------------------------

Le projet utilise Django 3.0. Les migrations initiales de lettings et profiles
declarent les cles primaires avec models.BigAutoField, mais cette version de
Django ne prend pas encore en charge default_auto_field dans AppConfig comme
les versions recentes.

Les champs id de Address, Letting et Profile sont donc declares explicitement
avec models.BigAutoField dans les modeles. Les options auto_created,
primary_key, serialize et verbose_name reproduisent exactement l'etat inscrit
dans les migrations initiales. Cette declaration conserve les modeles alignes
avec les migrations et permet a la commande suivante de reussir sans generer
de migration artificielle :

    python manage.py makemigrations --check --dry-run

Ne pas retirer ces champs id sans mettre a niveau Django et verifier
l'historique complet des migrations ainsi que la base de donnees existante.
