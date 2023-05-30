# our base image
FROM python:3.9-slim-buster

RUN pip install uvicorn[standart]

RUN pip install --upgrade pip

RUN pip install fastapi[all]

RUN pip install mysql-connector-python

WORKDIR /app
COPY . /app

EXPOSE 80

CMD python -m uvicorn main:app --reload --host 0.0.0.0
