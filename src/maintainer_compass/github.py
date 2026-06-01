from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass


GITHUB_RE = re.compile(r"^https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+?)(?:\.git)?/?$")


@dataclass(frozen=True)
class GitHubRepository:
    owner: str
    repo: str

    @property
    def api_url(self) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}"

    @property
    def html_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"


def parse_github_url(url: str) -> GitHubRepository:
    match = GITHUB_RE.match(url.strip())
    if not match:
        raise ValueError("Expected a public GitHub URL like https://github.com/owner/repo")
    return GitHubRepository(owner=match.group("owner"), repo=match.group("repo"))


def fetch_github_metadata(url: str, token: str | None = None) -> dict[str, object]:
    repository = parse_github_url(url)
    request = urllib.request.Request(
        repository.api_url,
        headers=_headers(token),
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API returned {exc.code} for {repository.html_url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API for {repository.html_url}") from exc

    return {
        "url": payload.get("html_url", repository.html_url),
        "description": payload.get("description"),
        "stars": payload.get("stargazers_count", 0),
        "forks": payload.get("forks_count", 0),
        "open_issues": payload.get("open_issues_count", 0),
        "default_branch": payload.get("default_branch"),
        "license": (payload.get("license") or {}).get("spdx_id"),
        "updated_at": payload.get("updated_at"),
        "pushed_at": payload.get("pushed_at"),
    }


def token_from_environment() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def _headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "maintainer-compass",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

