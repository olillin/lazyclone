import argparse
import sys
from .repository import *
from .console import *
from .program import *


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="lazyclone",
        description="Clone Git repositories easier",
    )
    parser.add_argument("repo", type=str, help="url or name of repository to clone")
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        help="the name of a new directory to clone into",
    )

    # Flags
    parser.add_argument(
        "-p",
        "--program",
        help="open with this program after cloning",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    repo = args.repo
    directory = args.directory
    program = args.program
    console.log("[blue][DEBUG]", repo, directory, program)

    cloned_dir = lazy_clone(repo, directory)
    if cloned_dir is None:
        return

    console.print(f"[green]Successfully cloned {cloned_dir}")
    if program is not None:
        console.print(f"[plum1]Launching {program}...")
        error = run_program(program, cloned_dir)
        if error is not None:
            errors.print(f"Failed to launch program: {program} does not exist")
            sys.exit(2)


if __name__ == "__main__":
    main()
