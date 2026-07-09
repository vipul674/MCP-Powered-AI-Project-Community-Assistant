from langchain_core.tools import tool
from app.services.github_client import github_client
import base64
import os

def search_repositories(query: str, limit: int = 5) -> list[dict]:
    """Search for Github repositories using a text query."""

    data = github_client.get("/search/repositories", params={"q": query, "per_page": limit})

    results = []
    for item in data.get("items", []):
        results.append({
            "name": item["full_name"],
            "description": item["description"],
            "url": item["html_url"],
            "stars": item["stargazers_count"]
        })
    return results

def get_repository_readme(owner: str, repo: str) -> str:
    """Fetch the decoded readme content of a repository."""
    try:
        data = github_client.get(f"/repos/{owner}/{repo}/readme")
        content_b64 = data.get("content", "")
        if not content_b64:
            return "README has no content."
        return base64.b64decode(content_b64).decode("utf-8")
    except Exception as e:
        return f"Could not fetch README: {e}"

def get_repository_metadata(owner: str, repo: str) -> dict:
    """Fetch basic metadata about a repository"""
    try:
        data = github_client.get(f"/repos/{owner}/{repo}")
        return {
            "name": data.get("full_name"),
            "description": data.get("description"),
            "language": data.get("language"),
            "open_issues": data.get("open_issues_count"),
            "topics": data.get("topics", [])
        }
    except Exception as e:
        return {
            "error": f"Could not fetch repository metadata: {e}",
            "name": f"{owner}/{repo}"
        }

@tool
def create_github_issue(repo: str, title: str, body: str, labels: list[str] = None) -> str:
    """
    Creates a new issue in a Github repository.
    If DRY_RUN is enabled, it simulates the creation safely.
    """
    is_dry_run = os.getenv("DRY_RUN", "True").lower() == "true"

    if is_dry_run:
        return f"✅ [DRY-RUN MODE] Issue preview verified. In production, issues '{title}' would be created in '{repo}' with labels {labels}."

    endpoint = f"/repos/{repo}/issues"
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels

    try:
        response = github_client.post(endpoint, json=payload)
        issue_url = response.get("html_url", "Unknown URL")
        return f"✅ Issue successfully created: {issue_url}"
    except Exception as e:
        return f"❌ Error creating issue: {e}"
    