from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a Python teacher.Answer briefly."),
        ("human","Explain {topic} in Python and give one example.")
    ]
)

formatted_prompt=prompt.invoke(
    {"topic":"list"}
)
print(type(prompt))
print(type(formatted_prompt))

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

chain=prompt|model
response=chain.invoke(
    {"topic":"list"}
)
# print(response.content)
# print(type(response))
