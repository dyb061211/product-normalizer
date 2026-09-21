from product_normalizer.ai.workflow.schemas import RouteDecision
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from product_normalizer.ai.workflow.state import WorkflowState
from langchain_core.prompts import ChatPromptTemplate
from product_normalizer.rag.service import answer_question
from langgraph.prebuilt import ToolNode
from product_normalizer.ai.workflow.tools import TOOLS

load_dotenv()

router_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are the router for Product Normalizer Assistant.

Choose exactly one route:

direct:
- General conversation
- Greetings
- Questions that do not require project data or project knowledge

tools:
- Questions about real processing run data
- processing_runs
- validation_issues
- A specific run
- Recent processing history

rag:
- Questions about project documentation
- API behavior
- Project architecture
- Error handling rules
- Configuration or constants such as MAX_TOOL_ROUNDS
"""
    ),
    (
        "human",
        "{question}"
    )
])

model=init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

tool_model=model.bind_tools(TOOLS)
tool_node=ToolNode(TOOLS)

structured_model=model.with_structured_output(RouteDecision)
structured_router=router_prompt|structured_model

def route_request(state: WorkflowState):
    question=state["user_query"]
    decision=structured_router.invoke({
        "question":question
    })
    return {
        "route":decision.route
    }

def direct_answer(state: WorkflowState):
   response=model.invoke(state["user_query"])
   return {
       "messages":[response],
       "answer":response.content,
       "status":"success"
   }

def rag_answer(state: WorkflowState):
    response=answer_question(state["user_query"])
    if not response.sources:
        return {
            "answer":response.answer,
            "sources":response.sources,
            "status":"no_answer"
        }
    return {
        "answer": response.answer,
        "sources": response.sources,
        "status": "success"
    }

def increment_tool_round(state:WorkflowState):
    return {
        "tool_rounds":state["tool_rounds"]+1
    }

def tool_llm(state:WorkflowState):
    response=tool_model.invoke(state["messages"])
    return {
        "messages":[response]
    }

def finalize(state:WorkflowState):
    if state["status"] == "error":
        return {}
    if state["route"]=="tools":
        return {
            "answer":str(state["messages"][-1].content),
            "status":"success"
        }
    return {}

def max_rounds_error(state:WorkflowState):
    return {
        "answer":"Tool workflow reached the maximum number of rounds.",
        "status":"error",
        "error_type":"max_rounds_error",
        "error_message":"Maximum number of rounds reached.",
    }


