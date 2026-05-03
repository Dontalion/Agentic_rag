import re
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import tool
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        logger.info("Fetching webpage: %s", url)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        logger.error("Error fetching webpage %s: %s", url, e)
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        logger.error("Unexpected error fetching webpage %s: %s", url, e)
        return f"An unexpected error occurred: {str(e)}"