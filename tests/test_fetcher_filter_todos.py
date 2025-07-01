import pytest
from issue_fetcher.fetcher_filter_todos import Issue, issues_to_markdown, fetch_issues, filter_todos


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


def test_filter_todos_only_unchecked() -> None:
    # filter_todos should return only unchecked checkbox lines
    description = '''
        Line before
        - [ ] unchecked task
        * [ ] another unchecked
        - [x] checked task
        * [x] another checked
        No list here
    '''
    issue = Issue("Test", description)
    todos = filter_todos(issue)
    assert todos == [
        "- [ ] unchecked task",
        "* [ ] another unchecked",
    ]



def test_fetch_issues(monkeypatch) -> None:
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
                labels,
                order_by,
                sort,
                all
        ):
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
