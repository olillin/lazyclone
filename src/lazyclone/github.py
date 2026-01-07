import subprocess
import math
import platform
from .console import *

use_shell = platform.system() == "Windows"


def github_username() -> str | None:
    """Get the GitHub username of the logged in user using the `gh` CLI. Returns None if it failed"""
    process = subprocess.run(
        ["gh", "api", "https://api.github.com/user", "--jq", ".login"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )

    if process.returncode != 0 or process.stdout is None:
        # Unable to get username
        debug.log(f"Failed to get GitHub username")
        if process.stderr:
            debug.log(process.stderr.decode())
        return None
    return process.stdout.decode().strip()


def search_repository_names(query: str, owner: str | None, limit: int) -> list[str]:
    """Search the GitHub API for repositories matching a query"""
    debug.log(f"Searching for repositories with query '{query}' and owner {owner}")

    owner_string = f" owner:{owner}" if owner is not None else ""
    process = subprocess.run(
        [
            "gh",
            "api",
            "search/repositories",
            "--method",
            "GET",
            "-f",
            f"q={query}{owner_string} fork:true",
            "-f",
            "per_page={limit}",
            "-q",
            ".items[]|.full_name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )

    def get_names(stdout: str) -> list[str]:
        return [line.strip() for line in stdout.split("\n") if line.strip() != ""]

    if process.returncode != 0 or process.stdout is None:
        summary = f"Failed to search for GitHub repositories with query: '{query}' and owner '{owner}'"
        if process.stderr is None:
            raise Exception(summary)
        else:
            raise Exception(summary + ": " + process.stdout.decode())

    names = get_names(process.stdout.decode())[:limit]
    debug.log(f"Found repositories: {names}")
    return names


def github_repositories(query: str, owner: str | None, limit: int = 6) -> list[str]:
    repositories: list[str] = []

    if owner is not None:
        # Get repositories owned by the specified owner
        search_limit = math.ceil(limit / 2)
        debug.log(f"Searching for {search_limit} user repositories")
        names = search_repository_names(query, owner, search_limit)
        repositories.extend(names)

    # Get repositories from all of GitHub
    remaining_limit = limit - len(repositories)
    if remaining_limit <= 0:
        return repositories

    debug.log(f"Searching for {remaining_limit} remaining repositories")
    names = search_repository_names(query, None, remaining_limit)
    for name in names:
        if name not in repositories:
            repositories.append(name)

    return repositories


def github_repository_exists(owner: str, repo: str) -> bool:
    debug.log(f"Checking if {owner}/{repo} exists on GitHub")
    process = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{owner}/{repo}",
            "--method",
            "GET",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )
    exists = process.returncode == 0
    debug.log(f"Exists on GitHub ({owner}/{repo}): {exists}")
    return exists
