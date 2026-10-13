# Automated Waste Classification using Predictive Analysis (Django)

## Run (Windows, VS Code terminal)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations classifier
python manage.py migrate
python manage.py generate_dataset
python manage.py train_model
python manage.py createsuperuser   (optional, for /admin)
python manage.py runserver
Open http://127.0.0.1:8000/

## MySQL (optional)
Create DB:  CREATE DATABASE waste_db CHARACTER SET utf8mb4;
Then in the same terminal:
  set DB_ENGINE=mysql
  set DB_NAME=waste_db
  set DB_USER=root
  set DB_PASSWORD=your_password
and run migrate again.
