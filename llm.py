import os
import asyncio
from typing import List

from openai import OpenAI
from dotenv import load_dotenv

from schemas import Commit, LlmCommitAnalysis

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_client = OpenAI(api_key=openai_api_key)


async def llm_analyze_commit(commit: Commit) -> LlmCommitAnalysis:

    dev_msg = ""
    model = "gpt-5-nano"

    response = await llm_client.responses.parse(
        model=model, instructions=dev_msg, text_format=LlmCommitAnalysis
    )

    return response.output_parsed


async def llm_analyze_commits(commits: List[Commit]) -> List[LlmCommitAnalysis]:
    analysis_tasks = [llm_analyze_commit(commit) for commit in commits]
    analysis_results = await asyncio.gather(*analysis_tasks)

    return analysis_results
