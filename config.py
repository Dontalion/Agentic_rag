from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configuration settings for the application using environment variables and .env file.
    """
    # API Keys
    openai_api_key: str
    huggingface_token: str
    
    # Model configuration
    model_name: str 
    # Embedding model configuration
    embedding_model_name: str 
    
    # Tokenizer model configuration
    tokenizer_model_name: str 
    
    # Text splitting configuration
    chunk_size: int 
    chunk_overlap: int
    
    # Vector database configuration
    distance_strategy: str
    
    # Similarity search configuration
    search_k: int
    
    class Config:
        # Read from environment variables and .env file
        env_prefix = "AGENTIC_RAG_"
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
@lru_cache()
def get_settings():
    return Settings()
