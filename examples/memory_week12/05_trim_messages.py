from langchain_core.messages import trim_messages,HumanMessage,AIMessage,ToolMessage

messages=[
    HumanMessage(content="message 1"),
    AIMessage(content="reply 1"),
    HumanMessage(content="message 2"),
    AIMessage(content="reply 2"),
    HumanMessage(content="message 3"),
    AIMessage(content="reply 3"),
]

tool_messages=[
    HumanMessage(content="Please check run 6"),
    AIMessage(
        content="",
        tool_calls=[
            {
                "name":"get_run_detail",
                "args":{"run_id":6},
                "id":"call_1",
                "type":"tool_call"
            }
        ]
    ),
    ToolMessage(
        content="run 6 status is success",
        tool_call_id="call_1"
    ),
    AIMessage(
        content="Run 6 completed successfully."
    ),
    HumanMessage(content="Thanks."),
    AIMessage(content="You're welcome.")
]

trimmed_messages=trim_messages(
    messages,
    max_tokens=20,
    token_counter="approximate",
    strategy="last"
)

trimmed_tool_messages=trim_messages(
    tool_messages,
    max_tokens=40,
    token_counter="approximate",
    strategy="last",
    start_on="human"
)


bad_messages=tool_messages[-4:]

for message in bad_messages:
    print(type(message).__name__, message.content)

print("="*30)

for message in trimmed_tool_messages:
    print(type(message).__name__, message.content)