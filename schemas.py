from pydantic import BaseModel


class Commit(BaseModel):
    message: str
    diff: str


class LlmCommitAnalysis(BaseModel):
    message: str
    score: int
    issue: str | None = None
    praise: str | None = None
    suggestion: str | None = None
