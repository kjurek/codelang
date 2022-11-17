#!/bin/bash
python -m ycmd --options_file /home/intellisense/ycmd/ycmd/default_settings.json --port ${YCMD_PORT} &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start ycmd: $status"
  exit $status
fi
