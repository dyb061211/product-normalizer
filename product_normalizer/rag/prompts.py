from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

def build_context(docs:list[Document])->str:
    result=[]
    for doc in docs:
        content=doc.page_content
        source=doc.metadata.get("filename","unknown")
        block=f"[Source: {source}]\n{content}"
        result.append(block)
    return "\n\n".join(result)

RAG_PROMPT=ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer the user's question using only the provided context. "
        "If the context does not contain the answer, say you do not know."
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion:\n{question}"
    )
])
