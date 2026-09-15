from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()

def build_context(docs:list[Document])->str:
    results=[]
    for doc in docs:
        content=doc.page_content
        source=doc.metadata.get("source","unknown")
        block=f"Source:{source}\n{content}"
        results.append(block)
    return "\n\n".join(results)

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
print(type(vector_store))
retriever=vector_store.as_retriever(
    search_kwargs={"k":2}
)

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)
question = "What is the weather in Los Angeles today?"
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant.Answer the {question} using only the provided {context}.If the {context} does not contain the answer,say that you do not know based on the provided {context}.")
    ]
)

docs=retriever.invoke(question)
print(type(docs))
context=build_context(docs)
print(type(context))
print(context)

prompt_value=prompt.invoke({
    "question":question,
    "context":context,
})

print(type(prompt_value))
print(prompt_value)

response = model.invoke(prompt_value)

print(type(response))
print(response.content)

