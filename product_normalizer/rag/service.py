from product_normalizer.rag.embeddings import get_embedding_model
from product_normalizer.rag.vector_store import create_vector_store
from product_normalizer.rag.retriever import retrieve_documents
from product_normalizer.rag.schemas import RAGResponse,RAGSource
from langchain_core.documents import Document
from product_normalizer.rag.prompts import build_context,RAG_PROMPT
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import logging
import time

logger=logging.getLogger(__name__)

load_dotenv()

def answer_question(question:str)->RAGResponse:
    start_time=time.perf_counter()
    embedding_model=get_embedding_model()
    embedding_elapsed=time.perf_counter()-start_time
    logger.info(
        "RAG embedding model ready: elapsed=%.3fs",
        embedding_elapsed,
    )
    vector_store=create_vector_store(embedding_model)
    retrieval_start = time.perf_counter()
    try:
        docs = retrieve_documents(vector_store, question)
    except Exception:
        logger.exception("RAG retrieval failed")
        raise
    retrieval_elapsed=time.perf_counter()-retrieval_start
    logger.info(
        "RAG retrieval completed:retrived_count=%d,retrival_elapsed=%.3f",
        len(docs),
        retrieval_elapsed
    )
    if not docs:
        elapsed=time.perf_counter()-start_time
        logger.info(
            "RAG no-answer:retrived_count=0,total_elapsed=%.3f",
            elapsed
        )
        return RAGResponse(
            answer="知识库中没有找到足够相关的信息.",
            sources=[]
        )
    sources=build_sources(docs)
    context=build_context(docs)
    prompt_value=RAG_PROMPT.invoke({
        "context":context,
        "question":question,
    })
    llm_start=time.perf_counter()
    try:
        model = init_chat_model(
            model="deepseek-chat",
            model_provider="deepseek"
        )
        response = model.invoke(prompt_value)
    except Exception:
        logger.exception("RAG LLM failed")
        raise
    llm_elapsed = time.perf_counter() - llm_start
    logger.info(
        "RAG LLM completed: llm_elapsed=%.3fs",
        llm_elapsed,
    )
    answer=response.content
    elapsed = time.perf_counter() - start_time
    logger.info(
        "RAG success: retrieved_count=%d sources=%s total_elapsed=%.3fs",
        len(docs),
        [source.filename for source in sources],
        elapsed,
    )
    return RAGResponse(
        answer=answer,
        sources=sources
    )

def build_sources(docs:list[Document])->list[RAGSource]:
    result=[]
    seen_source=set()
    for doc in docs:
        filename=doc.metadata['filename']
        source=doc.metadata['source']
        if source in seen_source:
            continue
        result.append(RAGSource(
            filename=filename,
            source=source
        ))
        seen_source.add(source)
    return result



if __name__=="__main__":
    result = answer_question(
         "What is the weather like today in Los Angeles?"
    )

    print(result.answer)
    print(result.sources)