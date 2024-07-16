FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements/production.txt



EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata specialties
RUN python manage.py loaddata doctors

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]