# Doctorex

## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/G4-Team/Doctorex.git
```
2- SetUp a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
or
```
python -m venv venv
venv/scripts/activate
```
3- install Dependencies
```
pip install -r requirements/local.txt
```
4- make migrations
```
python manage.py makemigrations
```
5- migrate
```
python manage.py migrate
```
6- make default specialties and related images
```
python manage.py collectmedia
python manage.py loaddata specialties
```
7- create an admin
```
python manage.py createsuperuser
```
8- run the program
```
python manage.py runserver
```