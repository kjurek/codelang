FROM python:3.10

RUN apt-get update && apt-get install -y build-essential cmake patchelf

RUN useradd -ms /bin/bash executor
USER executor

WORKDIR /home/executor
RUN python -m venv venv
RUN . /home/executor/venv/bin/activate && pip install --upgrade pip && pip install pip-tools
COPY requirements.in /tmp
RUN . /home/executor/venv/bin/activate && pip-compile /tmp/requirements.in && pip-sync /tmp/requirements.txt

RUN mkdir /tmp/code

COPY src /home/executor/code/app/src
WORKDIR /home/executor/code/app

CMD . /home/executor/venv/bin/activate && gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker
