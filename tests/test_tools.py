from unittest.mock import Mock,patch
from ai.tools import get_run_detail_tool,get_runs_tool,get_run_issues_tool

def test_get_run_detail_tool():
    fake_run={
        "id":1,
        "status":"success"
    }
    with patch(
        "ai.tools.get_run",
        return_value=fake_run
    ) as get_run_mock:
        result=get_run_detail_tool(1)
    assert result == fake_run
    get_run_mock.assert_called_once_with(1)

def test_get_runs_tool():
    fake_run=[
        {
            "id":1,
            "status":"success"
        },
        {
            "id":2,
            "status":"success"
        }
    ]
    with patch(
        "ai.tools.get_runs",
        return_value=fake_run
    ) as get_run_mock:
        result=get_runs_tool(2)
    assert result == fake_run
    get_run_mock.assert_called_once_with(2)

def test_get_run_issues_tool():
    fake_run={
        "id":1,
        "status":"success"
    }
    with patch(
        "ai.tools.get_run_issues",
        return_value=fake_run
    ) as get_run_issues_mock:
        result=get_run_issues_tool(1)
    assert result == fake_run
    get_run_issues_mock.assert_called_once_with(1)
