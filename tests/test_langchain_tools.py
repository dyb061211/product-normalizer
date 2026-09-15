from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

def test_add_tool_schema():
    schema=add.args_schema.model_json_schema()
    assert "a" in schema["properties"]
    assert "b" in schema["properties"]
    assert schema["properties"]["a"]["type"] == "integer"
    assert add.name == "add"
    assert add.description == "Add two integers and return the sum."

def test_add_tool_invoke():
    assert add.invoke({"a":1,"b":2})==3