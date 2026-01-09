
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lazyclone.repository import resolve_repo

class TestRepositoryResolution(unittest.TestCase):
    @patch("lazyclone.repository.check_repository_exists")
    def test_github_implicit(self, mock_check):
        # input: "olillin/olillin"
        # Since this resolves via network check or github searching, we expect it to resolve to the full URL.
        mock_check.return_value = True
        result = resolve_repo("olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")
        mock_check.assert_called_with("https://github.com/olillin/olillin")

    @patch("lazyclone.repository.check_repository_exists")
    def test_github_flake_style(self, mock_check):
        mock_check.return_value = True
        # input: "github:olillin/olillin"
        result = resolve_repo("github:olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")

    @patch("lazyclone.repository.check_repository_exists")
    def test_direct_url(self, mock_check):
        mock_check.return_value = True
        # input: "https://github.com/olillin/olillin"
        url = "https://github.com/olillin/olillin"
        result = resolve_repo(url)
        self.assertEqual(result, url)

    @patch("lazyclone.repository.check_repository_exists")
    def test_git_plus_prefix(self, mock_check):
        mock_check.return_value = True
        # input: "git+https://github.com/olillin/olillin"
        # Should strip "git+" and return "https://..."
        result = resolve_repo("git+https://github.com/olillin/olillin")
        self.assertEqual(result, "https://github.com/olillin/olillin")
    
    @patch("lazyclone.repository.check_repository_exists")
    def test_gitlab_flake(self, mock_check):
        mock_check.return_value = True
        # input: "gitlab:gitlab-org/gitlab-foss"
        result = resolve_repo("gitlab:gitlab-org/gitlab-foss")
        self.assertEqual(result, "https://gitlab.com/gitlab-org/gitlab-foss")

    @patch("lazyclone.repository.check_repository_exists")
    def test_sourcehut_flake(self, mock_check):
         mock_check.return_value = True
         # input: "sourcehut:emersion/mrsh"
         result = resolve_repo("sourcehut:emersion/mrsh")
         self.assertEqual(result, "https://git.sr.ht/~emersion/mrsh")

    @patch("lazyclone.repository.check_repository_exists")
    def test_custom_host(self, mock_check):
        mock_check.return_value = True
        # input: "gitlab-org/gitlab-foss", host="https://gitlab.com"
        result = resolve_repo("gitlab-org/gitlab-foss", host="https://gitlab.com")
        self.assertEqual(result, "https://gitlab.com/gitlab-org/gitlab-foss")

    @patch("lazyclone.repository.check_repository_exists")
    def test_ssh_shorthand(self, mock_check):
        mock_check.return_value = True
        # input: "@olillin/lazyclone"
        # Should resolve to git@github.com:olillin/lazyclone
        result = resolve_repo("@olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_custom_host_ssh_shorthand(self, mock_check):
        mock_check.return_value = True
        # input: "@olillin/lazyclone" with host "https://gitlab.com"
        result = resolve_repo("@olillin/lazyclone", host="https://gitlab.com")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_git_prefixed_ssh_shorthand(self, mock_check):
        mock_check.return_value = True
        # input: "git@olillin/lazyclone"
        result = resolve_repo("git@olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_ssh_shorthand_flake_syntax(self, mock_check):
        mock_check.return_value = True
        # input: "@gitlab:olillin/lazyclone"
        # Should resolve to git@gitlab.com:olillin/lazyclone
        result = resolve_repo("@gitlab:olillin/lazyclone")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_ssh_url(self, mock_check):
        mock_check.return_value = True
        # input: "olillin@git.olillin.com:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:foo/bar")

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_ssh_url_with_port(self, mock_check):
        mock_check.return_value = True
        # input: "olillin@git.olillin.com:2222:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:2222:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:2222:foo/bar")


if __name__ == "__main__":
    unittest.main()
