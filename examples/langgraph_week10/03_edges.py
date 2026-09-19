from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    number:int
    name:str

state:State={
    "number":10,
    "name":"dyb"
}

def increment(state:State):
    return {
        "number":state["number"]+1
    }

def double(state:State):
    return {
        "number":state["number"]*2
    }

builder=StateGraph(State)
builder.add_node("increment",increment)
builder.add_node("double",double)
builder.add_edge(START,"increment")
builder.add_edge("increment","double")
builder.add_edge("double",END)

graph=builder.compile()

result=graph.invoke(state)
print(state)
print(result)
print(type(result))
print(type(builder))
print(type(graph))