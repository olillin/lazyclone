import subprocess
import platform
from .console import *

use_shell = platform.system() == "Windows"


def clone(url: str, output: str | None) -> str:
    return output or url


def github_username() -> str | None:
    """Get the GitHub username of the logged in user using the `gh` CLI. Returns None if it failed"""
    process = subprocess.run(
        ["gh", "api", "https://api.github.com/user", "--jq", ".login"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )

    if process.stdout is None:
        # Unable to get username
        return None
    return process.stdout.decode().strip()


def github_repositories(query: str, owner: str | None) -> list[str]:
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
                "per_page=10",
                "-q",
                ".items[]|.full_name",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=use_shell,
        )
        if user_process.stdout is not None:
            names = get_names(user_process.stdout.decode())
            console.log(f"[blue][DEBUG] User repos {names}")
            repositories.extend(names)

    # Get repositories from all of GitHub
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
            "per_page=10",
            "-q",
            ".items[]|.full_name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell,
    )
    if all_process.stdout is not None:
        names = get_names(all_process.stdout.decode())
        console.log(f"[blue][DEBUG] All repos {names}")
        for name in names:
            if name not in repositories:
                repositories.append(name)

    return repositories
