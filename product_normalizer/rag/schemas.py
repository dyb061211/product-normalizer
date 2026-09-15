from pydantic import BaseModel

class RAGSource(BaseModel):
    filename:str
    source:str

class RAGResponse(BaseModel):
    answer:str
    sources:list[RAGSource]
