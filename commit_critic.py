import sys
import asyncio
from typing import List

from git import Repo

from llm import llm_analyze_commits, llm_create_commit_msg
from commits import (
    get_last_n_commits_remote,
    get_staged_diffs,
    make_commit,
    get_last_n_commits,
)
from schemas import LlmCommitAnalysis, LlmCommitMsg

DEFAULT_PATH = "./"  # Path defaults to root of wherever interpreter is run
DEFAULT_REPO = Repo(DEFAULT_PATH)
DEFAULT_COMMITS = 3  # Dear Steele Browser team, saving tokens, 50 reqs is a lot 🥲


async def run_cmd_line():
    args = sys.argv[1:]

    has_analyze = "--analyze" in args
    has_write = "--write" in args

    if not has_analyze and not has_write:
        print("Error: Must provide --analyze or --write")
        sys.exit(1)

    if has_analyze and has_write:
        print("Error: Cannot use both --analyze and --write")
        sys.exit(1)

    url = None
    for arg in args:
        if arg.startswith("--url="):
            url = arg.split("=", 1)[1]
            break

    n = None
    for arg in args:
        if arg.startswith("--n="):
            try:
                n = int(arg.split("=", 1)[1])
                if n < 1:
                    raise ValueError
            except:
                print("Error: --n= must provide an integer greater than zero.")
            break

    if url and has_write:
        print("Error: --url can only be used with --analyze")
        sys.exit(1)

    if has_analyze:
        num_commits = n if n else DEFAULT_COMMITS

        print(f"Analyzing last {n} commits...")
        if url:
            commits = get_last_n_commits_remote(num_commits, url)
            llm_commits_analysis = await llm_analyze_commits(commits)

            display_commit_analysis(llm_commits_analysis)
        else:
            commits = get_last_n_commits(DEFAULT_COMMITS, DEFAULT_REPO)
            llm_commits_analysis = await llm_analyze_commits(commits)

            display_commit_analysis(llm_commits_analysis)
    elif has_write:
        diffs = get_staged_diffs(DEFAULT_REPO)
        llm_suggestion = llm_create_commit_msg(diffs)

        display_suggested_commit(llm_suggestion, DEFAULT_REPO)


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


if __name__ == "__main__":
    asyncio.run(run_cmd_line())
