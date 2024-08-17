FROM python:3

# prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# prevents python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# install system dependencies
RUN apt-get update

