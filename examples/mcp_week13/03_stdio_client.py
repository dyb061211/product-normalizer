import asyncio
from mcp import Client,StdioServerParameters
from pathlib import Path

project_root=Path(__file__).resolve().parents[2]

server_params=StdioServerParameters(
    command=str(project_root/".venv/bin/mcp"),
    args=[
        "run",
        "product_normalizer/mcp_server/server.py"
    ],
    cwd=project_root
)

async def main():
    async with Client(server_params) as client:
        result=await client.list_tools()
        print(result)
        for tool in result.tools:
            print(tool.name)
        call_result=await client.call_tool(
            "get_run_detail",
            {"run_id":"64"}
        )
        print(call_result.is_error)
        print(call_result.content)

asyncio.run(main())