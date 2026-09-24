from langchain_core.messages import AnyMessage,trim_messages

def build_model_context(messages:list[AnyMessage],max_tokens:int=200)->list[AnyMessage]:
    return trim_messages(
        messages,
        max_tokens=max_tokens,
        token_counter="approximate",
        strategy="last",
        start_on="human",
        allow_partial=False
    )
