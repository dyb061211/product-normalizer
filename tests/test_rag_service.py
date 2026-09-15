from unittest.mock import Mock
import product_normalizer.rag.service as rag_service
from langchain_core.documents import Document
import pytest

def test_answer_question_does_not_call_llm_when_no_docs(monkeypatch):
    fake_embedding_model=Mock()
    fake_vector_store=Mock()
    get_embedding_model_mock = Mock(return_value=fake_embedding_model)
    monkeypatch.setattr(
        rag_service,
        "get_embedding_model",
        get_embedding_model_mock
    )
    create_vector_store_mock = Mock(return_value=fake_vector_store)
    monkeypatch.setattr(
        rag_service,
        "create_vector_store",
        create_vector_store_mock
    )
    monkeypatch.setattr(
        rag_service,
        "retrieve_documents",
        Mock(return_value=[])
    )
    model_mock=Mock()
    init_model_mock=Mock(return_value=model_mock)
    monkeypatch.setattr(
        rag_service,
        "init_chat_model",
        init_model_mock
    )
    result=rag_service.answer_question(
        "What is the weather tomorrow?"
    )
    assert result.answer == "知识库中没有找到足够相关的信息."
    assert result.sources==[]
    init_model_mock.assert_not_called()
    model_mock.invoke.assert_not_called()

def test_answer_question_calls_llm_when_docs_found(monkeypatch):
    fake_embedding_model = Mock()
    fake_vector_store = Mock()
    doc = Document(
        page_content="MAX_TOOL_ROUNDS = 3",
        metadata={
            "filename": "error_handling.md",
            "source": "knowledge/error_handling.md",
        }
    )
    monkeypatch.setattr(
        rag_service,
        "get_embedding_model",
        Mock(return_value=fake_embedding_model)
    )
    monkeypatch.setattr(
        rag_service,
        "create_vector_store",
        Mock(return_value=fake_vector_store)
    )
    monkeypatch.setattr(
        rag_service,
        "retrieve_documents",
        Mock(return_value=[doc])
    )
    fake_response=Mock()
    fake_response.content="The maximum number of tool rounds is 3."
    model_mock=Mock(return_value=fake_response)
    model_mock.invoke.return_value=fake_response
    init_model_mock=Mock(return_value=model_mock)
    monkeypatch.setattr(
        rag_service,
        "init_chat_model",
        init_model_mock
    )
    result=rag_service.answer_question("How many tool rounds are allowed?")
    assert result.answer == "The maximum number of tool rounds is 3."
    assert len(result.sources) == 1
    assert result.sources[0].filename == "error_handling.md"
    assert result.sources[0].source == "knowledge/error_handling.md"
    init_model_mock.assert_called_once()
    model_mock.invoke.assert_called_once()

def test_answer_question_raises_when_retriever_fails(monkeypatch):
    fake_embedding_model = Mock()
    fake_vector_store = Mock()
    doc = Document(
        page_content="MAX_TOOL_ROUNDS = 3",
        metadata={
            "filename": "error_handling.md",
            "source": "knowledge/error_handling.md",
        }
    )
    monkeypatch.setattr(
        rag_service,
        "get_embedding_model",
        Mock(return_value=fake_embedding_model)
    )
    monkeypatch.setattr(
        rag_service,
        "create_vector_store",
        Mock(return_value=fake_vector_store)
    )
    monkeypatch.setattr(
        rag_service,
        "retrieve_documents",
        Mock(side_effect=RuntimeError("retrieval failed"))
    )
    with pytest.raises(RuntimeError) as exc:
        rag_service.answer_question("How many tool rounds are allowed?")

    assert str(exc.value)=="retrieval failed"

def test_answer_question_raises_when_llm_fails(monkeypatch):
    fake_embedding_model = Mock()
    fake_vector_store = Mock()
    doc = Document(
        page_content="MAX_TOOL_ROUNDS = 3",
        metadata={
            "filename": "error_handling.md",
            "source": "knowledge/error_handling.md",
        }
    )
    monkeypatch.setattr(
        rag_service,
        "get_embedding_model",
        Mock(return_value=fake_embedding_model)
    )
    monkeypatch.setattr(
        rag_service,
        "create_vector_store",
        Mock(return_value=fake_vector_store)
    )
    monkeypatch.setattr(
        rag_service,
        "retrieve_documents",
        Mock(return_value=[doc])
    )
    model_mock = Mock()
    model_mock.invoke.side_effect = RuntimeError("llm failed")
    monkeypatch.setattr(
        rag_service,
        "init_chat_model",
        Mock(return_value=model_mock)
    )
    with pytest.raises(RuntimeError) as exc:
        rag_service.answer_question(
            "How many tool rounds are allowed?"
        )
    assert str(exc.value) == "llm failed"