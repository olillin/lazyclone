import re
import inquirer as inq
from .console import console, debug
from .git import clone as git_clone, check_repository_exists
from .github import github_username, github_repositories

# Prefixes from Nix Flakes URL-like syntax
# See: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html#flake-references
FLAKE_PREFIXES = {
    "github": "https://github.com/",
    "gitlab": "https://gitlab.com/",
    "sourcehut": "https://git.sr.ht/~",
}
FLAKE_GIT_PREFIX = "git+"


def choose_repository(choices: list[str]) -> str:
    if len(choices) == 0:
        raise Exception("No repositories to choose from")
    elif len(choices) == 1:
        return choices[0]

    question = inq.List("repo", message="Select repository to clone", choices=choices)
    answers = inq.prompt([question])
    if answers is None:
        raise KeyboardInterrupt

    return answers["repo"]


def find_repo_choices(repo: str, owner: str | None = None) -> list[str]:
    if owner is None:
        owner = github_username()
    debug.log(f"Searching for repos with owner: {owner}")
    return github_repositories(repo, owner)


def build_url(
    path: str, host: str, ssh: bool = False, ssh_prefix: str | None = None
) -> str:
    """Build a URL from a path and a host"""
    if "://" not in host:
        raise Exception("Host must be a valid URL")

    if ssh:
        domain = host.split("://")[-1].rstrip("/")
        if ssh_prefix is None:
            ssh_prefix = "git"
        return f"{ssh_prefix}@{domain}:{path}"
    else:
        # If host already ends with a separator, don't add another one
        separator = "" if host[-1] in ["/", "~"] else "/"
        return host + separator + path.lstrip("/")


def resolve_repo(
    repo: str, host: str = "https://github.com", default_ssh: bool = False
) -> str:
    if "://" not in host:
        raise Exception("Host must be a valid URL")
    host = host.rstrip("/").strip()
    repo = repo.strip()

    # Strip ssh:// protocol
    ssh_prefix: str | None = None
    if repo.startswith("ssh://"):
        ssh_prefix = "ssh://"
        repo = repo[len("ssh://") :]
    if user_match := re.match("[a-zA-Z0-9]+(?=@)", repo):
        user = user_match.group(0)
        if ssh_prefix:
            ssh_prefix += user
        else:
            ssh_prefix = user
        repo = repo[len(user) :]

    # Don't resolve already completed URLs
    elif re.match(f"^({FLAKE_GIT_PREFIX.replace('+', '\\+')})?https?://", repo):
        if repo.startswith(FLAKE_GIT_PREFIX):
            return repo[len(FLAKE_GIT_PREFIX) :]
        return repo

    # Resolve SSH prefix
    use_ssh: bool
    if repo.startswith("@") or repo.startswith("git@") or repo.startswith("ssh://"):
        use_ssh = True
        repo = repo.split("@", maxsplit=1)[1]

        # Remove protocol if present
        if "://" in repo:
            repo = repo.split("://", maxsplit=1)[1]
    else:
        use_ssh = default_ssh

    # Try to add GitHub username if no owner is specified
    if "/" not in repo:
        username = github_username()
        if username is not None:
            repo = username + "/" + repo

    # Resolve Nix Flake-like URLs
    if ":" in repo:
        for key, flake_host in FLAKE_PREFIXES.items():
            if not repo.startswith(key + ":"):
                continue
            path = repo[len(key) + 1 :]
            url = build_url(path, host=flake_host, ssh=use_ssh)
            if not check_repository_exists(url):
                # If flake resolution fails, strip prefix and try regular resolution/search
                repo = path
                break
            return url

    # Try to build URL if domain is provided
    if "." in repo and "/" in repo:
        colon = re.search(":(?!\\d)", repo)
        if colon:
            domain, path = repo[: colon.start()], repo[colon.start() + 1 :]
        else:
            domain, path = repo.split("/", maxsplit=1)
        url = build_url(
            path, host="https://" + domain, ssh=use_ssh, ssh_prefix=ssh_prefix
        )
        if check_repository_exists(url):
            return url

    # Try default host with owner and name
    if re.match("[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$", repo):
        url = build_url(repo, host=host, ssh=use_ssh, ssh_prefix=ssh_prefix)
        if check_repository_exists(url):
            return url

    # Use GitHub search as fallback
    owner: str | None
    if "/" in repo:
        owner, repo = repo.split("/", maxsplit=1)
    else:
        owner = None

    choices: list[str] = find_repo_choices(repo, owner)

    debug.log(f"Choosing between: {choices}")
    chosen_repository = choose_repository(choices)
    debug.log(f"Chosen repository: {chosen_repository}")
    github_host = "https://github.com"
    return build_url(
        chosen_repository, host=github_host, ssh=use_ssh, ssh_prefix=ssh_prefix
    )


def get_repo_name(url: str) -> str:
    match = re.search(r"(?<=\/)[^\/]+?(?=(\.git)?$)", url)
    if match is None:
        raise Exception(f"Invalid repository url: {url}")
    return match.group(0)


def lazy_clone(
    repo: str,
    directory: str | None,
    host: str = "https://github.com",
    default_ssh: bool = False,
) -> str:
    url = resolve_repo(repo, host, default_ssh)
    debug.log(f"Resolved URL to {url}")
    console.print(f"Cloning [yellow]{url}")
    output = git_clone(url, directory)
    return output
