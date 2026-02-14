from pydantic import BaseModel, Field


class Commit(BaseModel):
    message: str
    diff: str


class Staged(BaseModel):
    diffs: str


class LlmCommitAnalysis(BaseModel):
    message: str = Field(description="ONLY the analyzed commit message.")
    score: int = Field(
        description="Score rating the quality of the commit message.", ge=0, le=10
    )
    issue: str | None = Field(
        default=None,
        description="Optionally, describe why this is a poor commit message.",
    )
    suggestion: str | None = Field(
        default=None, description="Optionally, suggest a new, better commit message."
    )
    praise: str | None = Field(
        default=None,
        description="Optionally, explain what is good about this commit message.",
    )
    vague: bool


class LlmCommitMsg(BaseModel):
    changes: list[str]
    message: str
