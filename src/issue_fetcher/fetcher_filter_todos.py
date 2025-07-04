import os
import re
from typing import List, Union
import gitlab


class Issue:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description


def fetch_issues(
        project: Union[int, str],
        labels: List[str],
        gl_token: str,
        gl_url: str,
        order_by: str = "created_at",
        sort: str = "desc",
) -> List[Issue]:
    """
    Connects to GitLab and retrieves all issues for the given project that
    have all of the specified labels, ordered as requested.

    Args:
        project_id: The GitLab project ID or path.
        labels: A list of label names to filter issues by.
        gl_token: Personal access token with API scope.
        gl_url: Base URL of the GitLab instance (default: gitlab.com).
        order_by: Field to order by (e.g., 'created_at', 'updated_at').
        sort: Sort direction, either 'asc' or 'desc'.

    Returns:
        A list of Issue objects.
    """
    gl = gitlab.Gitlab(gl_url, private_token=gl_token)
    project_obj = gl.projects.get(project)
    issues = project_obj.issues.list(
        labels=labels,
        order_by=order_by,
        all=True,
        sort=sort,
    )
    return [Issue(i.title, i.description or "") for i in issues]


def issues_to_markdown(issues: List[Issue]) -> str:
    """
    Renders a list of Issue objects into a Markdown string where each
    issue title is a ### heading, and only lines starting with '- [ ]'
    or '* [ ]' from the description are included as todo items.
    """
    md_lines: List[str] = []
    for issue in issues:
        # Issue heading
        md_lines.append(f"### {issue.title}")
        # Extract only todo (markdown checkboxes) and heading lines
        todos_and_headings = filter_headings_sections_todos(issue)
        # Add each todo and heading line
        md_lines.extend(todos_and_headings)
        # Blank line after each issue
        md_lines.append("")
    return "\n".join(md_lines)


def filter_headings_sections_todos(issue: Issue) -> List[str]:
    """
    Extracts both unchecked markdown checkbox lines and markdown heading lines
    from an issue description.

    Returns a list of todo and heading strings without leading/trailing whitespace.
    """
    headings_sections_todos: List[str] = []

    # Regex patterns
    todo_pattern = r"^\s*([-*]\s\[ \]\s.*)"  # Unchecked checkbox lines
    heading_pattern = r"^\s*#{1,6}\s.*"  # Matches headings of all levels (1 to 6 '#')
    section_pattern = r"^\s*\*\*.*:\*\*$" # Matches section headings like "**Section:**"


    for line in issue.description.splitlines():
        # Check for unchecked todo checkbox lines
        if re.match(todo_pattern, line):
            headings_sections_todos.append(line.strip())
        # Check for markdown heading lines
        elif re.match(heading_pattern, line):
            headings_sections_todos.append(line.strip())
        elif re.match(section_pattern, line):
            headings_sections_todos.append(line.strip())

    return headings_sections_todos


if __name__ == "__main__":
    # --- read & validate environment variables ---
    token = os.getenv("GITLAB_API_TOKEN")
    if not token:
        raise RuntimeError("Missing environment variable: GITLAB_API_TOKEN")

    url = os.getenv("GITLAB_URL")
    if not url:
        raise RuntimeError("Missing environment variable: GITLAB_URL")

    project = os.getenv("GITLAB_PROJECT_PATH")
    if not project:
        raise RuntimeError("Missing environment variable: GITLAB_PROJECT_PATH")

    labels_env = os.getenv("GITLAB_LABELS", "")
    labels = [lbl.strip() for lbl in labels_env.split(",") if lbl.strip()]

    # Read order_by field (default: created_at)
    order_by = os.getenv("GITLAB_ORDER_BY", "created_at").lower()
    # Optionally enforce allowed values
    valid_order_fields = {"created_at", "updated_at", "title"}
    if order_by not in valid_order_fields:
        raise RuntimeError(
            f"Invalid GITLAB_ORDER_BY value: {order_by!r}, must be one of {', '.join(valid_order_fields)}"
        )

    # New: sort order (asc or desc)
    sort_order = os.getenv("GITLAB_SORT", "desc").lower()
    if sort_order not in ("asc", "desc"):
        raise RuntimeError(f"Invalid GITLAB_SORT value: {sort_order!r}, must be 'asc' or 'desc'")

    # --- fetch & render ---
    issues = fetch_issues(project, labels, token, url, order_by, sort_order)
    print(issues_to_markdown(issues))
