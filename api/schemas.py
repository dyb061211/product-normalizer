from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    sku:str
    product_name:str
    price:float

class RAGQueryRequest(BaseModel):
    question:str=Field(min_length=1)