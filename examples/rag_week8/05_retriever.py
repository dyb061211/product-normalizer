from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)

vector_store=InMemoryVectorStore(
    embedding=embeddings
)

documents=[
    Document(
        page_content="Maximum tool rounds is 3.",
        metadata={"source":"error_handling.md"}
    ),
    Document(
        page_content="The /assistant endpoint accepts a user message",
        metadata={"source": "api_guide.md"}
    ),
    Document(
        page_content="Portable camping chair costs 29.99 dollars.",
        metadata={"source": "product.md"}
    )
]

vector_store.add_documents(documents)

question = "What is the weather in Los Angeles today?"
retriever=vector_store.as_retriever(
    search_kwargs={"k":2}
)

docs=retriever.invoke(question)

print(type(retriever))
print(docs)
print(type(docs))
print(len(docs))

for doc in docs:
    print(type(doc))
    print(doc.page_content)
    print(doc.metadata)
    print()