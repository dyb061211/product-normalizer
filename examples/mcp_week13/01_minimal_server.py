from mcp.server import MCPServer

mcp=MCPServer("Demo")

@mcp.tool()
def add(a:int,b:int)->int:
    """
    Return the sum of two numbers.
    """
    return a+b