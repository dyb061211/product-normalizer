import asyncio
from mcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tool_result=await client.list_tools()
        print("=== TOOLS ===")
        for tool in tool_result.tools:
            print(tool.name)
        runs_result=await client.call_tool(
            "get_runs",
            {"limit":"3"}
        )
        print("=== GET RUNS ===")
        print(runs_result.content)
        detail_result = await client.call_tool(
            "get_run_detail",
            {"run_id": 64}
        )
        print("=== GET RUN DETAIL ===")
        print(detail_result.content)
        resources_result=await client.list_resources()
        print("=== RESOURCES ===")
        for resource in resources_result.resources:
            print(resource.uri)
        resource_result=await client.read_resource("project://overview")
        print("=== PROJECT OVERVIEW ===")
        print(resource_result.contents)
        prompts_result=await client.list_prompts()
        print("=== PROMPTS ===")
        for prompt in prompts_result.prompts:
            print(prompt.name)
        prompt_result=await client.get_prompt(
            "explain_run",
            {
                "run_id": "64",
                "issue_text": "This validation issue count is unusually high."
            }
        )
        print("=== EXPLAIN RUN PROMPT ===")
        print(prompt_result.messages)
asyncio.run(main())