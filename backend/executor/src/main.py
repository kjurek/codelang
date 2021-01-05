from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src import handlers, schema

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)


@app.post("/compile", response_model=schema.CompileResponse)
async def compile(request: schema.CompileRequest):
    return handlers.compile(request)


@app.post("/execute", response_model=schema.ExecuteResponse)
async def execute(request: schema.ExecuteRequest):
    return handlers.execute(request)
