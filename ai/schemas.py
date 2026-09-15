from pydantic import BaseModel,Field

class ProductInput(BaseModel):
    sku:str=Field(min_length=1)
    title:str=Field(min_length=1)
    color:str=Field(min_length=1)
    category:str=Field(min_length=1)
    price:float=Field(ge=0)

class GeneratedListing(BaseModel):
    sku:str
    listing_title:str
    bullet_points:list[str]=Field(min_length=3,max_length=3)
    description:str

class RunDetailArguments(BaseModel):
    run_id:int=Field(gt=0)

class RunIssuesArguments(BaseModel):
    run_id: int = Field(gt=0)

class RunsArguments(BaseModel):
    limit: int = Field(gt=0)

class AgentRequest(BaseModel):
    message:str=Field(min_length=1)
    
class AgentResponse(BaseModel):
    answer:str

