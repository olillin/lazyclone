import os
from .console import *

def run_program(program: str, cloned_dir: str) -> str | None:
    console.log("[blue][DEBUG]", "cloned_dir:", cloned_dir)
    try:
        os.execvp(program, [program, cloned_dir])
    except FileNotFoundError:
        return f'{program} does not exist'
