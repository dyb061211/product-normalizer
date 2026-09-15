import numpy as np
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

question="What is the weather in USA today"
results=vector_store.similarity_search_with_score(
    question,
    k=3
)

print(type(results))
print(len(results))
print(results[0])
print(results[0][0])

for doc,score in results:
    print(score)
    print("content:", doc.page_content)
    print("metadata:", doc.metadata)
    print()



