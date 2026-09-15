from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

def load_documents()->list[Document]:
    return [
        Document(
            page_content="Maximum tool rounds is 3.",
            metadata={"source": "error_handling.md"}
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
def split_documents(documents:list[Document])->list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    chunks=text_splitter.split_documents(documents)
    return chunks

def build_vector_store(documents:list[Document],embeddings):
    vector_store = InMemoryVectorStore(
        embedding=embeddings
    )
    vector_store.add_documents(documents)
    return vector_store

def retrieve_documents(vector_store,question:str,k:int=2)->list[Document]:
    retriever=vector_store.as_retriever(
        search_kwargs={"k":k}
    )
    documents=retriever.invoke(question)
    return documents

def build_context(docs:list[Document])->str:
    result=[]
    for doc in docs:
        content=doc.page_content
        source=doc.metadata.get("source","unknown")
        block=f"{source}\n{content}"
        result.append(block)
    return "\n\n".join(result)

def answer_question(
    question: str,
    vector_store,
    model,
    k: int = 2,
) -> str:
    docs = retrieve_documents(
        vector_store,
        question,
        k
    )
    for doc in docs:
        print(doc.page_content)
    context = build_context(docs)
    print(context)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant. "
            "Answer using only the provided context. "
            "Use semantically equivalent information even if the wording "
            "does not exactly match the question. "
            "If the context truly does not contain the answer, say you do not know."
        ),
        (
            "human",
            """Context:
    {context}

    Question:
    {question}"""
        )
    ])
    prompt_value = prompt.invoke({
        "question": question,
        "context": context,
    })
    response = model.invoke(prompt_value)
    return response.content

embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)
documents=load_documents()
chunks=split_documents(documents)
vector_store=build_vector_store(chunks,embeddings)
model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

answer = answer_question(
    question="What is the limit on agent tool usage?",
    vector_store=vector_store,
    model=model,
)
print(answer)

