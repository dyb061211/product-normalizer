from openai import OpenAI

client=OpenAI(
    api_key="wrong-key",
    base_url="https://api.deepseek.com",
    timeout=30.0
)

response=client.responses.create(
    model="deepseek-v4-flash",
    input="return hello"
)