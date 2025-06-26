import pytest
from issue_fetcher.fetcher import Issue, issues_to_markdown

def test_issues_to_markdown_empty():
    assert issues_to_markdown([]) == ""

def test_issues_to_markdown_single():
    issue = Issue("Bug found", "- Steps to reproduce\n- Expected vs actual")
    md = issues_to_markdown([issue]).splitlines()
    assert md[0] == "### Bug found"
    assert md[1] == "- Steps to reproduce"
    assert md[2] == "- Expected vs actual"
