FROM python:3.10.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ITForum/main

COPY Pipfile Pipfile.lock /ITForum/
RUN pip install pipenv && pipenv install --system
RUN pip install django-debug-toolbar
RUN pip install packaging

COPY . /ITForum/