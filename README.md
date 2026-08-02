## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Documentation technique

La documentation Sphinx se trouve dans le dossier `docs/`. Pour la construire
localement :

```bash
pip install --requirement requirements.txt
pip install --requirement docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Ouvrir ensuite `docs/_build/html/index.html`. La publication sur Read the Docs
est configurée par `.readthedocs.yaml`; la procédure d'import du projet est
décrite dans `docs/read_the_docs.rst`.

## Déploiement

### Fonctionnement général

Le déploiement est automatisé par le workflow GitHub Actions
`.github/workflows/ci-cd.yml` :

1. À chaque *push* ou *pull request*, le job `quality` installe les dépendances,
   vérifie Django et les migrations, collecte les fichiers statiques, exécute
   Flake8 puis les tests avec une couverture minimale de 80 %.
2. Lors d'un *push* sur la branche `master`, et uniquement si les contrôles
   précédents réussissent, le job `docker` construit l'image et la publie sur
   Docker Hub avec les tags `sha-<hash-du-commit>` et `latest`.
3. Si la publication de l'image réussit, le job `deploy` appelle le Deploy Hook
   de Render en lui transmettant le tag immuable du commit. Render récupère
   alors cette image et redémarre le Web Service.

Les autres branches exécutent donc les contrôles de qualité, mais ne publient
pas d'image et ne déclenchent aucun déploiement.

### Configuration requise

Configurer dans **GitHub > Settings > Secrets and variables > Actions** :

- les variables `DOCKERHUB_USERNAME` et `DOCKERHUB_REPOSITORY` ;
- le secret `DOCKERHUB_TOKEN`, contenant un jeton autorisé à publier l'image ;
- le secret `RENDER_DEPLOY_HOOK_URL`, généré dans les paramètres du Web Service
  Render.

Créer sur Render un Web Service basé sur une image Docker existante (l'image
initiale actuellement utilisée est `docker.io/ycosy/oc-lettings:latest`) et
utiliser la commande suivante :

```bash
gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT
```

Configurer également les variables d'environnement du service :

```text
SENTRY_DSN=<DSN du projet Sentry>
SECRET_KEY=<clé longue, aléatoire et confidentielle>
DEBUG=False
ALLOWED_HOSTS=<nom-du-service>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<nom-du-service>.onrender.com
```

`SENTRY_DSN` permet à Sentry de recevoir les erreurs de production. Si Render
attribue un autre domaine, adapter `ALLOWED_HOSTS` et
`CSRF_TRUSTED_ORIGINS`. Les valeurs réelles des secrets ne doivent jamais être
ajoutées au dépôt, au Dockerfile ou à l'image.

### Effectuer un déploiement

1. Avant de fusionner, exécuter localement les contrôles utilisés par la CI :

   ```bash
   python manage.py check
   python manage.py makemigrations --check --dry-run
   flake8
   pytest --cov=. --cov-report=term-missing --cov-fail-under=80
   ```

2. Fusionner les changements validés dans `master`, puis pousser cette branche
   sur GitHub. Aucune action manuelle sur Docker Hub ou Render n'est nécessaire.
3. Dans l'onglet **Actions** de GitHub, vérifier successivement les jobs
   `quality`, `docker` et `deploy`. Le déploiement s'arrête automatiquement dès
   qu'un job échoue.
4. Dans Render, vérifier que le dernier déploiement utilise bien l'image
   `sha-<hash-du-commit>` attendue et que le service est démarré.
5. Contrôler en production la page d'accueil, `/admin/`, la navigation et le
   chargement des fichiers statiques. Vérifier aussi dans Sentry qu'une erreur
   de test contrôlée est bien remontée, si nécessaire.

Pour vérifier une image indépendamment de Render, elle peut être téléchargée
et exécutée localement avec Docker :

```bash
docker pull docker.io/<utilisateur>/<dépôt>:sha-<hash-du-commit>
docker run --rm -p 8000:8000 --env-file .env docker.io/<utilisateur>/<dépôt>:sha-<hash-du-commit>
```

Le projet utilise actuellement SQLite dans l'image. Le système de fichiers
d'une instance Render gratuite étant éphémère, les données modifiées en
production peuvent disparaître lors d'un redémarrage ou d'un nouveau
déploiement. Une production nécessitant des données persistantes doit utiliser
une base telle que PostgreSQL ou un stockage persistant approprié.
