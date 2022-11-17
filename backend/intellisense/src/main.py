from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.info(request)
    logging.info(exc)
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/healthy")
async def get_healthy():
    return send_get_healthy()


@app.post("/completions")
async def completions(completions_request: CompletionsRequest):
    logging.info(send_load_config())
    completions = send_completions(completions_request)
    logging.info(completions)
    return completions
