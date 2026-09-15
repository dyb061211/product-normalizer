from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

load_dotenv()

prompt=ChatPromptTemplate(
    [
        ("system","You are a Python teacher.Answer briefly"),
        ("human","Explain {topic} in Python and give one example")
    ]
)

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

parser=StrOutputParser()

chain=prompt | model | parser
response=chain.invoke(
    {"topic":"dict"}
)

print(type(prompt))
print(type(model))
print(type(parser))
print(type(chain))
print(type(response))
print(response)