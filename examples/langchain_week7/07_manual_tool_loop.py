from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import ToolMessage,HumanMessage,AIMessage

load_dotenv()

MAX_TOOL_ROUNDS=5

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

tools=[add]
model_with_tools=model.bind_tools(tools)

tools_by_name={tool.name:tool for tool in tools}

user_input="""
"What is 17 + 25? You must use the add tool."
"""

messages=[
    HumanMessage(content=user_input)
]

for tool_call_round in range(1,MAX_TOOL_ROUNDS+1):
    response=model_with_tools.invoke(messages)
    messages.append(response)
    if not response.tool_calls:
        print(response.content)
        break
    elif tool_call_round==MAX_TOOL_ROUNDS:
        raise RuntimeError("Max tool rounds exceeded")
    else:
        for tool_call in response.tool_calls:
            tool=tools_by_name[tool_call["name"]]
            temp_result=tool.invoke(tool_call["args"])
            tool_message=ToolMessage(
                content=str(temp_result),
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)
