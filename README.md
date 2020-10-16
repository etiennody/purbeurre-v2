# Purbeurre
App built for project 10 in Python developer path at Openclassrooms.

The startup Pur Beurre wants to develop a web platform for its customers. This site will allow anyone to find a healthy substitute for a food considered "Too fat, too sweet, too salty".

## Online application
https://www.purbeurre.etiennody.fr

## Requirements
* Python 3
* Django
* Psycopg2
* PostgreSQL
* Requests
* Pillow

## Setup
To run this application locally:

* Create a virtual environment. First, install pipenv:
    ```
    pip install --user pipenv
    ```

* Clone / create the application repository:
    ```
    git clone https://github.com/etiennody/purbeurre.git && cd purbeure-v2
    ```

* Install the requirements:
    ```
    pipenv install
    ```

* Activate the pipenv shell:
    ```
    pipenv shell
    ```

* Create a database with PostgreSQL


* Add and update this information in environment variables file named .env in root directory:
    * ENV=local
    * PURBEURRE_DBNAME=yourpurbeurre_dbname
    * PURBEURRE_DBUSER=yourpurbeurre_dbuser
    * PURBEURRE_DBPASSWD=yourpurbeurre_dbpassword

* Import data from Open Food Facts:
    ```
    python manage.py import_off
    ```

* Run Pur Beurre application:
    ````
    python manage.py runserver
    ````

* Launch Django server:
You can visit localhost at https://127.0.0.1:8000/

* Enjoy!