from llm import llm_analyze_commits
from commits import get_last_n_commits_remote
from schemas import LlmCommitAnalysis

from typing import List

import asyncio


def display_commit_analysis(analyses: List[LlmCommitAnalysis]) -> None:
    bad_commits = [a for a in analyses if a.score < 6]
    good_commits = [a for a in analyses if a.score >= 6]

    total = len(analyses)
    avg_score = sum(a.score for a in analyses) / total if total else 0
    vague_commits = sum(1 for a in analyses if a.vague)
    one_word_commits = sum(1 for a in analyses if len(a.message.split()) <= 1)

    if bad_commits:
        print(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 💩 COMMITS THAT NEED WORK ━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        for analysis in bad_commits:
            print(f'Commit: "{analysis.message}"')
            print(f"Score: {analysis.score}/10")
            if analysis.issue:
                print(f"Issue: {analysis.issue}")
            if analysis.suggestion:
                print(f"Better: {analysis.suggestion}")
            print()

    if good_commits:
        print(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 💎 WELL-WRITTEN COMMITS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        for analysis in good_commits:
            print(f'Commit: "{analysis.message}"')
            print(f"Score: {analysis.score}/10")
            if analysis.praise:
                print(f"Why it's good: {analysis.praise}")
            print()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 📊 YOUR STATS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Average score: {avg_score:.1f}/10")
    print(f"Vague commits: {vague_commits} ({vague_commits/total*100:.0f}%)")
    print(f"One-word commits: {one_word_commits} ({one_word_commits/total*100:.0f}%)")
    print()


async def main():
    repo_url = "https://github.com/MichaelMoriarty67/mcp-autogen.git"
    commits = get_last_n_commits_remote(1, repo_url)
    llm_commits_analysis = await llm_analyze_commits(commits)

    display_commit_analysis(llm_commits_analysis)


if __name__ == "__main__":
    asyncio.run(main())
