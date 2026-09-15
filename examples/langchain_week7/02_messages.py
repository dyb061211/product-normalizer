from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,SystemMessage

load_dotenv()

messages=[
    SystemMessage(content="you are my python teacher"),
    HumanMessage(content="what is list")
]

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

response=model.invoke(messages)
messages.append(response)
messages.append(HumanMessage(content="What is the difference between it and tuple? Answer in three points."))
second_response=model.invoke(messages)

short_messages=[
    ("system","You are my Python teacher,answer briefly"),
    ("human","What is dictionary in Python?")
]
print(short_messages[0])
short_response = model.invoke(short_messages)
print(short_response.content)
print(type(short_response))
