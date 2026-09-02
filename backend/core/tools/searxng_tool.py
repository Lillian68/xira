from langchain.tools import tool
from langchain_community.utilities import SearxSearchWrapper

from config.config import Config

searx = SearxSearchWrapper(searx_host=Config.SEARXNG_URL)


@tool
def search_study_resources(keyword: str, platform: str) -> str:
    """Search for study resources using SearxNG."""
    all_results = []
    for item in searx.results(query=keyword, num_results=5, engines=[platform]):
        if "title" not in item:
            break
        all_results.append(
            {
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet", ""),
                "platform": platform,
            }
        )

    return all_results
