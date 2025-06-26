import pytest
from issue_fetcher.fetcher import Issue, issues_to_markdown, fetch_issues


def test_issues_to_markdown_empty() -> None:
    assert issues_to_markdown([]) == ""


def test_issues_to_markdown_single() -> None:
    issue = Issue("Bug found", "- Steps to reproduce\n- Expected vs actual")
    md_lines = issues_to_markdown([issue]).splitlines()
    assert md_lines[0] == "### Bug found"
    assert md_lines[1] == "- Steps to reproduce"
    assert md_lines[2] == "- Expected vs actual"


def test_fetch_issues(monkeypatch) -> None:
    # Prepare dummy data
    class DummyIssueObj:
        def __init__(self, title: str, description: str) -> None:
            self.title = title
            self.description = description

    dummy_issues = [DummyIssueObj("T1", "D1"), DummyIssueObj("T2", "D2")]

    # Mock project.issues.list(...)
    class DummyProject:
        def __init__(self) -> None:
            self.issues = self

        def list(
                self,
                labels,
                order_by,
                sort,
                all
        ):
            # verify parameters
            assert labels == ["a", "b"]
            assert order_by == "updated_at"
            assert sort == "asc"
            assert all is True
            return dummy_issues

    # Mock Gitlab client
    class DummyGitlab:
        def __init__(self, url: str, private_token: str) -> None:
            assert url == "https://example.com"
            assert private_token == "secrettoken"
            self.projects = self

        def get(self, project) -> DummyProject:
            assert project == "group/proj"
            return DummyProject()

    monkeypatch.setattr(
        "issue_fetcher.fetcher.gitlab.Gitlab",
        DummyGitlab
    )

    # Call fetch_issues with our dummy values
    issues = fetch_issues(
        project="group/proj",
        labels=["a", "b"],
        gl_token="secrettoken",
        gl_url="https://example.com",
        order_by="updated_at",
        sort="asc",
    )

    # Verify we got back Issue instances with correct data
    assert isinstance(issues, list)
    assert all(isinstance(i, Issue) for i in issues)
    assert issues[0].title == "T1"
    assert issues[0].description == "D1"
    assert issues[1].title == "T2"
    assert issues[1].description == "D2"
