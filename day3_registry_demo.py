from ai.tool_registry import TOOL_REGISTRY
from ai.tool_registry import execute_tool

func = TOOL_REGISTRY["get_run_detail"]

res=execute_tool("get_run_issues", {"run_id": 1})
print(res)


