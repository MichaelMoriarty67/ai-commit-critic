from pydantic import BaseModel


class Commit(BaseModel):
    message: str
    diff: str


class Staged(BaseModel):
    diffs: str


class LlmCommitAnalysis(BaseModel):
    message: str
    score: int
    issue: str | None = None
    suggestion: str | None = None
    praise: str | None = None
    vague: bool


class LlmCommitMsg(BaseModel):
    changes: list[str]
    message: str
