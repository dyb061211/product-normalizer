from types import SimpleNamespace
from unittest.mock import Mock,patch
from ai.agent_service import run_agent
import pytest
from ai.exceptions import ToolArgumentError,ToolExecutionError,UnknownToolError,AgentMaxRoundsError

def test_run_agent_without_tool_call():
    fake_response=SimpleNamespace(
        output=[],
        output_text="Hello,this is test answer"
    )
    client_mock=Mock()
    client_mock.create_response.return_value=fake_response
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool"
    ) as execute_tool_mock:
        result=run_agent("Hello")
    assert result=="Hello,this is test answer"
    client_mock.create_response.assert_called_once()
    execute_tool_mock.assert_not_called()

def test_run_agent_with_tool_call():
    tool_call=SimpleNamespace(
        type="function_call",
        name="get_run_detail",
        arguments='{"run_id": 1}',
        call_id="call_test_1"
    )
    first_response=SimpleNamespace(
        output=[tool_call],
        output_text=""
    )
    second_response=SimpleNamespace(
        output=[],
        output_text="Run 1 processing succeeded"
    )
    client_mock=Mock()
    client_mock.create_response.side_effect=[
        first_response,
        second_response
    ]
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool",
        return_value={
            "id":1,
            "status":"success"
        }
    ) as execute_tool_mock:
        result = run_agent("帮我查看 run 1")
    assert result == "Run 1 processing succeeded"
    assert client_mock.create_response.call_count == 2
    execute_tool_mock.assert_called_once_with(
        "get_run_detail",
        {"run_id": 1}
    )
    second_call=client_mock.create_response.call_args_list[1]
    second_input=second_call.kwargs["input_text"]
    assert second_input[-2]=={
        "type":"function_call",
        "call_id": "call_test_1",
        "name":"get_run_detail",
        "arguments":'{"run_id": 1}'
    }
    assert second_input[-1]=={
        "type":"function_call_output",
        "call_id": "call_test_1",
        "output": '{"id": 1, "status": "success"}'
    }

def test_run_agent_tool_argument_error():
    tool_call=SimpleNamespace(
        type="function_call",
        name="get_run_detail",
        arguments='{"run_id": "abc"}',
        call_id="call_test_1"
    )
    fake_response=SimpleNamespace(
        output=[tool_call],
        output_text=""
    )
    client_mock=Mock()
    client_mock.create_response.return_value = fake_response
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool",
        side_effect=ToolArgumentError("Invalid arguments for tool: get_run_detail")
    ) as execute_tool_mock:
        with pytest.raises(ToolArgumentError) as exc:
            run_agent("请帮我查看abc")
    assert "get_run_detail" in str(exc.value)
    execute_tool_mock.assert_called_once_with(
        "get_run_detail",
        {"run_id": "abc"}
    )
    assert client_mock.create_response.call_count==1

def test_run_agent_tool_execution_error():
    tool_call=SimpleNamespace(
        type="function_call",
        name="get_run_detail",
        arguments='{"run_id": 1}',
        call_id="call_test_1"
    )
    fake_response=SimpleNamespace(
        output=[tool_call],
        output_text=""
    )
    client_mock=Mock()
    client_mock.create_response.return_value = fake_response
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool",
        side_effect=ToolExecutionError("Tool execution failed: get_run_detail")
    ) as execute_tool_mock:
        with pytest.raises(ToolExecutionError) as exc:
            run_agent("请帮我查看run_id=1")
    assert "get_run_detail" in str(exc.value)
    execute_tool_mock.assert_called_once_with(
        "get_run_detail",
        {"run_id": 1}
    )
    assert client_mock.create_response.call_count==1

def test_run_agent_unknown_error():
    tool_call = SimpleNamespace(
        type="function_call",
        name="wrong_name",
        arguments='{"run_id": 1}',
        call_id="call_test_1"
    )
    fake_response = SimpleNamespace(
        output=[tool_call],
        output_text=""
    )
    client_mock = Mock()
    client_mock.create_response.return_value = fake_response
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool",
        side_effect=UnknownToolError("There is no tool registered with this wrong_name")
    ) as execute_tool_mock:
        with pytest.raises(UnknownToolError) as exc:
            run_agent("请帮我查看run_id=1")
    assert "wrong_name" in str(exc.value)
    execute_tool_mock.assert_called_once_with(
        "wrong_name",
        {"run_id": 1}
    )
    assert client_mock.create_response.call_count==1

def test_run_agent_max_rounds_error():
    tool_call = SimpleNamespace(
        type="function_call",
        name="get_run_detail",
        arguments='{"run_id": 1}',
        call_id="call_test_1"
    )
    fake_response = SimpleNamespace(
        output=[tool_call],
        output_text=""
    )
    client_mock = Mock()
    client_mock.create_response.return_value = fake_response
    with patch(
        "ai.agent_service.LLMClient",
        return_value=client_mock
    ),patch(
        "ai.agent_service.execute_tool",
        return_value=('{"id":1,"status":"success"}')
    ) as execute_tool_mock:
        with pytest.raises(AgentMaxRoundsError) as exc:
            run_agent("请帮我查看run_id=1")
    assert "The maximum number of rounds has been reached"==str(exc.value)
    assert execute_tool_mock.call_count==3
    assert client_mock.create_response.call_count==4
