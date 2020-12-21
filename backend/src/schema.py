from pydantic import BaseModel


class CompletionsRequest(BaseModel):
    file_name: str
    file_type: str
    line_num: int
    column_num: int
    contents: str
