FROM python:alpine3.19

COPY ./src/department_microservice.py .

COPY ./src/db.py .

COPY ./src/data.py .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "department_microservice:app"]