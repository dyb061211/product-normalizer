from typing import TypedDict,Annotated
from langchain_core.messages import AnyMessage,HumanMessage,AIMessage
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

state:State={
    "messages":[]
}

def chat(state:State):
    response = model.invoke(state["messages"])
    return {
        "messages": [response]
    }

builder=StateGraph(State)
builder.add_node("chat",chat)
builder.add_edge(START,"chat")
builder.add_edge("chat",END)

checkpointer=InMemorySaver()
graph=builder.compile(
    checkpointer=checkpointer
)

config={
    "configurable":{
        "thread_id":"A"
    }
}

config_b = {
    "configurable": {
        "thread_id": "B"
    }
}

response1=graph.invoke(
    {
        "messages": [
            HumanMessage(content="My name is Tom.")
        ]
    },
    config=config
)

snapshot1=graph.get_state(config)
print(type(snapshot1))
print(snapshot1.values)
print(snapshot1.config)
print(snapshot1.next)

response2 = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name?")
        ]
    },
    config=config
)

snapshot2 = graph.get_state(config)

print(snapshot2.values)

response3 = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name?")
        ]
    },
    config=config_b
)



