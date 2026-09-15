from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a product listing assistant."),
        (
            "human",
            "Title: {title}\n"
            "Color: {color}\n"
            "Category: {category}"
        ),
    ]
)

def test_prompt_variables_are_formatted():
    formatted = prompt.invoke(
        {
            "title": "Folding Chair",
            "color": "Black",
            "category": "Outdoor Furniture",
        }
    )
    human_message = formatted.messages[1]
    assert "Folding Chair" in human_message.content
    assert "Black" in human_message.content
    assert "Outdoor Furniture" in human_message.content


def test_prompt_input_variables():
    assert "title" in prompt.input_variables
    assert "color" in prompt.input_variables
    assert "category" in prompt.input_variables