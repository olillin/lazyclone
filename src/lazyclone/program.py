import os
from .console import debug


def run_program(program: str, cloned_dir: str) -> str | None:
    debug.log("Launching program for cloned_dir:", cloned_dir)
    try:
        os.execvp(program, [program, cloned_dir])
    except FileNotFoundError:
        return f"{program} does not exist"
