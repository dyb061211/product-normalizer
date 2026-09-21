from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.nodes import direct_answer
from product_normalizer.ai.workflow.state import WorkflowState

question = "你好，你能做什么？"

state: WorkflowState = {
    "messages": [HumanMessage(content=question)],
    "user_query": question,
    "route": "direct",
    "tool_rounds": 0,
    "answer": None,
    "sources": [],
    "status": "running",
    "error_type": None,
    "error_message": None,
}

result=direct_answer(state)

print("answer:", result["answer"])
print("messages:", result["messages"])