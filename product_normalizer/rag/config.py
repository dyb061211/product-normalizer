from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR=PROJECT_ROOT/"examples"/"rag_week8"/ "knowledge"
VECTORSTORE_DIR=PROJECT_ROOT / "data" / "vectorstore"
COLLECTION_NAME="product_normalizer_knowledge"

CHUNK_SIZE=100
CHUNK_OVERLAP=20

EMBEDDING_MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"

TOP_K=3
RELEVANCE_THRESHOLD=40.0
