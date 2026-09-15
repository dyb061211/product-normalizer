from openai import OpenAI,AuthenticationError,APITimeoutError,APIConnectionError,InternalServerError,RateLimitError
import os
from dotenv import load_dotenv
from ai.exceptions import LLMConnectionError,LLMAuthenticationError
import time
import logging

logger=logging.getLogger(__name__)
load_dotenv()

class LLMClient:
    def __init__(self,api_key=None,timeout=None,base_url=None,max_attempts=3):
        if max_attempts<1:
            raise ValueError("max_attempts must be at least 1")
        self.api_key=os.getenv("DEEPSEEK_API_KEY") if api_key is None else api_key
        self.base_url="https://api.deepseek.com" if base_url is None else base_url
        self.model="deepseek-v4-flash"
        self.timeout=30.0 if timeout is None else timeout
        self.max_attempts=max_attempts
        self.client=OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=0
        )

    def create_response(self,instructions,text,input_text,tools=None,tool_choice=None,reasoning=None):
        request_start_time=time.perf_counter()
        for attempt in range(1,self.max_attempts+1):
            try:
                start_time=time.perf_counter()
                request_kwargs={
                    "model":self.model,
                    "instructions":instructions,
                    "input":input_text
                }
                if text is not None:
                    request_kwargs["text"]=text
                if tools is not None:
                    request_kwargs["tools"]=tools
                if tool_choice is not None:
                    request_kwargs["tool_choice"]=tool_choice
                if reasoning is not None:
                    request_kwargs["reasoning"] = reasoning
                response = self.client.responses.create(**request_kwargs)
                total_elapsed = time.perf_counter() - request_start_time
                logger.info(
                    "LLM succeeded,model=%s,elapsed=%.2f,input_tokens=%s,output_tokens=%s,total_tokens=%s,%s/%s",
                    self.model,
                    total_elapsed,
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                    response.usage.total_tokens,
                    attempt,
                    self.max_attempts
                )
                return response
            except AuthenticationError as exc:
                raise LLMAuthenticationError("LLM authentication failed") from exc
            except (APITimeoutError, APIConnectionError, InternalServerError, RateLimitError) as exc:
                attempt_elapsed = time.perf_counter() - start_time
                if attempt==self.max_attempts:
                    logger.error(
                        "LLM request failed permanently,error=%s,elapsed=%.2f,attempt=%s/%s",
                        type(exc).__name__,
                        attempt_elapsed,
                        attempt,
                        self.max_attempts,
                    )
                    raise LLMConnectionError("LLM connection failed") from exc
                delay=2**(attempt-1)
                logger.warning(
                    "LLM request failed,error=%s,attempt %s/%s,elapsed=%.2f,retrying in %s seconds",
                    type(exc).__name__,attempt, self.max_attempts,attempt_elapsed, delay
                )
                time.sleep(delay)