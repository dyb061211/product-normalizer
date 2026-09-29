import asyncio
from mcp import Client
from product_normalizer.mcp_server.server import mcp

async def main():
    async with Client(mcp) as client:
        result = await client.list_tools()
        resources=await client.list_resources()
        resource_result=await client.read_resource("project://overview")
        templates=await client.list_resource_templates()
        summary = await client.read_resource("run://64/summary")
        prompts=await client.list_prompts()
        print(prompts)
        prompt_result=await client.get_prompt(
            "explain_run",
            {
                "run_id":"64",
                "issue_text":"This validation issue count is unusually high."
            }
        )
        print(prompt_result)
asyncio.run(main())