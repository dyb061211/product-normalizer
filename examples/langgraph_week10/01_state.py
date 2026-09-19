from typing_extensions import TypedDict

class State(TypedDict):
    value:int

state:State={
    "value":10
}

print(type(state))
print(type(state["value"]))
print(state["value"])
print(state)