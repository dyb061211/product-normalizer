from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.nodes import rag_answer
from product_normalizer.ai.workflow.state import WorkflowState

question = "这个项目2028年的年度营收目标是多少？"

state: WorkflowState = {
    "messages": [HumanMessage(content=question)],
    "user_query": question,
    "route": "rag",
    "tool_rounds": 0,
    "answer": None,
    "sources": [],
    "status": "running",
    "error_type": None,
    "error_message": None,
}

result=rag_answer(state)
print(result["answer"])
print(result["status"])
print(result["sources"])