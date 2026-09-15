from langchain_core.documents import Document
from unittest.mock import Mock
from product_normalizer.rag.retriever import retrieve_documents

def test_retrieve_documents_filters_by_threshold(monkeypatch):
    relevant_doc = Document(
        page_content="MAX_TOOL_ROUNDS = 3",
        metadata={"filename": "error_handling.md"}
    )

    irrelevant_doc = Document(
        page_content="GET /health returns ok",
        metadata={"filename": "api_guide.md"}
    )
    vector_store=Mock()
    vector_store.similarity_search_with_score.return_value=[
        (relevant_doc, 0.2),
        (irrelevant_doc, 10.0),
    ]
    monkeypatch.setattr(
        "product_normalizer.rag.retriever.RELEVANCE_THRESHOLD",
        1.0
    )
    result=retrieve_documents(vector_store,"How many tool rounds are allowed?")
    assert result == [relevant_doc]