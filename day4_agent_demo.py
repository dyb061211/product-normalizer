from ai.agent_service import run_agent
from product_normalizer.logging_config import setup_logging

setup_logging()

print(
    run_agent(
        "帮我找到最近一次失败的处理记录，并告诉我具体错误"
    )
)