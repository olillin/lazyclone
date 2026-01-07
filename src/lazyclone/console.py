from rich.console import Console

console = Console()

debug = Console(style="blue")
def set_debug(enabled: bool):
    debug.quiet = not enabled

errors = Console(stderr=True, style="bold red")
