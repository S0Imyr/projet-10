# projet 10


### Principe et configuration nécessaire :
Il s'agit de créer une API qui fournit un ensemble de endpoints utilisée par diverses applications web Androïd. Ces applications permettront le suivi et des échanges sur des projets de développement divers.

Ce projet nécessite d'installer python, django et PostgreSQL.

## Installation
### Fichiers du site
Sur le terminal se placer sur un dossier cible.

Puis suivre les étapes suivantes :
1. Cloner le dépôt ici présent en tapant: `$ git clone https://github.com/S0Imyr/Projet-10.git`
2. Accéder au dossier ainsi créé avec la commande : `$ cd Projet-10`
3. Créer un environnement virtuel pour le projet avec 
    - `$ python -m venv env` sous windows 
    - ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec 
    - `$ source env/Scripts/activate` sous windows 
    - ou `$ source env/bin/activate` sous MacOS ou Linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`

### Lancement du serveur
Revenir dans le terminal et tapper :

6. Démarrer le serveur avec `$ python manage.py runserver`


Une fois installé, toutes les étapes ne sont pas nécessaires. Pour les lancements ultérieurs du serveur de l'API, il suffit d'exécuter les étapes 4 et 6 à partir du répertoire racine du projet.

## Arrêter le serveur

Pour arrêter le serveur aller dans le terminal où il a été lancé, puis appuyer sur les touches Ctrl+C.