#!/bin/bash

gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker
