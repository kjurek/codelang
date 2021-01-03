import os
import subprocess  # nosec
from fastapi import status, HTTPException

from src import schema, settings

import logging

SOURCE_NAME = "code.cpp"
EXECUTABLE_NAME = "out"


def compile_executable(source_path: str, flags: list, executable_path: str):
    command = ["g++", source_path, "-o", executable_path] + flags
    output = subprocess.run(command, capture_output=True)  # nosec
    logging.info(f"compile_executable output: {output}")
    return output


def link_sandbox(executable_path: str):
    command = ["patchelf", "--add-needed", settings.SANDBOX_LIB_PATH, executable_path]
    output = subprocess.run(command, capture_output=True)  # nosec
    logging.info(f"link_sandbox output: {output}")
    return output


def run_executable(executable_path: str, arguments: list):
    command = ["runuser", "-u", settings.CODE_USER, "--", executable_path] + arguments
    output = subprocess.run(command, capture_output=True)  # nosec
    logging.info(f"run_executable output: {output}")
    return output


def filter_sandbox_messages(stderr: str):
    messages = '\n'.join([
        'initializing seccomp with default action (kill process)',
        'adding read to the process seccomp filter (allow)',
        'adding open to the process seccomp filter (allow)',
        'adding write to the process seccomp filter (allow)',
        'adding exit_group to the process seccomp filter (allow)',
        'adding fstat to the process seccomp filter (allow)\n',
    ])
    return stderr.replace(messages, '')


def compile(request: schema.CompileRequest):
    dir_path = os.path.join(settings.CODE_DIR, request.session_id)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    source_path = os.path.join(dir_path, SOURCE_NAME)
    with open(source_path, "w") as file_handle:
        file_handle.write(request.contents)

    executable_path = os.path.join(dir_path, EXECUTABLE_NAME)
    if os.path.exists(executable_path):
        os.remove(executable_path)

    compile_output = compile_executable(source_path, request.flags, executable_path)
    if os.path.exists(executable_path):
        link_sandbox(executable_path)

    return schema.CompileResponse(stdout=compile_output.stdout,
                                  stderr=compile_output.stderr,
                                  returncode=compile_output.returncode)


def execute(request: schema.ExecuteRequest):
    dir_path = os.path.join(settings.CODE_DIR, request.session_id)
    if not os.path.exists(dir_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session doesn't exist")

    executable_path = os.path.join(dir_path, EXECUTABLE_NAME)
    if not os.path.exists(executable_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code isn't compiled")

    output = run_executable(executable_path, request.arguments)
    return schema.ExecuteResponse(stdout=output.stdout,
                                  stderr=filter_sandbox_messages(output.stderr.decode()),
                                  returncode=output.returncode)
