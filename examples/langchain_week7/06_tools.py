from langchain.tools import tool
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

@tool
def add(a:int,b:int)->int:
    """
    Add two integers
    and return the sum
    """
    return a+b

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

toools=[add]
model_with_tools=model.bind_tools(toools)

response = model_with_tools.invoke(
    "What is 17 + 25? You must use the add tool."
)
print(response)
print(type(response))
print(response.content)
print(response.tool_calls)
tool_call = response.tool_calls[0]

print(type(response.tool_calls))
print(type(tool_call))

print(tool_call["name"])
print(tool_call["args"])
print(tool_call["id"])
print(tool_call["type"])

result=add.invoke(tool_call["args"])
print(result)
print(type(result))