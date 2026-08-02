Installation
============

Prérequis
---------

* Git ;
* Python 3.8, version utilisée par la CI et l'image Docker ;
* ``pip`` ;
* SQLite, facultatif pour inspecter manuellement la base.

Installation sous macOS ou Linux
--------------------------------

.. code-block:: bash

   git clone <URL_DU_DEPOT>
   cd alt13-Python-OC-Lettings-FR
   python -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install --requirement requirements.txt
   cp .env.example .env
   python manage.py migrate

Installation sous Windows PowerShell
------------------------------------

.. code-block:: powershell

   git clone <URL_DU_DEPOT>
   Set-Location alt13-Python-OC-Lettings-FR
   py -3.8 -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install --requirement requirements.txt
   Copy-Item .env.example .env
   python manage.py migrate

Variables locales
-----------------

Le fichier ``.env`` est ignoré par Git. Pour un lancement local, conserver
``DEBUG=True`` et ``ALLOWED_HOSTS=localhost,127.0.0.1``. Le champ
``SENTRY_DSN`` peut rester vide pour désactiver l'envoi vers Sentry.

Ne jamais placer une vraie ``SECRET_KEY`` ou un DSN Sentry dans un fichier
versionné.
