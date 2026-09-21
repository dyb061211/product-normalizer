from langgraph.graph import START,END,StateGraph
from product_normalizer.ai.workflow.nodes import route_request,direct_answer,rag_answer,increment_tool_round,tool_llm,finalize,max_rounds_error,tool_node
from product_normalizer.ai.workflow.routers import route_by_request,should_continue_tools
from product_normalizer.ai.workflow.state import WorkflowState

def build_workflow_graph():
    builder=StateGraph(WorkflowState)
    builder.add_node("route_request",route_request)
    builder.add_node("direct_answer",direct_answer)
    builder.add_node("rag_answer",rag_answer)
    builder.add_node("increment_tool_round",increment_tool_round)
    builder.add_node("tool_llm",tool_llm)
    builder.add_node("finalize",finalize)
    builder.add_node("max_rounds_error",max_rounds_error)
    builder.add_node("tools",tool_node)
    builder.add_edge(START,"route_request")
    builder.add_conditional_edges(
        "route_request",
        route_by_request,
        {
            "direct":"direct_answer",
            "tools":"tool_llm",
            "rag":"rag_answer"
        }
    )
    builder.add_edge("direct_answer","finalize")
    builder.add_edge("rag_answer","finalize")
    builder.add_conditional_edges(
        "tool_llm",
        should_continue_tools,
        {
            "max_rounds":"max_rounds_error",
            "finalize":"finalize",
            "tools":"increment_tool_round"
        }
    )
    builder.add_edge("increment_tool_round","tools")
    builder.add_edge("tools","tool_llm")
    builder.add_edge("max_rounds_error","finalize")
    builder.add_edge("finalize",END)
    return builder.compile()