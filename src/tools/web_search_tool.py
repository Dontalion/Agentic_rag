"""
Web Search Tool for smolagents.
Performs web searches using DuckDuckGo.
"""
from smolagents import Tool
from duckduckgo_search import DDGS


class WebSearchTool(Tool):
    name = "web_search"
    description = """
    Performs a web search using DuckDuckGo and returns relevant results.
    Use this tool when you need to find current information from the internet,
    news, facts, or any topic that may not be in the local knowledge base.
    Returns search results with titles, snippets, and URLs.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to look up on the web. Be specific and descriptive for better results.",
        },
        "max_results": {
            "type": "integer",
            "description": "Maximum number of search results to return. Default is 5.",
        },
    }
    output_type = "string"

    def forward(self, query: str, max_results: int = 5) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return f"No web search results found for query: '{query}'"

            formatted_results = []
            for i, r in enumerate(results):
                title = r.get("title", "No title")
                snippet = r.get("body", "No snippet")
                url = r.get("href", "No URL")
                formatted_results.append(
                    f"===== Result {i + 1} =====\n"
                    f"Title: {title}\n"
                    f"URL: {url}\n"
                    f"Snippet: {snippet}\n"
                )

            return f"Web Search Results for '{query}':\n\n" + "\n".join(formatted_results)

        except Exception as e:
            return f"Error performing web search for '{query}': {type(e).__name__}: {str(e)}"
