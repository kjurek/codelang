from pydantic import BaseModel

from typing import List, Optional


class CompileRequest(BaseModel):
    session_id: str
    contents: str
    flags: List[str]


class ExecuteRequest(BaseModel):
    session_id: str
    arguments: List[str]


class CompileResponse(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    returncode: Optional[int]


class ExecuteResponse(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    returncode: Optional[int]
