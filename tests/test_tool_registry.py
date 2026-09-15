import sys
from unittest.mock import Mock,patch
from ai.tool_registry import execute_tool
import pytest
from ai.exceptions import UnknownToolError,ToolArgumentError,ToolExecutionError

def test_execute_tool_success():
    tool_mock=Mock(return_value={"id":1})
    with patch.dict(
        "ai.tool_registry.TOOL_REGISTRY",
            {"get_run_detail":tool_mock}
    ):
        result=execute_tool(
            "get_run_detail",
            {"run_id":1}
        )
    assert result=={"id":1}
    tool_mock.assert_called_once_with(run_id=1)

def test_execute_tool_unknown_error():
    with pytest.raises(UnknownToolError) as exc:
        execute_tool(
            "delete_database",
            {}
        )
    assert "delete_database" in str(exc.value)

def test_execute_tool_invalidate_arguments_error():
    with pytest.raises(ToolArgumentError) as exc:
        execute_tool(
            "get_run_detail",
            {"run_id": "abc"}
        )
    assert "get_run_detail" in str(exc.value)

def test_execute_tool_failed_execution_error():
    tool_mock=Mock(
        side_effect=RuntimeError("database failed")
    )
    with patch.dict(
        "ai.tool_registry.TOOL_REGISTRY",
        {"get_run_detail":tool_mock}
    ):
        with pytest.raises(ToolExecutionError) as exc:
            execute_tool(
                "get_run_detail",
                {"run_id": "1"}
            )
    assert "get_run_detail" in str(exc.value)
    tool_mock.assert_called_once_with(run_id=1)