from git import Repo
from schemas import Commit

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


if __name__ == "__main__":
    repo_path = "./"
    repo = Repo(repo_path)
    commits = get_last_n_commits(10, repo)
    print(commits)
