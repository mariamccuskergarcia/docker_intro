FROM python:3.10

COPY ./src/api.py .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "api:app"]