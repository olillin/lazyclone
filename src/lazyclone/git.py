import subprocess
import platform
import math
from .console import *

use_shell = platform.system() == "Windows"


def _find_clone_output(stdout: str) -> str:
    """Find the output directory from the stdout of git clone"""
    first_line = stdout[: stdout.index("\n")].strip()
    quote_start = first_line.index("'") + 1
    quote_end = first_line.rindex("'")
    name = first_line[quote_start:quote_end]
    return name


def clone(url: str, output: str | None) -> str:
    """Clone a git repository"""
    args = ["git", "clone", url]
    if output is not None:
        args.append(output)

    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell
    )

    if process.returncode != 0:
        if process.stderr is None:
            raise Exception("Failed to clone git repository")
        else:
            message = process.stderr.decode()
            raise Exception(
                f"Failed to clone git repository: {process.stderr.decode()}"
            )

    output = process.stderr.decode()
    return _find_clone_output(output)


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
        return None
    return process.stdout.decode().strip()


def github_repositories(query: str, owner: str | None, limit: int = 6) -> list[str]:
    repositories: list[str] = []

    def get_names(stdout: str) -> list[str]:
        return [line.strip() for line in stdout.split("\n") if line.strip() != ""]

    if owner is not None:
        # Get repositories owned by the specified owner
        user_process = subprocess.run(
            [
                "gh",
                "api",
                "search/repositories",
                "--method",
                "GET",
                "-f",
                f"q={query} owner:{owner} fork:true",
                "-f",
                "per_page={math.ceil(limit / 2)}",
                "-q",
                ".items[]|.full_name",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=use_shell,
        )
        if user_process.stdout is not None:
            names = get_names(user_process.stdout.decode())
            debug.log(f"User repos {names}")
            repositories.extend(names)

    # Get repositories from all of GitHub
    remaining_limit = limit - len(repositories)
    if remaining_limit <= 0:
        return repositories

    debug.log(f"Searching for {remaining_limit} remaining repositories")
    all_process = subprocess.run(
        [
            "gh",
            "api",
            "search/repositories",
            "--method",
            "GET",
            "-f",
            f"q={query} fork:true",
            "-f",
            "per_page={remaining_limit}",
            "-q",
            ".items[]|.full_name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )
    if all_process.stdout is not None:
        names = get_names(all_process.stdout.decode())[:remaining_limit]
        debug.log(f"All repos {names}")
        for name in names:
            if name not in repositories:
                repositories.append(name)

    return repositories
