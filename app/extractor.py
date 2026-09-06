from bs4 import BeautifulSoup
import requests


def extract_text(url: str) -> str:
    """
    Fetch a webpage and extract readable text.
    Returns an empty string if the page cannot be accessed.
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            element.decompose()

        return soup.get_text(separator=" ", strip=True)

    except requests.RequestException:
        return ""