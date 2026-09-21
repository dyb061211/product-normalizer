from ai.tools import get_run_detail_tool,get_runs_tool,get_run_issues_tool
from langchain_core.tools import tool

@tool
def get_run_detail(run_id:int):
    "Get details for a processing run."
    return get_run_detail_tool(run_id)

@tool
def get_runs(limit:int):
    "Get recent processing runs."
    return get_runs_tool(limit)

@tool
def get_run_issues(run_id:int):
    "Get validation issues for a processing run."
    return get_run_issues_tool(run_id)

TOOLS=[get_run_detail,get_runs,get_run_issues]