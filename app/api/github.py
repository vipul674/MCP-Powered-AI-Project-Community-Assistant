from fastapi import APIRouter
from app.tools.github_tools import search_repositories, get_repository_readme, get_repository_metadata

router = APIRouter(prefix="/api/github", tags=["github"])

@router.get("/search")
def api_search_repositories(query: str, limit: int = 5):
    return search_repositories(query, limit)

@router.get("/repo/{owner}/{repo}")
def api_get_repository(owner: str, repo: str):
    metadata = get_repository_metadata(owner, repo)
    readme = get_repository_readme(owner, repo)
    return {
        "metadata": metadata,
        "readme_preview": readme[:500] + "..." if readme else None
    }