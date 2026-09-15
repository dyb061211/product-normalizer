from langchain_core.documents import Document
from product_normalizer.rag.config import TOP_K,RELEVANCE_THRESHOLD

def retrieve_documents(vector_store,question:str)->list[Document]:
    result=[]
    docs=vector_store.similarity_search_with_score(
        question,
        k=TOP_K
    )
    for doc,score in docs:
        if score<=RELEVANCE_THRESHOLD:
            result.append(doc)
    return result
