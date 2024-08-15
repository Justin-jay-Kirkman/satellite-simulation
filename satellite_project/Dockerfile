FROM python:3

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# update schema if needed
RUN python manage.py makemigrations simulation_app
# apply new db structure
RUN python manage.py migrate

CMD ["python","manage.py","runserver", "0.0.0.0:8000"]

