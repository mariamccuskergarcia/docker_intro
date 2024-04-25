#Build stage
FROM alpine:latest as builder

RUN apk add --no-cache \
    python3 \
    py3-pip

WORKDIR /src

COPY ./src/api.py .

COPY ./requirements.txt .

RUN python3 -m venv venv --system-site-packages && source venv/bin/activate && pip install --no-cache-dir --upgrade -r requirements.txt

#Production stage

FROM alpine:latest

ENV PATH=/src/venv/bin:$PATH

RUN apk add --no-cache \
    python3 

COPY --from=builder /src /src

WORKDIR src

#RUN adduser -D uvicornuser && chown -R uvicornuser /src

RUN adduser -D uvicornuser

USER uvicornuser

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "api:app"]


