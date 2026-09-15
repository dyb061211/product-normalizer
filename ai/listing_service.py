from ai.client import LLMClient
from ai.prompts import SYSTEM_PROMPT,build_listing_prompt
from ai.schemas import GeneratedListing,ProductInput
from ai.exceptions import LLMOutputError
import json
from pydantic import ValidationError

def generate_listing(product:ProductInput)->GeneratedListing:
    user_prompt=build_listing_prompt(product)
    llm_client=LLMClient()
    listing_schema=GeneratedListing.model_json_schema()
    text={
        "format":{
            "type":"json_schema",
            "name":"generated_listing",
            "schema":listing_schema
        }
    }
    response=llm_client.create_response(
        instructions=SYSTEM_PROMPT,
        input_text=user_prompt,
        text=text
    )
    try:
        data = json.loads(response.output_text)
        result = GeneratedListing.model_validate(data)
    except (json.JSONDecodeError,ValidationError) as exc:
        raise LLMOutputError("Invalid LLM output") from exc
    return result


