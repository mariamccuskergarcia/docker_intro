FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip

COPY ./src/api.py .

COPY ./requirements.txt .

#RUN python3 -m venv .venv --system-site-packages && source .venv/bin/activate && pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install -r requirements.txt --break-system-packages

RUN adduser -D uvicornuser

USER uvicornuser

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "api:app"]

#CMD ["/bin/sh", "-c", "source .venv/bin/activate;uvicorn --host=0.0.0.0 --port=8000 api:app"]

