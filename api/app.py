from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from product_normalizer.exceptions import ProductNormalizerError
from api.routes import router
from ai.exceptions import LLMAuthenticationError,LLMConnectionError,LLMOutputError,AgentMaxRoundsError,UnknownToolError,ToolExecutionError,ToolArgumentError
from product_normalizer.logging_config import setup_logging

setup_logging()

app=FastAPI()
app.include_router(router)

@app.exception_handler(ProductNormalizerError)
async def product_normalizer_exception_handler(
        request:Request,
        exc:ProductNormalizerError
):
    return JSONResponse(
        status_code=400,
        content={"detail":str(exc)}
    )

@app.exception_handler(LLMConnectionError)
async def llm_connection_exception_handler(
        request:Request,
        exc:LLMConnectionError
):
    return JSONResponse(
        status_code=503,
        content={"detail": "AI service unavailable"}
    )

@app.exception_handler(LLMAuthenticationError)
async def llm_authentication_exception_handler(
        request:Request,
        exc:LLMAuthenticationError
):
    return JSONResponse(
        status_code=500,
        content={"detail": "AI service error"}
    )

@app.exception_handler(LLMOutputError)
async def llm_output_exception_handler(
        request:Request,
        exc:LLMOutputError
):
    return JSONResponse(
        status_code=502,
        content={"detail": "AI service returned invalid output"}
    )

@app.exception_handler(AgentMaxRoundsError)
async def agent_max_rounds_exception_handler(
        request:Request,
        exc:AgentMaxRoundsError
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Agent exceeded maximum tool rounds"}
    )

@app.exception_handler(UnknownToolError)
async def unknown_tool_error_exception_handler(
        request:Request,
        exc:UnknownToolError
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Unknown tool"}
    )

@app.exception_handler(ToolArgumentError)
async def tool_argument_error_exception_handler(
        request:Request,
        exc:ToolArgumentError
):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.exception_handler(ToolExecutionError)
async def tool_execution_error_exception_handler(
        request:Request,
        exc:ToolExecutionError
):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )