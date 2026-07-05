from mcp.server.fastmcp import FastMCP
from app.tools.github_tools import search_repositories, get_repository_readme, get_repository_metadata

mcp = FastMCP("Community Assistant Github Tools")

@mcp.tool()
def search_github(query: str, limit: int = 5) -> list[dict]:
    """Search for Github repositories using a text query."""
    return search_repositories(query, limit)

@mcp.tool()
def get_readme(owner: str, repo: str) -> str:
    """Fetch the decoded README content of a specific Github repository."""
    return get_repository_readme(owner, repo)

@mcp.tool()
def get_metadata(owner: str, repo: str) -> dict:
    """Fetch the basic metadata about a Github repository (stars, issues, language)"""
    return get_repository_metadata(owner, repo)

if __name__ == "__main__":
    mcp.run()