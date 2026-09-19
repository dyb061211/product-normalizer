from typing_extensions import TypedDict

class State(TypedDict):
    number:int
    name:str

state:State={
    "number":10,
    "name":"dyb"
}

def increment(state:State):
    temp=state["number"]+1
    return {
        "number":temp,
    }

result1 = increment(state)
print(state)
print(result1)

def double(state:State):
    temp=state["number"]*2
    return {
        "number":temp,
    }

result2=double(state)
print(state)
print(result2)