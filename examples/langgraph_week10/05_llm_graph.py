from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,AIMessage,AnyMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model=init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek"
    )

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

def llm_node(state:State):
    response=model.invoke(state["messages"])
    return {
        "messages":[
            response
        ]
    }

builder=StateGraph(State)
builder.add_node("llm",llm_node)
builder.add_edge(START,"llm")
builder.add_edge("llm",END)

graph=builder.compile()

initial_state:State={
    "messages":[HumanMessage(content="Hello!")]
}

result=graph.invoke(initial_state)

for message in result["messages"]:
    print(message)
    print(type(message))