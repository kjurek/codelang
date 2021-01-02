FROM python

RUN apt-get update && apt-get install -y build-essential cmake
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir /code

WORKDIR /app

CMD gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker