from __future__ import annotations

import unittest

from maintainer_compass.github import parse_github_url


class GitHubUrlTests(unittest.TestCase):
    def test_parses_repository_url(self) -> None:
        repository = parse_github_url("https://github.com/panda4556/maintainer-compass")

        self.assertEqual(repository.owner, "panda4556")
        self.assertEqual(repository.repo, "maintainer-compass")
        self.assertEqual(repository.api_url, "https://api.github.com/repos/panda4556/maintainer-compass")

    def test_parses_git_suffix(self) -> None:
        repository = parse_github_url("https://github.com/panda4556/maintainer-compass.git")

        self.assertEqual(repository.repo, "maintainer-compass")

    def test_rejects_non_github_url(self) -> None:
        with self.assertRaises(ValueError):
            parse_github_url("https://example.com/panda4556/maintainer-compass")


if __name__ == "__main__":
    unittest.main()
