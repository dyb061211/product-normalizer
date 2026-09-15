from ai.prompts import SYSTEM_PROMPT,build_listing_prompt
import json
from ai.schemas import GeneratedListing,ProductInput
from ai.client import LLMClient


product=ProductInput(
    sku="A001",
    title="Portable Camping Chair",
    color="Green",
    category="Outdoor",
    price=29.99
)

print(type(product))
print(product.price)

user_prompt=build_listing_prompt(
    product
)

listing_schema=GeneratedListing.model_json_schema()
text={
    "format":{
        "type":"json_schema",
        "name":"generated_listing",
        "schema":listing_schema
    }
}

llmclient=LLMClient()
response=llmclient.create_response(
    SYSTEM_PROMPT,
    text,
    user_prompt
)

print(response.output_text)
print(type(response.output_text))

data=json.loads(response.output_text)
print(type(data))

listing=GeneratedListing.model_validate(data)
print(type(listing))
print(listing.listing_title)
print(listing.bullet_points)