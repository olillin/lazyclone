import re
import platform
import inquirer as inq
from .console import *
from .git import github_username, github_repositories, clone as git_clone


def choose_repository(choices: list[str]) -> str:
    if len(choices) == 0:
        raise Exception("No repositories to choose from")

    question = inq.List("repo", message="Select repository to clone", choices=choices)
    answers = inq.prompt([question])
    if answers is None:
        raise KeyboardInterrupt

    return answers["repo"]


def find_repo_choices(repo: str) -> list[str]:
    username = github_username()
    console.log(f"[blue][DEBUG] GitHub username: {username}")
    return github_repositories(repo, username)


def resolve_repo(repo: str) -> str:
    choices: list[str] = find_repo_choices(repo)

    console.log(f"[blue][DEBUG] Choosing between: {choices}")
    return "https://github.com/" + choose_repository(choices)

    # Resolve repository name only
    if re.match("^[a-zA-Z0-9._-]+$", repo):
        username = github_username()
        if username is None:
            raise Exception("Failed to get GitHub username")

        url = "https://github.com/" + username + "/" + repo
        return url

    # Resolve repository owner and name
    if re.match("^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$", repo):
        url = "https://github.com/" + repo
        return url

    raise Exception("Unable to resolve repository")


def get_repo_name(url: str) -> str:
    match = re.search(r"(?<=\/)[^\/]+?(?=(\.git)?$)", url)
    if match is None:
        raise Exception(f"Invalid repository url: {url}")
    return match.group(0)


def lazy_clone(repo: str, directory: str | None) -> str:
    url = resolve_repo(repo)
    console.log(f"[blue][DEBUG] Resolved URL to {url}")
    console.print(f"Cloning [yellow]{url}")
    output = git_clone(url, directory)
    return output
