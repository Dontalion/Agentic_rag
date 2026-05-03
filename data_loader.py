from langchain_core.documents import Document

def load_documents(knowledge_base):
    """
    Load and create source documents from knowledge base.
    
    Args:
        knowledge_base: List of dictionaries with 'text' and 'source' keys
        
    Returns:
        List of Document objects
    """
    source_docs = [
        Document(page_content=doc["text"], metadata={"source": doc["source"].split("/")[1]})
        for doc in knowledge_base
    ]
    return source_docs