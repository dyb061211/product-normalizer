from langchain_chroma import Chroma
from product_normalizer.rag.config import VECTORSTORE_DIR, COLLECTION_NAME

def create_vector_store(embeddings)->Chroma:
    vector_store=Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTORSTORE_DIR)
    )
    return vector_store

def delete_vector_store_collection(embeddings)->None:
    vector_store=create_vector_store(embeddings)
    vector_store.delete_collection()
