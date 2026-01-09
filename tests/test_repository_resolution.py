
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

if __name__ == "__main__":
    unittest.main()
