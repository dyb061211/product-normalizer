from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict,Annotated
from langchain_core.messages import AnyMessage,HumanMessage,AIMessage
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END

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

root_path=Path(__file__).parent.parent.parent
print(root_path)
checkpoint_dir=root_path/"data"/"checkpoints"
checkpoint_dir.mkdir(parents=True,exist_ok=True)
dp_path=checkpoint_dir/"workflow_checkpoints.sqlite"

config={
    "configurable":{
        "thread_id":"memory-test"
    }
}

with SqliteSaver.from_conn_string(str(dp_path)) as checkpointer:
    graph=builder.compile(
        checkpointer=checkpointer
    )
    # response=graph.invoke(
    #     {
    #         "messages":[
    #             HumanMessage(content="My favorite programming language is Python.")
    #         ]
    #     },
    #     config=config
    # )
    response = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is my favorite programming language?"
                )
            ]
        },
        config=config
    )

    print(response["messages"][-1].content)