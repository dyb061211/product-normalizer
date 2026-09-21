from product_normalizer.ai.workflow.state import WorkflowState,Route

MAX_TOOL_ROUNDS=3

def route_by_request(state:WorkflowState)->Route:
    route=state["route"]
    if route is None:
        raise ValueError("Rout has not been decided")
    return route

def should_continue_tools(state:WorkflowState):
    last_message=state["messages"][-1]
    if not last_message.tool_calls:
        return "finalize"
    elif state["tool_rounds"]>=MAX_TOOL_ROUNDS:
        return "max_rounds"
    return "tools"