from unittest.mock import Mock,patch
from types import SimpleNamespace
from ai.agent_service import run_agent
from ai.exceptions import AgentMaxRoundsError
import ai.agent_service
from product_normalizer.logging_config import  setup_logging

setup_logging()

tool_call=SimpleNamespace(
    type="function_call",
    name="get_run_detail",
    arguments='{"run_id":1}',
    call_id="call_test"
)

fake_response=SimpleNamespace(
    output=[tool_call],
    output_text=""
)

mock_execute_tool=Mock(
    return_value={"id": 1, "status": "success"}
)
mock_client=Mock()
mock_client.create_response.return_value=fake_response
with patch(
    "ai.agent_service.LLMClient",
    return_value=mock_client,

),patch(
    "ai.agent_service.execute_tool",
    mock_execute_tool
):
    try:
        run_agent("请帮我查看最近出错的消息")
    except AgentMaxRoundsError as exc:
        print(mock_client.create_response.call_count)
        print(mock_execute_tool.call_count)
        print(exc)
