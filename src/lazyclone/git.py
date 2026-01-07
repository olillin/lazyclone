import subprocess
import platform
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


def check_repository_exists(url: str) -> bool:
    """Check if a git remote exists"""
    debug.log(f"Checking if {url} exists")

    args = ["git", "ls-remote", "-q", "--exit-code", url]
    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell
    )
    exists = process.returncode == 0
    debug.log(f"Repo exists ({url}): {exists}")
    return exists
