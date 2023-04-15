# our base image
FROM ubuntu

RUN apt install mysql-server

RUN pip install --upgrade pip

RUN pip install fastapi[all]

# run the application
CMD python -m uvicorn main:app --reload --host 0.0.0.0
