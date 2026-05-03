from smolagents import Tool
from langchain_core.vectorstores import VectorStore
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class RetrieverTool(Tool):
    name = "rag_retriever"
    description = """Retrieves relevant documents from the knowledge base using semantic similarity (RAG).
    Use this tool when you need to find information from the pre-loaded knowledge base.
    The tool returns documents that have the closest embeddings to the input query.
    Provide your query in affirmative form rather than a question."""
    inputs = {
        "query": {
            "type": "string",
            "description": """The query to perform. This should be semantically close to your target documents.
            Use the affirmative form rather than a question.""",
        }
    }
    output_type = "string"

    def __init__(self, vectordb: VectorStore, **kwargs):
        super().__init__(**kwargs)
        self.vectordb = vectordb

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        logger.info("Retrieving documents for query: '%s'", query)
        docs = self.vectordb.similarity_search(
            query,
            k=settings.search_k,
        )

        if not docs:
            return f"No documents found for query: '{query}'"

        return "\nRetrieved documents:\n" + "".join(
            [
                f"===== Document {str(i)} (Source: {doc.metadata.get('source', 'unknown')}) =====\n{doc.page_content}\n"
                for i, doc in enumerate(docs)
            ]
        )
