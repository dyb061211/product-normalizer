import os
from dotenv import load_dotenv
import time
from openai import OpenAI
from ai.schemas import RunDetailArguments
from ai.tool_registry import TOOL_DEFINITIONS

load_dotenv()

client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response=client.responses.create(
    model="deepseek-v4-flash",
    input="帮我查看 run 6",
    tools=TOOL_DEFINITIONS,
    tool_choice="auto"
)
for item in response.output:
    if item.type=="function_call":
        ans=RunDetailArguments.model_validate_json(item.arguments)
        print(ans.model_dump())
        print(type(ans.model_dump()))
        break