import os
import shutil
import tempfile
from git import Repo
from schemas import Commit, Staged


from typing import List


def get_last_n_commits(n: int, repo: Repo) -> List[Commit]:
    commit_data: List[Commit] = []

    commits = list(repo.iter_commits("HEAD", max_count=n))

    for commit in commits:
        msg = commit.message

        parent = commit.parents[0] if commit.parents else None
        diffs = commit.diff(parent, create_patch=True)

        diff_str = ""
        for diff in diffs:
            diff_str += diff.diff.decode("utf-8")

        commit_data.append(Commit(message=msg, diff=diff_str))

    return commit_data


def get_last_n_commits_remote(n: int, url: str) -> List[Commit]:
    temp_path = tempfile.mkdtemp()

    try:
        repo = Repo.clone_from(url, temp_path)
        commits = get_last_n_commits(n, repo)

        return commits

    finally:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)


def get_staged_diffs(repo: Repo) -> Staged:
    staged_changes = repo.index.diff(repo.head.commit, create_patch=True)

    diff_str = ""
    for diff in staged_changes:
        diff_str += diff.diff.decode("utf-8")

    diff = Staged(diffs=diff_str)

    return diff


def make_commit(repo: Repo, message: str) -> None:
    repo.index.commit(message)
