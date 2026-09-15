from unittest.mock import Mock
import httpx
from openai import APITimeoutError

from ai.client import LLMClient

request = httpx.Request(
    "POST",
    "https://api.deepseek.com/responses"
)

error1 = APITimeoutError(request=request)
error2 = APITimeoutError(request=request)

fake_response = Mock()
fake_response.usage.input_tokens = 100
fake_response.usage.output_tokens = 50
fake_response.usage.total_tokens = 150

llm_client = LLMClient(
    max_attempts=3
)

llm_client.client.responses.create = Mock(
    side_effect=[
        error1,
        error2,
        fake_response
    ]
)

response = llm_client.create_response(
    instructions="test",
    input_text="test",
    text={}
)

print(response)
print(llm_client.client.responses.create.call_count)