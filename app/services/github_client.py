import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class GithubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
    
        headers = {
            "Accept":
            "application/vnd.github.v3+json",
            "User-Agent": "MCP-Community-Assistant",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers=headers,
            timeout=10.0,
            follow_redirects=True
        )
    
    def get(self, endpoint: str, params: dict = None):
        """Helper method to make GET requests to GitHub."""
        response = self.client.get(endpoint, params=params)

        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, json: dict = None):
        """Helper method to make POST requests to Github."""
        response = self.client.post(endpoint, json=json)
        response.raise_for_status()
        return response.json()

github_client = GithubClient()
