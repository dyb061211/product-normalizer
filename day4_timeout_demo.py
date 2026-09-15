from openai import OpenAI

client=OpenAI(
    api_key="wrong-key",
    base_url="https://api.deepseek.com",
    timeout=0.001
)

response=client.responses.create(
    model="deepseek-v4-flash",
    input="return hello"
)