FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements/production.txt

EXPOSE 8000

RUN mkdir db

RUN python manage.py migrate
RUN python manage.py loaddata specialties
RUN python manage.py loaddata doctors
RUN python manage.py collectstatic --noinput

CMD [ "gunicorn", "doctorex.wsgi:application", "-b", "0.0.0.0:8000" ]