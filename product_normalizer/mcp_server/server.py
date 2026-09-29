from mcp.server import MCPServer
from ai.tools import get_run_detail_tool as business_get_run_detail,get_runs_tool as business_get_runs,get_run_issues_tool as business_get_run_issues

mcp=MCPServer("product-normalizer")

@mcp.tool()
def get_run_detail(run_id:int):
    """
    Get processing details for a specific product-normalizer run
    """
    return business_get_run_detail(run_id)

@mcp.tool()
def get_run_issues(run_id:int):
    """
    Get issue details for a specific product-normalizer run
    """
    return business_get_run_issues(run_id)

@mcp.tool()
def get_runs(limit:int):
    """
    Get processing details for some product-normalizer runs
    """
    return business_get_runs(limit)

@mcp.resource("project://overview")
def project_overview()->str:
    """
        Basic overview of the product-normalizer project.
    """
    return """
        Project: product-normalizer
        Purpose: Normalize product data and expose processing history.
        MCP Tools:
        - get_runs
        - get_run_detail
        - get_run_issues
        """

@mcp.resource("run://{run_id}/summary")
def run_summary(run_id: str) -> str:
    """
    Return a short summary for a processing run.
    """
    return f"Processing run id: {run_id}"

@mcp.prompt()
def explain_run(run_id: str, issue_text: str) -> str:
    """
    Create a prompt for explaining a product-normalizer run issue.
    """
    return (
        f"Explain the following product-normalizer processing issue.\n"
        f"Run ID: {run_id}\n"
        f"Issue: {issue_text}\n"
        f"Explain the likely meaning and what should be checked."
    )