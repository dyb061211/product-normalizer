from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()


model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"

)

response=model.invoke(
    input="用一句话解释什么是API"
)

print(response)
print(response.content)
print(type(response))
print(response.response_metadata)
print(response.usage_metadata)
print(type(response.content))
print(type(response.response_metadata))
print(type(response.usage_metadata))