from langchain_core.documents import Document
from product_normalizer.rag.config import CHUNK_SIZE,CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents:list[Document])-> list[Document]:
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks=text_splitter.split_documents(documents)
    return chunks
