from pydantic import BaseModel


class Commit(BaseModel):
    message: str
    diff: str
