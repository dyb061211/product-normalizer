from pydantic import BaseModel
from typing import Literal
from product_normalizer.rag.schemas import RAGSource

class RouteDecision(BaseModel):
    route:Literal["direct", "tools", "rag"]

class WorkflowResult(BaseModel):
    answer:str
    route:Literal["direct", "tools", "rag"]
    sources: list[RAGSource]
    status: Literal[
        "success",
        "no_answer",
        "error",
    ]