import os
import subprocess
from fastapi import status, HTTPException

from src import schema, settings


def compile(request: schema.CompileRequest):
    dir_path = os.path.join(settings.CODE_DIR, request.session_id)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, "code.cpp")
    with open(file_path, "w") as file_handle:
        file_handle.write(request.contents)

    out_path = os.path.join(dir_path, "out")
    command = ["g++", file_path, "-o", out_path] + request.flags
    output = subprocess.run(command, capture_output=True)

    return schema.CompileResponse(stdout=output.stdout, stderr=output.stderr,
                                  returncode=output.returncode)


def execute(request: schema.ExecuteRequest):
    dir_path = os.path.join(settings.CODE_DIR, request.session_id)
    if not os.path.exists(dir_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session doesn't exist")

    executable_path = os.path.join(dir_path, "out")
    if not os.path.exists(executable_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code isn't compiled")

    command = [executable_path] + request.arguments
    output = subprocess.run(command, capture_output=True)

    return schema.ExecuteResponse(stdout=output.stdout, stderr=output.stderr,
                                  returncode=output.returncode)
