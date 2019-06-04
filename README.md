[![Try Django 2.2 tutorial](https://static.codingforentrepreneurs.com/media/projects/try-django-22/images/share/try_django_2_2_share.jpg)](https://www.codingforentrepreneurs.com/projects/try-django-22)


### Getting Started

#### Pré requis
- Python Python 3.7.3
- Virtual Environment (pipenv or virtualenv)


#### 1. Systeme s'exploitation utilisé
- Windows: 


#### 2. Création d'un environnement virtuel et installé Django
- python -m venv proj_france_env


#### 3. Création du projet

aller dans le dossier de l'environnement virtuel puis l'activer via: 
- .\proj_france_env\Scripts\activate.bat
- créer un dossier  "test_project" (n'importe où, l'essentiel est d'activer l'environnement virtuel)
- cloner: git clone https://github.com/steairfuz/test_france.git
- aller dans le dossier cloner :  pip install -r requirements.txt


#### 3. Pour le Test 2
- il faut telecharger le Json de l'ID clients OAuth 2.0 de votre API google Calendar
- renommer ce fichier en "client_secret_key.json"
- le mettre dans le dossier "/test_france/mes_models/"
- editer le fichier "/test_france/mes_models/mes_evenements.py":
  - changer la variable de CALENDAR_ID  (Mettre l'ID de votre Google calendar) j'ai utilisé 'kokouvi.sewoavi@gmail.com'
- supprimer le fichier "le_token.json" situé dans le dossier "/test_france/mes_models/" (si le fichier existe)
- Exécuter: python .\mes_models\mes_evenements.py (il faut noter que je suis sur le système Windows)
  le navigateur se lance , on se connete et on a le message "Authentication successful."

#### 4. Lancement du projet
- se positionner dans le projet cloné et lancer: python manage.py runserver
- aller sur http://127.0.0.1:8000







