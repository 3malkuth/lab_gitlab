import pytest
from pytest import MonkeyPatch
from typing import List
from issue_fetcher.fetcher_filter_todos import Issue, issues_to_markdown, fetch_issues, filter_headings_sections_todos

def test_issues_to_markdown_empty() -> None:
    # No issues should produce an empty string
    assert issues_to_markdown([]) == ""


def test_issues_to_markdown_single() -> None:
    # Description contains various checkbox lines; only unchecked markers should be included
    description = '''
        - [ ] first task
        * [ ] second task
        - [x] done task
        Regular line
    '''
    issue = Issue("Task list", description)
    # splitlines() retains lines without trailing line break markers
    md_lines = issues_to_markdown([issue]).splitlines()
    assert md_lines == [
        "### Task list",
        "- [ ] first task",
        "* [ ] second task",
    ]

def test_filter_headings_sections_todos() -> None:
    # filter_todos_and_headings should return both unchecked checkbox lines and headings
    description = '''
        # Main Heading
        - [ ] unchecked task
        * [ ] another unchecked
        ## Subheading
        **Section:**
        - [x] checked task
        * [x] another checked
        # Another Heading
    '''
    issue = Issue("Test", description)
    headings_sections_todos = filter_headings_sections_todos(issue)
    assert headings_sections_todos == [
        "# Main Heading",
        "- [ ] unchecked task",
        "* [ ] another unchecked",
        "## Subheading",
        '**Section:**',
        "# Another Heading"
    ]


def test_fetch_issues(monkeypatch: MonkeyPatch) -> None:
    # Prepare dummy GitLab issue objects
    class DummyIssueObj:
        def __init__(self, title: str, description: str) -> None:
            self.title = title
            self.description = description

    dummy_issues = [DummyIssueObj("T1", "Desc1"), DummyIssueObj("T2", "Desc2")]

    # Mock project.issues.list(...) to assert parameters
    class DummyProject:
        def __init__(self) -> None:
            self.issues = self

        def list(
                self,
                labels: List[str],
                order_by: str,
                sort: str,
                all: bool
        ) -> List[DummyIssueObj]:
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

        def get(self, project: str) -> DummyProject:
            assert project == "group/proj"
            return DummyProject()

    # Patch the Gitlab client in our module
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

    # Verify output
    assert len(issues) == 2
    assert all(isinstance(i, Issue) for i in issues)
    assert issues[0].title == "T1"
    assert issues[0].description == "Desc1"
    assert issues[1].title == "T2"
    assert issues[1].description == "Desc2"
