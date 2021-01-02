from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.handlers import (
    send_get_healthy,
    send_load_config,
    send_completions,
)
from src.schema import CompletionsRequest


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)


@app.get("/healthy")
async def get_healthy():
    return send_get_healthy()


@app.post("/completions")
async def completions(completions_request: CompletionsRequest):
    logging.info(send_load_config())
    return send_completions(completions_request)
