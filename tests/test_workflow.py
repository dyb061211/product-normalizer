from unittest.mock import Mock
from product_normalizer.ai.workflow.nodes import route_request
from product_normalizer.ai.workflow.schemas import RouteDecision
from product_normalizer.ai.workflow import nodes
from product_normalizer.rag.schemas import RAGSource,RAGResponse
from langchain_core.messages import AIMessage,HumanMessage
from product_normalizer.ai.workflow.service import run_workflow
from product_normalizer.ai.workflow import tools
from product_normalizer.ai.workflow.service import workflow_graph
from product_normalizer.ai.workflow.routers import should_continue_tools

def test_route_request_writes_route(monkeypatch):
    fake_router=Mock()
    fake_router.invoke.return_value=RouteDecision(route="tools")
    monkeypatch.setattr(
        nodes,
        "structured_router",
        fake_router
    )
    state = {
        "user_query": "run 6有什么问题？"
    }
    result=route_request(state)
    assert result == {"route":"tools"}
    fake_router.invoke.assert_called_once_with(
        {
            "question": "run 6有什么问题？"
        }
    )

def test_rag_answer_updates_state(monkeypatch):
    fake_response=RAGResponse(
        answer="MAX_TOOL_ROUNDS = 3",
        sources=[
            RAGSource(
                filename="error_handling.md",
                source="/fake/error_handling.md"
            )
        ]
    )
    answer_question_mock=Mock(
        return_value=fake_response
    )
    monkeypatch.setattr(
        nodes,
        "answer_question",
        answer_question_mock
    )
    state = {
        "user_query": "MAX_TOOL_ROUNDS是多少？"
    }
    result=nodes.rag_answer(state)
    assert result["answer"] == "MAX_TOOL_ROUNDS = 3"
    assert result["status"] == "success"
    assert result["sources"] == fake_response.sources
    answer_question_mock.assert_called_once_with(
        "MAX_TOOL_ROUNDS是多少？"
    )

def test_direct_path_returns_workflow_result(monkeypatch):
    fake_router=Mock()
    fake_router.invoke.return_value=RouteDecision(route="direct")
    monkeypatch.setattr(
        nodes,
        "structured_router",
        fake_router
    )
    fake_model=Mock()
    fake_model.invoke.return_value=AIMessage(
        content="你好，我是 Product Normalizer Assistant。"
    )
    monkeypatch.setattr(
        nodes,
        "model",
        fake_model
    )
    result = run_workflow("你好")
    assert result.answer=="你好，我是 Product Normalizer Assistant。"
    assert result.route == "direct"
    assert result.status == "success"
    assert result.sources == []

def test_tool_path_runs_one_tool_round(monkeypatch):
    fake_router = Mock()
    fake_router.invoke.return_value = RouteDecision(route="tools")
    monkeypatch.setattr(
        nodes,
        "structured_router",
        fake_router
    )
    fake_tool_model=Mock()
    fake_tool_model.invoke.side_effect=[
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_run_issues",
                    "args": {"run_id": 6},
                    "id": "call-test-1",
                    "type": "tool_call",
                }
            ]
        ),
        AIMessage(
            content="run 6 有 2 个校验问题。",
            tool_calls=[]
        )
    ]
    monkeypatch.setattr(
        nodes,
        "tool_model",
        fake_tool_model
    )
    get_run_issues_mock = Mock(
        return_value=[
            {"field": "sku", "message": "sku不能为空"},
            {"field": "upc", "message": "upc重复"},
        ]
    )
    monkeypatch.setattr(
        tools,
        "get_run_issues_tool",
        get_run_issues_mock
    )
    question = "run 6有什么问题？"
    initial_state = {
        "messages": [HumanMessage(content=question)],
        "user_query": question,
        "route": None,
        "tool_rounds": 0,
        "answer": None,
        "sources": [],
        "status": "running",
        "error_type": None,
        "error_message": None,
    }
    result = workflow_graph.invoke(initial_state)
    assert result["route"] == "tools"
    assert result["status"] == "success"
    assert result["answer"] == "run 6 有 2 个校验问题。"
    assert result["tool_rounds"] == 1
    assert fake_tool_model.invoke.call_count==2
    get_run_issues_mock.assert_called_once_with(6)

def test_rag_answer_returns_no_answer(monkeypatch):
    fake_response=RAGResponse(
        answer="知识库中没有找到足够相关的信息。",
        sources=[]
    )
    answer_question_mock=Mock(return_value=fake_response)
    monkeypatch.setattr(
        nodes,
        "answer_question",
        answer_question_mock
    )
    state = {
        "user_query": "这个项目2028年的年度营收目标是多少？"
    }
    result=nodes.rag_answer(state)
    assert result["answer"] == "知识库中没有找到足够相关的信息。"
    assert result["sources"] == []
    assert result["status"] == "no_answer"

def test_tool_path_stops_at_max_rounds():
    state = {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "get_run_issues",
                        "args": {"run_id": 6},
                        "id": "call-test-max-rounds",
                        "type": "tool_call",
                    }
                ],
            )
        ],
        "tool_rounds": 3,
    }
    result = should_continue_tools(state)
    assert result == "max_rounds"
    error_update = nodes.max_rounds_error(state)
    assert error_update["status"] == "error"
    assert error_update["error_type"] == "max_rounds_error"