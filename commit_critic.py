from llm import llm_analyze_commits, llm_create_commit_msg
from commits import get_last_n_commits_remote, get_staged_diffs, make_commit
from schemas import LlmCommitAnalysis, LlmCommitMsg

from git import Repo

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


def display_suggested_commit(suggestion: LlmCommitMsg, repo: Repo) -> None:

    print("\nAnalyzing staged changes...")
    # print(f"({files_changed} files changed, +{additions} -{deletions} lines)\n")

    print("\nChanges detected:")
    for change in suggestion.changes:
        print(f"-{change}")

    print("\nSuggested commit message:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(suggestion.message)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    user_input = input("Press Enter to accept, or type your own message: ")

    if user_input.strip():
        commit_message = user_input
    else:
        commit_message = suggestion.message

    make_commit(repo, commit_message)
    print("\n✅ Committed successfully!")


async def main():
    # repo_url = "https://github.com/MichaelMoriarty67/mcp-autogen.git"
    repo_path = "./"
    repo = Repo(repo_path)

    # commits = get_last_n_commits_remote(1, repo_url)
    # llm_commits_analysis = await llm_analyze_commits(commits)

    diffs = get_staged_diffs(repo)
    llm_suggestion = llm_create_commit_msg(diffs)

    # display_commit_analysis(llm_commits_analysis)
    display_suggested_commit(llm_suggestion, repo)


if __name__ == "__main__":
    asyncio.run(main())
