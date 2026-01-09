
import unittest
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lazyclone.repository import resolve_repo

class TestRepositoryResolution(unittest.TestCase):
    def test_github_implicit(self):
        # input: "olillin/olillin"
        # Since this resolves via network check or github searching, we expect it to resolve to the full URL.
        # Note: resolve_repo might depend on check_repository_exists which does a real network call.
        result = resolve_repo("olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")

    def test_github_flake_style(self):
        # input: "github:olillin/olillin"
        result = resolve_repo("github:olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")

    def test_direct_url(self):
        # input: "https://github.com/olillin/olillin"
        url = "https://github.com/olillin/olillin"
        result = resolve_repo(url)
        self.assertEqual(result, url)

    def test_git_plus_prefix(self):
        # input: "git+https://github.com/olillin/olillin"
        # Should strip "git+" and return "https://..."
        result = resolve_repo("git+https://github.com/olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")
    
    def test_gitlab_flake(self):
        # input: "gitlab:gitlab-org/gitlab-foss"
        # Assuming this repo exists and check_repository_exists returns True
        result = resolve_repo("gitlab:gitlab-org/gitlab-foss")
        self.assertEqual(result, "https://gitlab.com/gitlab-org/gitlab-foss")

    def test_sourcehut_flake(self):
         # input: "sourcehut:emersion/mrsh"
         result = resolve_repo("sourcehut:emersion/mrsh")
         self.assertEqual(result, "https://git.sr.ht/~emersion/mrsh")

    def test_custom_host(self):
        # input: "gitlab-org/gitlab-foss", host="https://gitlab.com"
        # Since we use check_repository_exists, we need a real repo.
        result = resolve_repo("gitlab-org/gitlab-foss", host="https://gitlab.com")
        self.assertEqual(result, "https://gitlab.com/gitlab-org/gitlab-foss")

    def test_ssh_shorthand(self):
        # input: "@olillin/lazyclone"
        # Should resolve to git@github.com:olillin/lazyclone
        result = resolve_repo("@olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

    def test_custom_host_ssh_shorthand(self):
        # input: "@olillin/lazyclone" with host "https://gitlab.com"
        result = resolve_repo("@olillin/lazyclone", host="https://gitlab.com")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    def test_git_prefixed_ssh_shorthand(self):
        # input: "git@olillin/lazyclone"
        result = resolve_repo("git@olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

    def test_ssh_shorthand_flake_syntax(self):
        # input: "@gitlab:olillin/lazyclone"
        # Should resolve to git@gitlab.com:olillin/lazyclone
        result = resolve_repo("@gitlab:olillin/lazyclone")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    def test_complete_ssh_url(self):
        # input: "olillin@git.olillin.com:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:foo/bar")

    def test_complete_ssh_url_with_port(self):
        # input: "olillin@git.olillin.com:2222:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:2222:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:2222:foo/bar")




if __name__ == "__main__":
    unittest.main()
