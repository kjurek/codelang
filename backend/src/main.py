from base64 import b64encode
from fastapi import FastAPI
from utils import CreateRequestHmac
from urllib.parse import urljoin

import requests
import settings
import logging

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


@app.get("/healthy")
async def get_healthy():
    hmac = b64encode(CreateRequestHmac(b"GET", b"/healthy", b"", settings.HMAC_SECRET.encode()))
    headers = {"x-ycm-hmac": hmac}
    url = urljoin(settings.YCMD_URL, "healthy")
    logging.info(f"url={url}, header={headers}")
    return requests.get(url, headers=headers).json()
