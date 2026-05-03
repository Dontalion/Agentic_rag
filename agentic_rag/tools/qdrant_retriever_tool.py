from smolagents import Tool
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)


class AdvancedQdrantRetrieverTool(Tool):
    name = "retrieve_knowledge"
    description = """Query the Qdrant vector database for relevant information based on a natural language query.
    Use this tool when you need to find information from the pre-loaded knowledge base stored in Qdrant."""

    inputs = {
        "query": {
            "type": "string",
            "description": "The natural language query to search for relevant information in the vector database.",
        }
    }
    output_type = "string"

    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embeddings: Embeddings,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.collection_name = collection_name
        self.client = qdrant_client
        self.embeddings = embeddings

    def forward(self, query: str) -> str:
        logger.info("Qdrant retrieval query: '%s'", query)

        # Generate embedding for query
        query_vector = self.embeddings.embed_query(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=5,
            score_threshold=0.7,
            with_payload=True,
        )

        # Extract and format the relevant information from search results
        if not results:
            return f"No relevant information found for query: '{query}'"

        formatted = []
        for i, hit in enumerate(results, 1):
            text = hit.payload.get("text", hit.payload.get("content", "No content"))
            score = hit.score
            formatted.append(f"[{i}] (score: {score:.2f}) -> {text[:300]}...")

        return "\nRetrieved documents:\n" + "\n".join(formatted)
