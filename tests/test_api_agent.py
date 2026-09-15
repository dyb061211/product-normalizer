from fastapi.testclient import TestClient
from unittest.mock import Mock,patch
from api.app import app
from ai.exceptions import AgentMaxRoundsError, UnknownToolError,ToolArgumentError,ToolExecutionError

client=TestClient(app)

def test_assistant_success():
    with patch(
        "api.routes.run_agent",
        return_value="这是测试回答"
    ) as run_agent_mock:
        response=client.post("/assistant",json={"message":"帮我查看最近失败的运行"})
        assert response.status_code == 200
        assert response.json()=={
            "answer":"这是测试回答"
        }
        run_agent_mock.assert_called_once_with("帮我查看最近失败的运行")

def test_assistant_empty_message_returns_422():
    with patch("api.routes.run_agent") as run_agent_mock:
        response=client.post("/assistant",json={"message":""})
        assert response.status_code == 422
        run_agent_mock.assert_not_called()

def test_assistant_agent_max_rounds_returns_500():
    with patch(
        "api.routes.run_agent",
        side_effect=AgentMaxRoundsError(
            "The maximum number of rounds has been reached"
        ),
    ):
        response = client.post(
            "/assistant",
            json={"message": "帮我查看最近失败的运行"},
        )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Agent exceeded maximum tool rounds"
    }

def test_assistant_unknown_tool_returns_500():
    with patch(
        "api.routes.run_agent",
        side_effect=UnknownToolError("unknown tool")
    ):
        response = client.post(
            "/assistant",
            json={"message": "帮我查看最近失败的运行"}
        )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Unknown tool"
    }

def test_assistant_tool_argument_error_returns_500():
    with patch(
        "api.routes.run_agent",
        side_effect=ToolArgumentError(
            "Invalid arguments for tool: get_run_detail"
        ),
    ):
        response = client.post(
            "/assistant",
            json={"message": "帮我查看 run abc"},
        )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Invalid arguments for tool: get_run_detail"
    }


def test_assistant_tool_execution_error_returns_500():
    with patch(
        "api.routes.run_agent",
        side_effect=ToolExecutionError(
            "Tool execution failed: get_run_detail"
        ),
    ):
        response = client.post(
            "/assistant",
            json={"message": "帮我查看 run 1"},
        )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Tool execution failed: get_run_detail"
    }