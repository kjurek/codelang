import base64
import hmac
import hashlib
import json
import requests
import os

from urllib.parse import urljoin
from src import settings, schema


def create_headers(method, path, data=""):
    secret = settings.HMAC_SECRET.encode()
    request = create_request_hmac(method.encode(), path.encode(), data.encode(), secret)
    hmac = base64.b64encode(request)
    return {"x-ycm-hmac": hmac}


def create_hmac(content, hmac_secret):
    if not isinstance(content, bytes):
        raise TypeError("content was not of bytes type; you have a bug!")
    if not isinstance(hmac_secret, bytes):
        raise TypeError("hmac_secret was not of bytes type; you have a bug!")

    return bytes(hmac.new(hmac_secret, msg=content, digestmod=hashlib.sha256).digest())


def create_request_hmac(method, path, body, hmac_secret):
    if not isinstance(body, bytes):
        raise TypeError("body was not of bytes type; you have a bug!")
    if not isinstance(hmac_secret, bytes):
        raise TypeError("hmac_secret was not of bytes type; you have a bug!")
    if not isinstance(method, bytes):
        raise TypeError("method was not of bytes type; you have a bug!")
    if not isinstance(path, bytes):
        raise TypeError("path was not of bytes type; you have a bug!")

    method_hmac = create_hmac(method, hmac_secret)
    path_hmac = create_hmac(path, hmac_secret)
    body_hmac = create_hmac(body, hmac_secret)

    joined_hmac_input = bytes().join((method_hmac, path_hmac, body_hmac))
    return create_hmac(joined_hmac_input, hmac_secret)


def send_get_healthy():
    headers = create_headers("GET", "/healthy")
    url = urljoin(settings.YCMD_URL, "healthy")
    return requests.get(url, headers=headers).json()


def send_load_config():
    data_config = {
        "filepath": os.path.join(".ycm_extra_conf.py")
    }
    headers_config = create_headers("POST", "/load_extra_conf_file", json.dumps(data_config))
    url_config = urljoin(settings.YCMD_URL, "load_extra_conf_file")
    return requests.post(url_config, json=data_config, headers=headers_config)


def send_completions(completions_request: schema.CompletionsRequest):
    data = {
        "line_num": completions_request.line_num,
        "column_num": completions_request.column_num,
        "filepath": completions_request.file_name,
        "file_data": {
            completions_request.file_name: {
                "filetypes": [completions_request.file_type],
                "contents": completions_request.contents
            }
        }
    }
    headers = create_headers("POST", "/completions", json.dumps(data))
    url = urljoin(settings.YCMD_URL, "completions")
    return requests.post(url, json=data, headers=headers).json()
