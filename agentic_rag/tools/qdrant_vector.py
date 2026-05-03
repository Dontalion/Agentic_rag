from smolagents import Tool
from qdrant_client import QdrantClient
from fastembed import TextEmbedding

class QdrantQueryTool(Tool):
    name = "qdrant_query"
    description = "Query the Qdrant vector database for relevant information based on a natural language query."
    
    inputs = {
        "query": {
            "type": "string",
            "description": "The natural language query to search for relevant information in the vector database.",
            }
    }
    output_type = "string"
    
    def __init__(self, collection_name: str, **kwargs):
        super().__init__(**kwargs)
        self.collection_name = collection_name
        self.client = QdrantClient() # If running locally
        self.embedding_model = TextEmbedding()
    
    def forward(self, query: str) -> str:
        #generate embedding for query
        query_embedding = list(self.embedding_model.query_embed(query))[0]
            
        #semantic search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=3,  # تعداد نتایج
        )
        
        # Extract and concatenate the relevant information from search results
        if not search_result:
            return "No relevant information found."
        
        formatted_results = ["retrieved information: \n"]
        for i, point in enumerate(search_result):
            formatted_results.append(f"== Result {i+1} ==\n")
            formatted_results.append(f"content: {point.payload['text']}\n")
        return "\n".join(formatted_results)
