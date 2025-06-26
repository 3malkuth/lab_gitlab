import os
from typing import List, Union
import gitlab


class Issue:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description


def fetch_issues(
        project: Union[int, str],
        labels: List[str],
        gl_token: str,
        gl_url: str,
) -> List[Issue]:
    """
    Connects to GitLab and retrieves all issues for the given project (by ID or path)
    that have all of the specified labels.
    """
    gl = gitlab.Gitlab(gl_url, private_token=gl_token)
    project_obj = gl.projects.get(project)
    issues = project_obj.issues.list(labels=labels, all=True)
    return [Issue(i.title, i.description or "") for i in issues]


def issues_to_markdown(issues: List[Issue]) -> str:
    """
    Renders a list of Issue objects into a Markdown string where each
    issue title is a ### heading and the description is rendered below.
    """
    md_lines: List[str] = []
    for issue in issues:
        md_lines.append(f"### {issue.title}")
        md_lines.append(issue.description)
        md_lines.append("")  # blank line
    return "\n".join(md_lines)


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

    # --- fetch & render ---
    issues = fetch_issues(project, labels, token, url)
    print(issues_to_markdown(issues))
