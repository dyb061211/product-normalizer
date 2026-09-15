import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key=os.getenv("DEEPSEEK_API_KEY")

client=OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response=client.responses.create(
    model="deepseek-v4-flash",
    input="Return exactly the word hello"
)
print(response.output_text)
print(response.usage)
print(type(response))