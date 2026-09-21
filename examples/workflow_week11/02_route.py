from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.nodes import route_request
from product_normalizer.ai.workflow.state import WorkflowState


def make_state(question: str) -> WorkflowState:
    return {
        "messages": [HumanMessage(content=question)],
        "user_query": question,
        "route": None,
        "tool_rounds": 0,
        "answer": None,
        "sources": [],
        "status": "running",
        "error_type": None,
        "error_message": None,
    }


questions = [
    "你好",
    "run 6有什么问题？",
    "MAX_TOOL_ROUNDS是多少？",
]

for question in questions:
    state = make_state(question)

    result = route_request(state)

    print("question:", question)
    print("route:", result["route"])
    print("-" * 30)

from product_normalizer.ai.workflow.routers import route_by_request

state = make_state("run 6有什么问题？")

update = route_request(state)

state["route"] = update["route"]

print(route_by_request(state))