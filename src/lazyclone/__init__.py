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
    parser.add_argument(
        "--host",
        help="URL for default git host (default: https://github.com)",
        default="https://github.com",
    )
    parser.add_argument(
        "--ssh",
        action="store_true",
        help="prefer ssh over https",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debugging output",
    )

    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_arguments()
    repo = args.repo
    directory = args.directory
    program = args.program
    host = args.host
    ssh = args.ssh

    # Enable debugging
    enable_debug = args.debug
    set_debug(enable_debug)

    debug.log("Args:: Repo:", repo, "Output directory:", directory, "Program:", program, "Host:", host, "SSH: ", ssh)

    try:
        cloned_dir = lazy_clone(repo, directory, host, default_ssh=ssh)

    except KeyboardInterrupt as e:
        console.print(f"[red]Cancelled")
        sys.exit(0)
    except Exception as e:
        errors.print(e)
        sys.exit(1)

    if cloned_dir is None:
        return

    console.print(f"[green]Successfully cloned into '{cloned_dir}'")
    if program is not None:
        console.print(f"[plum1]Launching {program}...")
        error = run_program(program, cloned_dir)
        if error is not None:
            errors.print(f"Failed to launch program: {program} does not exist")
            sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"[red]Cancelled")
