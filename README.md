# main

Projecte participant a la Hackovid, hackató ciutadana per afrontar el confinament pel COVID-19.

## Create venv

```bash
python3 -m venv ./venv-dropplets
source venv-dropplets/bin/activate
pip install -r requirements.txt
```

## Makemigrations

````bash
cd tickets-backend
python manage.py makemigrations
````

## Migrate

````bash
cd tickets-backend
python manage.py migrate
````

## Create superuser

````bash
cd tickets-backend
python manage.py createsuperuser
````

## Serve

````bash
cd tickets-backend
python manage.py runserver
````
