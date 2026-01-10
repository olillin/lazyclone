import unittest
from unittest.mock import patch
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lazyclone.repository import resolve_repo


class TestRepositoryResolution(unittest.TestCase):
    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_url(self, mock_check):
        mock_check.return_value = True
        # input: "https://github.com/olillin/olillin"
        url = "https://github.com/olillin/olillin"
        result = resolve_repo(url)
        self.assertEqual(result, url)

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_url_ssh(self, mock_check):
        mock_check.return_value = True
        # input: "git@github.com:olillin/olillin"
        url = "git@github.com:olillin/olillin"
        result = resolve_repo(url)
        self.assertEqual(result, url)

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_url_ssh_protocol(self, mock_check):
        mock_check.return_value = True
        # input: "ssh://git@github.com:olillin/olillin"
        url = "ssh://git@github.com:olillin/olillin"
        result = resolve_repo(url)
        self.assertEqual(result, url)

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_url_ssh_custom_user(self, mock_check):
        mock_check.return_value = True
        # input: "olillin@git.olillin.com:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:foo/bar")

    @patch("lazyclone.repository.check_repository_exists")
    def test_complete_url_ssh_with_port(self, mock_check):
        mock_check.return_value = True
        # input: "olillin@git.olillin.com:2222:foo/bar"
        result = resolve_repo("olillin@git.olillin.com:2222:foo/bar")
        self.assertEqual(result, "olillin@git.olillin.com:2222:foo/bar")

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
    def test_ssh_shorthand_with_domain(self, mock_check):
        mock_check.return_value = True
        # input: "@gitlab.com:olillin/lazyclone"
        # Should resolve to git@gitlab.com:olillin/lazyclone
        result = resolve_repo("@gitlab.com:olillin/lazyclone")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_ssh_shorthand_with_domain_slash(self, mock_check):
        mock_check.return_value = True
        # input: "@gitlab.com/olillin/lazyclone"
        # Should resolve to git@gitlab.com:olillin/lazyclone
        result = resolve_repo("@gitlab.com/olillin/lazyclone")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_ssh_shorthand_translate_https(self, mock_check):
        mock_check.return_value = True
        # input: "@https://github.com/olillin/lazyclone"
        # Should resolve to git@github.com:olillin/lazyclone
        result = resolve_repo("@https://github.com/olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

    @patch("lazyclone.repository.check_repository_exists")
    def test_custom_host_ssh_shorthand(self, mock_check):
        mock_check.return_value = True
        # input: "@olillin/lazyclone" with host "https://gitlab.com"
        result = resolve_repo("@olillin/lazyclone", host="https://gitlab.com")
        self.assertEqual(result, "git@gitlab.com:olillin/lazyclone")

    @patch("lazyclone.github.github_username")
    @patch("lazyclone.repository.find_repo_choices")
    @patch("lazyclone.repository.choose_repository")
    def test_ssh_shorthand_search(self, mock_choose, mock_find, mock_username):
        mock_find.return_value = ["olillin/lazyclone"]
        mock_choose.return_value = "olillin/lazyclone"
        mock_username.return_value = None
        # input: "@lazyclone"
        # Should resolve to git@github.com:olillin/lazyclone
        result = resolve_repo("@olillin/lazyclone")
        self.assertEqual(result, "git@github.com:olillin/lazyclone")

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
    @patch("lazyclone.repository.find_repo_choices")
    @patch("lazyclone.repository.choose_repository")
    def test_nonexistent_fallback_search(self, mock_choose, mock_find, mock_check):
        # Case: my/repo does not exist
        mock_check.return_value = False
        mock_find.return_value = ["suggested/repo"]
        mock_choose.return_value = "suggested/repo"

        result = resolve_repo("my/repo")

        # Should have checked existence
        mock_check.assert_called()
        # Should have searched
        mock_find.assert_called()
        # Should return the chosen one from search (defaulting to GitHub)
        self.assertEqual(result, "https://github.com/suggested/repo")

    @patch("lazyclone.repository.check_repository_exists")
    @patch("lazyclone.repository.find_repo_choices")
    @patch("lazyclone.repository.choose_repository")
    def test_nonexistent_flake_fallback(self, mock_choose, mock_find, mock_check):
        # Case: github:owner/repo does not exist
        mock_check.return_value = False
        mock_find.return_value = ["found/repo"]
        mock_choose.return_value = "found/repo"

        result = resolve_repo("github:owner/repo")

        # It should fall through to search
        self.assertEqual(result, "https://github.com/found/repo")
        # Check what it searched for - prefix should be stripped!
        mock_find.assert_called_with("repo", "owner")


if __name__ == "__main__":
    unittest.main()
