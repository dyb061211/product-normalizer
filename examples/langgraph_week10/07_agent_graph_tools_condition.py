from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    SystemMessage,
)

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv()


# =========================
# 1. Tool
# =========================

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers
    and return the sum
    """
    return a + b


tools = [add]


# =========================
# 2. Model
# =========================

model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
)

model_with_tools = model.bind_tools(tools)


# =========================
# 3. State
# =========================

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# =========================
# 4. LLM Node
# =========================

def llm_node(state: State):
    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =========================
# 5. 官方 ToolNode
# =========================

tool_node = ToolNode(tools)


# =========================
# 6. Graph
# =========================

builder = StateGraph(State)

builder.add_node("llm", llm_node)

# 注意这里最好叫 "tools"
# 因为 tools_condition 有 tool_calls 时默认返回 "tools"
builder.add_node("tools", tool_node)

builder.add_edge(
    START,
    "llm"
)

builder.add_conditional_edges(
    "llm",
    tools_condition
)

builder.add_edge(
    "tools",
    "llm"
)

graph = builder.compile()


# =========================
# 7. Initial State
# =========================

initial_state: State = {
    "messages": [
        SystemMessage(
            content="你是一个工具调用助手，需要计算时使用提供的工具。"
        ),
        HumanMessage(
            content="2+3=?"
        ),
    ]
}


# =========================
# 8. Run
# =========================

result = graph.invoke(initial_state)

print("最终回答：")
print(result["messages"][-1].content)

print("\n完整消息流：")

for message in result["messages"]:
    print(type(message))
    print(message)