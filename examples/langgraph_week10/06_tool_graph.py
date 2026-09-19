from langgraph.graph import StateGraph,START,END
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage,AIMessage,AnyMessage,ToolMessage,SystemMessage
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.graph.message import add_messages

load_dotenv()

MAX_TOOL_ROUNDS=3

@tool
def add(a:int,b:int)->int:
    """
    Add two integers
    and return the sum
    """
    return a+b

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

tools=[add]
model_with_tools=model.bind_tools(tools)
tool_by_names={tool.name:tool for tool in tools}

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    tool_rounds:int
    is_get_answer:int

def should_continue(state:State):
    last_message=state["messages"][-1]
    if not last_message.tool_calls:
        return "get_answer_node"
    elif state["tool_rounds"]>=MAX_TOOL_ROUNDS:
        return END
    else :
        return "tool_node"

def tool_node(state:State):
    last_message=state["messages"][-1]
    tool_calls=last_message.tool_calls
    temp_message=[]
    for tool_call in tool_calls:
        tool=tool_by_names[tool_call["name"]]
        temp_response=tool.invoke(tool_call["args"])
        tool_message=ToolMessage(
            content=str(temp_response),
            tool_call_id=tool_call["id"]
        )
        temp_message.append(tool_message)
    return {
        "messages":temp_message,
        "tool_rounds": state["tool_rounds"] + 1
    }

def llm_node(state:State):
    response=model_with_tools.invoke(state["messages"])
    return {
        "messages":[response]
    }

def get_answer_node(state:State):
    return {
        "is_get_answer":1
    }


initial_state:State={
    "messages":[
        SystemMessage(content="你是tool调用助手，需要对应信息时使用提供的 tools，每一轮最多调用一个工具，"
                         "如果需要多个工具，请先调用当前步骤所需的工具，等获得结果后再决定下一步。"),
        HumanMessage(content="2+3=?")
    ],
    "tool_rounds":0,
    "is_get_answer":0
}

builder=StateGraph(State)
builder.add_node("tool_node",tool_node)
builder.add_node("get_answer_node",get_answer_node)
builder.add_node("llm_node",llm_node)
builder.add_edge(START,"llm_node")
builder.add_conditional_edges(
    "llm_node",
    should_continue
)
builder.add_edge("get_answer_node",END)
builder.add_edge("tool_node","llm_node")

graph=builder.compile()

result=graph.invoke(initial_state)
if result["is_get_answer"]:
    print(result["messages"][-1].content)
else :
    print("Tool rounds exceeded the maximum number of tool rounds")

for message in result["messages"]:
    print(type(message))
    print(message)

print("tool_rounds =", result["tool_rounds"])
