from langchain_core.messages import HumanMessage
from product_normalizer.ai.workflow.state import WorkflowState

question="run 6有什么问题"

initial_state:WorkflowState={
    "messages":[HumanMessage(content=question)],
    "user_query":question,
    "route":None,
    "tool_rounds":0,
    "answer":None,
    "sources":[],
    "status":"running",
    "error_type":None,
    "error_message":None
}

print(initial_state)