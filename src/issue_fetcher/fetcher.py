from typing import List
import gitlab

class Issue:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

def fetch_issues(
        project_id: int,
        labels: List[str],
        gl_token: str,
        gl_url: str = "https://gitlab.com"
) -> List[Issue]:
    """
    Connects to GitLab and retrieves all issues for the given project that
    have all of the specified labels.
    """
    gl = gitlab.Gitlab(gl_url, private_token=gl_token)
    project = gl.projects.get(project_id)
    issues = project.issues.list(labels=labels, all=True)
    return [Issue(i.title, i.description or "") for i in issues]

def issues_to_markdown(issues: List[Issue]) -> str:
    """
    Renders a list of Issue objects into a Markdown string where each
    issue title is a ### heading and the description is rendered below.
    """
    md = []
    for issue in issues:
        md.append(f"### {issue.title}")
        md.append(issue.description)
        md.append("")  # blank line
    return "\n".join(md)
