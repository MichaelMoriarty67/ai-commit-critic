from git import Repo
from schemas import Commit

from typing import List


def get_last_n_commits(n: int, repo: Repo) -> List[Commit]:
    commits: List[Commit] = []

    commits = list(repo.iter_commits("HEAD", max_count=n))

    for commit in commits:
        msg = commit.message
        diff = commit.diff(commit.parents[0], creat_patch=True)
        print(diff)


if __name__ == "__main__":
    repo_path = "./"
    repo = Repo(repo_path)
    get_last_n_commits(10, repo)
