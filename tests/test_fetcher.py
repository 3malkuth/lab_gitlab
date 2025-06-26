import pytest
import pytest
from issue_fetcher.fetcher import Issue, issues_to_markdown

def test_issues_to_markdown_empty() -> None:
    assert issues_to_markdown([]) == ""

def test_issues_to_markdown_single() -> None:
    issue = Issue("Bug found", "- Steps to reproduce\n- Expected vs actual")
    md_lines = issues_to_markdown([issue]).splitlines()
    assert md_lines[0] == "### Bug found"
    assert md_lines[1] == "- Steps to reproduce"
    assert md_lines[2] == "- Expected vs actual"
