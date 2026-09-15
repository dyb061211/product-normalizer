from langchain_huggingface import HuggingFaceEmbeddings
from product_normalizer.rag.config import EMBEDDING_MODEL_NAME
from functools import lru_cache

@lru_cache(maxsize=1)
def get_embedding_model()->HuggingFaceEmbeddings:
    embedding=HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )
    return embedding
