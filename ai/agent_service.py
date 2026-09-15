import json
from ai.client import LLMClient
from ai.tool_registry import execute_tool,TOOL_DEFINITIONS
from ai.exceptions import AgentMaxRoundsError
import logging
import time

logger=logging.getLogger(__name__)

MAX_TOOL_ROUNDS=3

def run_agent(message:str):
    agent_start_time=time.perf_counter()
    agent_input=[
        {
            "role":"user",
            "content":message
        }
    ]
    tool_rounds=0
    llm_client = LLMClient()
    while True:
        response = llm_client.create_response(
            input_text=agent_input,
            instructions="你是 product-normalizer assistant，需要数据库信息时使用提供的 tools，每一轮最多调用一个工具，"
                         "如果需要多个工具，请先调用当前步骤所需的工具，等获得结果后再决定下一步。",
            text=None,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            reasoning={"effort": "none"}
        )
        tool_call=None
        for item in response.output:
            if item.type=="function_call":
                tool_call=item
                break
        if tool_call is None:
            total_elapsed=time.perf_counter()-agent_start_time
            logger.info(
                "Agent finished,tool_rounds=%s,elapsed=%.2f",
                tool_rounds,
                total_elapsed,
            )
            return response.output_text
        if tool_rounds >= MAX_TOOL_ROUNDS:
            tool_elapsed=time.perf_counter()-agent_start_time
            logger.error(
                "Agent exceeded max tool rounds,tool_rounds=%s,elapsed=%.2f",
                tool_rounds,
                tool_elapsed
            )
            raise AgentMaxRoundsError("The maximum number of rounds has been reached")
        if tool_call:
            data = json.loads(tool_call.arguments)
            tool_start_time=time.perf_counter()
            result = execute_tool(tool_call.name, data)
            tool_elapsed=time.perf_counter()-tool_start_time
            logger.info(
                "Agent tool executed,round=%s,tool_name=%s,elapsed=%.2f",
                tool_rounds + 1,
                tool_call.name,
                tool_elapsed,
            )
            agent_input.append(
                {
                    "type": "function_call",
                    "call_id": tool_call.call_id,
                    "name": tool_call.name,
                    "arguments": tool_call.arguments

                }
            )
            agent_input.append(
                {
                    "type": 'function_call_output',
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result, ensure_ascii=False)
                }
            )
            tool_rounds += 1