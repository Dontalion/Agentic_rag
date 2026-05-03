from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application using environment variables and .env file.
    """
    # API Keys
    openai_api_key: str | None = None
    huggingface_token: str | None = None

    # Model configuration
    model_name: str = "meta-llama/Llama-3.1-70B-Instruct"
    # Embedding model configuration
    embedding_model_name: str = "thenlper/gte-small"

    # Tokenizer model configuration
    tokenizer_model_name: str = "thenlper/gte-small"

    # Text splitting configuration
    chunk_size: int = 200
    chunk_overlap: int = 20

    # Vector database configuration
    distance_strategy: str = "COSINE"

    # Similarity search configuration
    search_k: int = 5

    class Config:
        # Read from environment variables and .env file
        env_prefix = "AGENTIC_RAG_"
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
@lru_cache()
def get_settings():
    return Settings()
