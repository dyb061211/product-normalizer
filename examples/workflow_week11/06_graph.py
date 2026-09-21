# from product_normalizer.ai.workflow.state import WorkflowState
# from product_normalizer.ai.workflow.graph import build_workflow_graph
# from langchain_core.messages import HumanMessage
#
# def make_state(question: str) -> WorkflowState:
#     return {
#         "messages": [HumanMessage(content=question)],
#         "user_query": question,
#         "route": None,
#         "tool_rounds": 0,
#         "answer": None,
#         "sources": [],
#         "status": "running",
#         "error_type": None,
#         "error_message": None,
#     }
#
# graph = build_workflow_graph()
#
# question= "run 6有什么问题？"
# result=graph.invoke(make_state(question))
# print("route:", result["route"])
# print("status:", result["status"])
# print("answer:", result["answer"])
# print("sources:", result["sources"])
# print("tool_rounds:", result["tool_rounds"])
#
# print("\nmessages:")
# for message in result["messages"]:
#     print(type(message).__name__)

from product_normalizer.ai.workflow.service import run_workflow


result = run_workflow("run 6有什么问题？")

print(result)
print(type(result))