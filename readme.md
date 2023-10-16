# Epic Events

Epic Events est une application de gestion d'événements conçue avec Django et Django Rest Framework. 
Elle permet aux utilisateurs de créer des clients, des contrats et des événements, tout en suivant les meilleures pratiques de sécurité.

### Configuration du projet: 
Cloner le projet depuis votre éditeur de code : 
```
git clone https://github.com/barseille/epic_events.git
```
### Installer pipenv : 
```
pip install pipenv
```
### Créez un dossier .venv : 
```
mkdir .venv
```
### Créer un environnement virtuel : 
```
python -m venv .venv
```
### Activer l'environnement virtuel :
Pour Windows :
```
.\.venv\Scripts\Activate
```
Pour macOS ou Linux :
```
pipenv shell
```
### Mise à jour "pip" si besoin à l'aide cette commande :
```
python -m pip install --upgrade pip
```
### Installez les dépendances :
Avec l'environnement virtuel activé, installez les dépendances requises :
```
pip install -r requirements.txt
```
### Configuration de la base de données : 
Exécutez les migrations de la base de données avec :
```
python manage.py migrate
```
### Exécution du serveur : 
```
python manage.py runserver
```
