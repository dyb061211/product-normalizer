# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from ai.prompts import SYSTEM_PROMPT,build_listing_prompt
#
# load_dotenv()
# api_key=os.getenv("DEEPSEEK_API_KEY")
#
# client=OpenAI(
#     api_key=api_key,
#     base_url="https://api.deepseek.com",
# )
#
# user_prompt=build_listing_prompt(
#     sku="A001",
#     title="Portable Camping Chair",
#     color="Green",
#     category="Outdoor",
#     price=29.99
# )
#
# response=client.responses.create(
#     model="deepseek-v4-flash",
#     instructions=SYSTEM_PROMPT,
#     input=user_prompt,
# )
# print(response.output_text)