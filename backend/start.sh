#!/bin/bash

python -m ycmd --options_file /ycmd/ycmd/default_settings.json --port ${YCMD_PORT} &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start ycmd: $status"
  exit $status
fi

gunicorn main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker