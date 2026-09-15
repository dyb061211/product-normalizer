class AIServiceError(Exception):
    pass

class LLMAuthenticationError(AIServiceError):
    pass

class LLMConnectionError(AIServiceError):
    pass

class LLMOutputError(AIServiceError):
    pass

class UnknownToolError(AIServiceError):
    pass

class ToolArgumentError(AIServiceError):
    pass

class ToolExecutionError(AIServiceError):
    pass

class AgentMaxRoundsError(AIServiceError):
    pass