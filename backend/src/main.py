from base64 import b64encode
from fastapi import FastAPI
from urllib.parse import urljoin


from src.utils import CreateRequestHmac
from src import settings, schema

import json
import logging
import requests
import os

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


def create_headers(method, path, data=""):
    secret = settings.HMAC_SECRET.encode()
    hmac = b64encode(CreateRequestHmac(method.encode(), path.encode(), data.encode(), secret))
    return {"x-ycm-hmac": hmac}


@app.get("/healthy")
async def get_healthy():
    headers = create_headers("GET", "/healthy")
    url = urljoin(settings.YCMD_URL, "healthy")
    logging.info(f"url={url}, header={headers}")
    return requests.get(url, headers=headers).json()


@app.post("/completions")
async def completions(completions_request: schema.CompletionsRequest):
    filepath = os.path.join("/code", completions_request.file_name)
    with open(filepath, "w") as f_code:
        f_code.write(completions_request.contents)

    data_config = {
        "filepath": "/code/.ycm_extra_conf.py"
    }
    headers_config = create_headers("POST", "/load_extra_conf_file", json.dumps(data_config))
    url_config = urljoin(settings.YCMD_URL, "load_extra_conf_file")
    response_config = requests.post(url_config, json=data_config, headers=headers_config)
    logging.info(response_config)

    data_event = {
        "line_num": completions_request.line_num,
        "column_num": completions_request.column_num,
        "filepath": filepath,
        "file_data": {
            filepath: {
                "filetypes": [completions_request.file_type],
                "contents": completions_request.contents
            }
        },
        "event_name": "FileReadyToParse"
    }
    headers_event = create_headers("POST", "/event_notification", json.dumps(data_event))
    url_event = urljoin(settings.YCMD_URL, "event_notification")
    response_event = requests.post(url_event, json=data_event, headers=headers_event).json()
    logging.info(response_event)

    data = {
        "line_num": completions_request.line_num,
        "column_num": completions_request.column_num,
        "filepath": filepath,
        "file_data": {
            filepath: {
                "filetypes": [completions_request.file_type],
                "contents": completions_request.contents
            }
        }
    }
    headers = create_headers("POST", "/completions", json.dumps(data))
    url = urljoin(settings.YCMD_URL, "completions")
    logging.info(f"url={url}, request={data}, header={headers}")
    return requests.post(url, json=data, headers=headers).json()
