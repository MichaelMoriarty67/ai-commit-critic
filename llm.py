import os
import asyncio
from typing import List

from openai import AsyncOpenAI
from dotenv import load_dotenv

from schemas import Commit, LlmCommitAnalysis

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_client = AsyncOpenAI(api_key=openai_api_key)


async def llm_analyze_commit(commit: Commit) -> LlmCommitAnalysis:

    system_msg = """Your goal is to provide HONEST git commit message reviews. You will be given
a commit message and the diff of files changed in that specific commit.

For scores that you would give a 5/10 or below, include an issue and suggest a new, better commit message. 
Suggestions should follow follow the "Conventional Commits" style, but just because a message doesn't use this style doesn't mean its bad. 
Additionally, you can set vague to "True" if the score is <= 5/10 and you think that the commit message was too vague.

For scores above 5/10, include a short praise message detailing why this was a good commit message."""
    model = "gpt-5-nano"

    user_msg = f"Commit Message: {commit.message}/n/nFiles Diff: {commit.diff}"

    response = await llm_client.responses.parse(
        model=model,
        instructions=system_msg,
        text_format=LlmCommitAnalysis,
        input=user_msg,
    )

    return response.output_parsed


async def llm_analyze_commits(commits: List[Commit]) -> List[LlmCommitAnalysis]:
    analysis_tasks = [llm_analyze_commit(commit) for commit in commits]
    analysis_results = await asyncio.gather(*analysis_tasks)

    return analysis_results
