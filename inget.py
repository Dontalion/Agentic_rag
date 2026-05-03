from tqdm import tqdm
from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from config import get_settings

settings = get_settings()

def process_documents(source_docs):
    """
    Process documents: tokenize, split, embed, and create vector database.
    
    Args:
        source_docs: List of Document objects
        
    Returns:
        FAISS vector database
    """
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(settings.tokenizer_model_name, token=settings.huggingface_token if settings.huggingface_token else None),
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    # Split docs and keep only unique ones
    print("Splitting documents...")
    docs_processed = []
    unique_texts = {}
    for doc in tqdm(source_docs):
        new_docs = text_splitter.split_documents([doc])
        for new_doc in new_docs:
            if new_doc.page_content not in unique_texts:
                unique_texts[new_doc.page_content] = True
                docs_processed.append(new_doc)

    print(
        "Embedding documents... This should take a few minutes (5 minutes on MacBook with M1 Pro)"
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name=settings.embedding_model_name,
        model_kwargs={"token": settings.huggingface_token} if settings.huggingface_token else {}
    )
    distance_strategy = DistanceStrategy.COSINE if settings.distance_strategy.upper() == "COSINE" else DistanceStrategy.EUCLIDEAN
    vectordb = FAISS.from_documents(
        documents=docs_processed,
        embedding=embedding_model,
        distance_strategy=distance_strategy,
    )
    return vectordb