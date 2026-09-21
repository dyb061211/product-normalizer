from typing import Annotated,TypedDict,Literal
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from product_normalizer.rag.schemas import RAGSource

Route=Literal["direct","tools","rag"]

WorkflowStatus=Literal[
    "running",
    "success",
    "no_answer",
    "error"
]

class WorkflowState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    user_query:str
    route:Route|None
    tool_rounds:int
    answer:str|None
    sources:list[RAGSource]
    status:WorkflowStatus
    error_type:str|None
    error_message:str|None





