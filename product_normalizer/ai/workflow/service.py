from product_normalizer.ai.workflow.graph import build_workflow_graph
from product_normalizer.ai.workflow.state import WorkflowState
from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.schemas import WorkflowResult
from langgraph.checkpoint.memory import InMemorySaver
from product_normalizer.ai.workflow.context import build_model_context

workflow_graph = build_workflow_graph()
checkpointer = InMemorySaver()
memory_workflow_graph = build_workflow_graph(
    checkpointer=checkpointer
)

def run_workflow(question:str)->WorkflowResult:
    initial_state:WorkflowState={
        "messages": [HumanMessage(content=question)],
        "user_query": question,
        "route": None,
        "tool_rounds": 0,
        "answer": None,
        "sources": [],
        "status": "running",
        "error_type": None,
        "error_message": None
    }
    final_state=workflow_graph.invoke(initial_state)
    return WorkflowResult(
        answer=final_state["answer"],
        route=final_state["route"],
        sources=final_state["sources"],
        status=final_state["status"]
    )

def run_workflow_with_memory(question:str,thread_id:str)->WorkflowResult:
    initial_state: WorkflowState = {
        "messages": [HumanMessage(content=question)],
        "user_query": question,
        "route": None,
        "tool_rounds": 0,
        "answer": None,
        "sources": [],
        "status": "running",
        "error_type": None,
        "error_message": None
    }
    config={
        "configurable":{
            "thread_id":thread_id
        }
    }
    final_state=memory_workflow_graph.invoke(
        initial_state,
        config
    )
    return WorkflowResult(
        answer=final_state["answer"],
        route=final_state["route"],
        sources=final_state["sources"],
        status=final_state["status"]
    )

