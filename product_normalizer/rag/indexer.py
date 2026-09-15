from product_normalizer.rag.loader import load_documents
from product_normalizer.rag.splitter import split_documents
from product_normalizer.rag.embeddings import get_embedding_model
from product_normalizer.rag.vector_store import create_vector_store,delete_vector_store_collection
from product_normalizer.rag.config import KNOWLEDGE_DIR

def build_index():
    documents=load_documents(KNOWLEDGE_DIR)
    chunks=split_documents(documents)
    embedding_model=get_embedding_model()
    vector_store=create_vector_store(
        embedding_model
    )
    vector_store.add_documents(chunks)
    return {
        "documents_count":len(documents),
        "chunks_count":len(chunks)
    }

def rebuild_index():
    embedding_model=get_embedding_model()
    delete_vector_store_collection(embedding_model)
    return build_index()
