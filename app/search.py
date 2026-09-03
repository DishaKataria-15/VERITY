import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables from .env
load_dotenv()

# Get Tavily API key
api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY is missing from .env")

# Create Tavily client
client = TavilyClient(api_key=api_key)


def search_web(query: str, max_results: int = 5):
    """
    Search the web and return relevant sources.
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False
    )

    return response["results"]