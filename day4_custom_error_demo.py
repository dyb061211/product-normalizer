from ai.client import LLMClient
from ai.prompts import SYSTEM_PROMPT, build_listing_prompt
from ai.schemas import GeneratedListing, ProductInput
from product_normalizer.logging_config import setup_logging

setup_logging()


listing_schema=GeneratedListing.model_json_schema()
text={
    "format":{
        "type":"json_schema",
        "name":"generated_listing",
        "schema":listing_schema
    }
}

product = ProductInput(
    sku="A001",
    title="Portable Camping Chair",
    color="Green",
    category="Outdoor",
    price=29.99
)
user_prompt = build_listing_prompt(product)

llm_client = LLMClient(
    base_url="https://definitely-not-exist-123456.invalid",
    timeout=30.0,
)
llm_client.create_response(
    instructions=SYSTEM_PROMPT,
    input_text=user_prompt,
    text=text
)