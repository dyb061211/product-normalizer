from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    score:int
    result:str

def route_result(state:State):
    if state["score"]>=60:
        return "pass_node"
    else:
        return "fail_node"

def pass_node(state:State):
    return {
        "result":"success"
    }

def fail_node(state:State):
    return {
        "result":"fail"
    }

def check(state:State):
    return {}

builder=StateGraph(State)
builder.add_node("check",check)
builder.add_node("pass_node",pass_node)
builder.add_node("fail_node",fail_node)
builder.add_edge(START,"check")
builder.add_conditional_edges(
    "check",
    route_result
)
builder.add_edge("pass_node", END)
builder.add_edge("fail_node", END)

graph=builder.compile()

state:State={
    "score":60,
    "result":""
}

result=graph.invoke(state)
print(result)

