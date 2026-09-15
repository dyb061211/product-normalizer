from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from ai.schemas import GeneratedListing

load_dotenv()

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

message="""
SKU: SKU-001
Title: Portable Folding Chair
Color: Black
Category: Outdoor Furniture
Price: 39.99

Generate an ecommerce listing for this product.
"""

structured_model=model.with_structured_output(
    GeneratedListing
)

structured_model_with_raw=model.with_structured_output(
    GeneratedListing,
    include_raw=True
)

raw_result=structured_model_with_raw.invoke(message)
print(type(raw_result))
print(raw_result.keys())
print(type(raw_result["raw"]))
print(type(raw_result["parsed"]))
print(type(raw_result["parsing_error"]))
print(raw_result["parsed"])
print(raw_result["parsing_error"])