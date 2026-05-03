from data_loader import load_documents
from inget import process_documents
from config import get_settings
from langchain_core.vectorstores import VectorStore

settings = get_settings()

def handle_user_query(vectordb, query):
    """
    Handle user query by performing similarity search in the vector database.
    
    Args:
        vectordb: FAISS vector database
        query: User's query string
        
    Returns:
        List of relevant documents
    """
    docs = vectordb.similarity_search(query, k=settings.search_k)
    return docs

def main():
    """
    Main function to load documents, process them, and handle user queries.
    """
    # Example knowledge_base - replace with actual data loading
    knowledge_base = [
        {"text": "Example document text 1", "source": "source1/file.txt"},
        {"text": "Example document text 2", "source": "source2/file.txt"},
    ]
    
    # Load documents
    source_docs = load_documents(knowledge_base)
    
    # Process documents (tokenize and embed)
    vectordb = process_documents(source_docs)
    
    # Handle user queries
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        relevant_docs = handle_user_query(vectordb, query)
        print("Relevant documents:")
        for doc in relevant_docs:
            print(f"- {doc.page_content} (source: {doc.metadata['source']})")
        print()

if __name__ == "__main__":
    main()