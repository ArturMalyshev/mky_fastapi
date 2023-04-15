# our base image
FROM python:3-onbuild

RUN pip install uvicorn[standart]

RUN pip install --upgrade pip

RUN pip install fastapi[all]

RUN pip install mysql-connector-python

# run the application
CMD python -m uvicorn main:app --reload --host 0.0.0.0
