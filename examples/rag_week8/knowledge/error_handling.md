# error_handling.md

# Product Normalizer Error Handling

The project handles errors at different layers.

## LLM Errors

The LLM client handles errors such as:

- authentication failure
- timeout
- connection failure
- rate limit
- provider server error

Temporary failures may be retried.

Authentication errors are not retried because retrying with an invalid API key would not solve the problem.

## LLM Output Errors

LLM structured output is validated.

If the returned JSON is invalid or does not match the required Pydantic schema, the system raises an LLM output error.

## Tool Errors

The Tool Calling system uses a whitelist.

Only registered tools can be executed.

Possible tool errors include:

- UnknownToolError
- ToolArgumentError
- ToolExecutionError

Tool arguments are validated with Pydantic before the Python function is executed.

## Agent Tool Rounds

The assistant limits the number of tool-calling rounds.

MAX_TOOL_ROUNDS = 3

This prevents the model from repeatedly calling tools forever.

## Agent Maximum Round Error

If the model continues requesting tools after the maximum number of allowed rounds, the system raises:

AgentMaxRoundsError

## API Error Handling

Agent, Tool, and LLM exceptions are mapped to HTTP responses by the FastAPI application.

This keeps HTTP error handling separate from Agent and Tool business logic.