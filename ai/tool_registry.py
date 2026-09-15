from ai.tools import get_run_detail_tool,get_run_issues_tool,get_runs_tool
from ai.schemas import RunDetailArguments,RunIssuesArguments,RunsArguments
from ai.exceptions import UnknownToolError,ToolArgumentError,ToolExecutionError
from pydantic import ValidationError
import logging

logger=logging.getLogger(__name__)

TOOL_DEFINITIONS=[
    {
        "type":"function",
        "name":"get_run_detail",
        "description":"Get processing details for a specific product-normalizer run",
        "parameters":RunDetailArguments.model_json_schema()
    },
    {
        "type":"function",
        "name":"get_runs",
        "description":"Get processing details for some product-normalizer runs",
        "parameters":RunsArguments.model_json_schema()
    },
    {
        "type":"function",
        "name":"get_run_issues",
        "description":"Get processing issues_details for a specific product-normalizer run",
        "parameters":RunIssuesArguments.model_json_schema()
    }
]

TOOL_REGISTRY={
    "get_run_detail":get_run_detail_tool,
    "get_runs":get_runs_tool,
    "get_run_issues":get_run_issues_tool,
}

TOOL_ARGUMENT_MODELS={
    "get_run_detail":RunDetailArguments,
    "get_runs":RunsArguments,
    "get_run_issues":RunIssuesArguments,
}

def execute_tool(tool_name:str,arguments:dict):
    if tool_name not in TOOL_REGISTRY:
        logger.warning(
            "Unknown tool requested,tool_name=%s",
            tool_name
        )
        raise UnknownToolError(f"There is no tool registered with this {tool_name}")
    func=TOOL_REGISTRY[tool_name]
    arguments_model=TOOL_ARGUMENT_MODELS[tool_name]
    try:
        data = arguments_model.model_validate(arguments)
    except ValidationError as exc:
        logger.warning(
            "Invalid tool arguments,tool_name=%s",
            tool_name
        )
        raise ToolArgumentError(f"Invalid arguments for tool: {tool_name}") from exc
    data=data.model_dump()
    try:
        return func(**data)
    except Exception as exc:
        logger.error(
            "Tool execution failed,tool_name=%s,error=%s",
            tool_name,
            type(exc).__name__
        )
        raise ToolExecutionError(f"Tool execution failed: {tool_name}") from exc
