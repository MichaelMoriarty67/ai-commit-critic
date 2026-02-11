import os
import asyncio
from typing import List

from openai import AsyncOpenAI, OpenAI
from dotenv import load_dotenv

from schemas import Commit, LlmCommitAnalysis, Staged, LlmCommitMsg

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_client_async = AsyncOpenAI(api_key=openai_api_key)
llm_client = OpenAI(api_key=openai_api_key)


async def llm_analyze_commit(commit: Commit) -> LlmCommitAnalysis:

    system_msg = """Your goal is to provide HONEST git commit message reviews. You will be given
a commit message and the diff of files changed in that specific commit.

For scores that you would give a 5/10 or below, include an issue and suggest a new, better commit message. 
Suggestions should follow follow the "Conventional Commits" style, but just because a message doesn't use this style doesn't mean its bad. 
Additionally, you can set vague to "True" if the score is <= 5/10 and you think that the commit message was too vague.

For scores above 5/10, include a short praise message detailing why this was a good commit message."""
    model = "gpt-5-nano"

    user_msg = f"Commit Message: {commit.message}/n/nFiles Diff: {commit.diff}"

    response = await llm_client_async.responses.parse(
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


def llm_create_commit_msg(diff: Staged) -> LlmCommitMsg:

    system_msg = """Your goal is to create a succint, detailed git commit message given a list of staged diffs.

Before you write the commit message, write down up 5 jot note changes that you knotice. Never more than 5, less is better. Keep them very short, under 10 words.

When making the commit message, expand on the "changes" and follow the "Conventional Commits" style.

Example of a strong commit message:
feat(api): add Redis caching layer
    - Implement cache for read endpoints
    - Add TTL configuration
    - Improves response time by 200ms"""
    model = "gpt-5-nano"

    user_msg = f"Staged Diffs: {diff.diffs}"

    response = llm_client.responses.parse(
        model=model,
        instructions=system_msg,
        text_format=LlmCommitMsg,
        input=user_msg,
    )

    return response.output_parsed
