import asyncio
from mcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result=await client.list_tools()
        for tool in result.tools:
            print(tool.name)
        call_result = await client.call_tool(
            "get_run_detail",
            {"run_id": 64}
        )
        print("is_error:", call_result.is_error)
        print("content:", call_result.content)

asyncio.run(main())