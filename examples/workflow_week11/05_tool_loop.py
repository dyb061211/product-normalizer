from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.nodes import tool_llm,tool_node,increment_tool_round
from product_normalizer.ai.workflow.routers import should_continue_tools
from product_normalizer.ai.workflow.state import WorkflowState
from langgraph.runtime import Runtime

question="run 6 有什么问题"

state:WorkflowState={
    "messages":[HumanMessage(content=question)],
    "user_query":question,
    "tool_rounds":0,
    "error_type":None,
    "error_message":None,
    "sources":[],
    "status":"running",
    "route":"tools",
    "answer":None
}

first_update=tool_llm(state)
first_ai_message=first_update["messages"][0]
print("第一次调用llm")
print(first_ai_message)
print("tool_calls:", first_ai_message.tool_calls)

state["messages"].append(first_ai_message)

next_step=should_continue_tools(state)
print(next_step)

round_update = increment_tool_round(state)
state["tool_rounds"] = round_update["tool_rounds"]
print("tool_rounds:", state["tool_rounds"])

tool_update = tool_node.invoke(
    state,
    runtime=Runtime()
)
print("ToolNode返回:")
print(tool_update)

state["messages"].extend(tool_update["messages"])

for message in state["messages"]:
    print(type(message))

second_update = tool_llm(state)
second_ai_message = second_update["messages"][0]
state["messages"].append(second_ai_message)
print("第二次 LLM:")
print(second_ai_message)
print("tool_calls:", second_ai_message.tool_calls)

print(
    "next_step:",
    should_continue_tools(state)
)