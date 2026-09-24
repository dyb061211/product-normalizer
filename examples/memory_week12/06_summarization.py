from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

old_messages = [
    HumanMessage(content="My project is product-normalizer."),
    AIMessage(content="Got it."),

    HumanMessage(content="The project uses Python."),
    AIMessage(content="Understood."),

    HumanMessage(content="I am learning AI Agent engineering."),
    AIMessage(content="Okay."),
]

summary_prompt="""
把下面历史压缩成简短 conversation summary。

保留对未来对话可能重要的信息。
不要回答对话中的问题。
只总结已有信息。
"""
summary_messages = [
    SystemMessage(content=summary_prompt),
    *old_messages,
]

model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

response=model.invoke(
    summary_messages
)

recent_messages = [
    HumanMessage(
        content="What programming language does my project use?"
    )
]

context_messages=[
    SystemMessage(
        content=f"""
    Conversation summary:
    {response.content}
    """
    ),
    *recent_messages
]

final_response = model.invoke(context_messages)
print(final_response.content)